import asyncio
import json
import logging
import time
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from models import ScreeningRequest, ScreeningResponse, CandidateScore, Recommendation
from prompts import SYSTEM_PROMPT, SCORING_PROMPT

logger = logging.getLogger(__name__)

_llm: Optional[ChatGroq] = None


def get_llm() -> ChatGroq:
    global _llm
    if _llm is None:
        _llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
    return _llm


def _neutral_score(resume_input, reason: str) -> CandidateScore:
    return CandidateScore(
        student_id=resume_input.student_id,
        name=resume_input.name,
        score=50.0,
        reasoning=reason,
        strengths=["Review resume directly — automated scoring unavailable"],
        gaps=["Manual review required"],
        recommendation="MAYBE",
    )


async def _score_with_retry(
    jd: str, criteria: dict, resume_input, max_retries: int = 3
) -> CandidateScore:
    prompt = SCORING_PROMPT.format(
        job_description=jd,
        eligibility_criteria=json.dumps(criteria, indent=2),
        candidate_name=resume_input.name,
        resume_text=resume_input.resume_text,
    )
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
    llm = get_llm()

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                await asyncio.sleep(35)
            response = await llm.ainvoke(messages)
            raw = response.content.strip()

            # Strip accidental markdown fences
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            data = json.loads(raw)

            # Clamp score to valid range
            data["score"] = max(0.0, min(100.0, float(data.get("score", 50))))

            # Validate recommendation field
            valid_recs: set[Recommendation] = {"STRONG_YES", "YES", "MAYBE", "NO"}
            if data.get("recommendation") not in valid_recs:
                data["recommendation"] = "MAYBE"

            return CandidateScore(
                student_id=resume_input.student_id,
                name=resume_input.name,
                **data,
            )

        except Exception as e:
            logger.warning("LLM error for %s (attempt %d/%d): %s", resume_input.student_id, attempt + 1, max_retries, e)
            if attempt >= max_retries - 1:
                return _neutral_score(resume_input, f"LLM unavailable after {max_retries} attempts.")

        except json.JSONDecodeError as e:
            logger.warning(
                "JSON parse failed for %s: %s", resume_input.student_id, e
            )
            return _neutral_score(resume_input, "Could not parse model response. Manual review required.")

        except Exception as e:
            logger.error("Unexpected error for %s (%s): %s", resume_input.student_id, type(e).__name__, e)
            return _neutral_score(resume_input, f"Screening error ({type(e).__name__}). Manual review required.")

    return _neutral_score(resume_input, "Max retries exceeded.")


async def screen_candidates(request: ScreeningRequest) -> ScreeningResponse:
    start = time.monotonic()

    tasks = [
        _score_with_retry(request.job_description, request.eligibility_criteria, r)
        for r in request.resumes
    ]

    # Throttle: process in batches of 10 to avoid overwhelming the API
    batch_size = 10
    results: list[CandidateScore] = []
    for i in range(0, len(tasks), batch_size):
        batch = await asyncio.gather(*tasks[i : i + batch_size])
        results.extend(batch)
        if i + batch_size < len(tasks):
            await asyncio.sleep(0.5)  # brief pause between batches

    ranked = sorted(results, key=lambda x: x.score, reverse=True)
    recommended = [c for c in ranked if c.recommendation in ("STRONG_YES", "YES")]

    elapsed = time.monotonic() - start
    logger.info(
        "Screened %d candidates in %.1fs. Recommended: %d.",
        len(ranked),
        elapsed,
        len(recommended),
    )

    summary = (
        f"Screened {len(ranked)} candidates in {elapsed:.1f}s. "
        f"{len(recommended)} recommended (score ≥ 65). "
        f"Top candidate: {ranked[0].name} ({ranked[0].score:.0f}/100)."
        if ranked
        else f"Screened 0 candidates."
    )

    return ScreeningResponse(
        ranked_candidates=ranked,
        screening_summary=summary,
        total_screened=len(ranked),
        recommended_count=len(recommended),
    )
