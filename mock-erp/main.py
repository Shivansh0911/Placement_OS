import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PlacementOS Mock ERP",
    description="Simulates a college ERP system for student and placement data",
    version="1.0.0",
)

DATA_DIR = Path(__file__).parent / "data"


def _load(filename: str) -> list:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def _save(filename: str, data: list) -> None:
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)


# ── Request/Response Models ─────────────────────────────────────────────────

class PlacementRecord(BaseModel):
    drive_id: str
    company_name: str
    role: str
    package_lpa: float
    student_id: str
    student_name: str
    joining_date: Optional[str] = None
    status: str = "OFFER_ACCEPTED"


# ── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    students = _load("students.json")
    return {"status": "ok", "student_count": len(students)}


@app.get("/students/eligible")
def get_eligible_students(
    min_cgpa: float = Query(6.0, ge=0, le=10, description="Minimum CGPA threshold"),
    branches: Optional[str] = Query(
        None, description="Comma-separated branch codes, e.g. CSE,IT,ECE"
    ),
    max_backlogs: int = Query(0, ge=0, description="Maximum number of active backlogs"),
):
    students = _load("students.json")
    branch_filter: Optional[List[str]] = (
        [b.strip().upper() for b in branches.split(",")] if branches else None
    )

    eligible = [
        s for s in students
        if s["cgpa"] >= min_cgpa
        and s["backlogs"] <= max_backlogs
        and (branch_filter is None or s["branch"].upper() in branch_filter)
    ]

    logger.info(
        "Eligibility query — min_cgpa=%.1f, branches=%s, max_backlogs=%d → %d/%d eligible",
        min_cgpa, branch_filter, max_backlogs, len(eligible), len(students),
    )
    return {"eligible_students": eligible, "count": len(eligible)}


@app.get("/students/{student_id}")
def get_student(student_id: str):
    students = _load("students.json")
    match = next((s for s in students if s["student_id"] == student_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return match


@app.post("/placements/record", status_code=201)
def record_placement(payload: PlacementRecord):
    placements = _load("placements.json")
    record = payload.model_dump()
    record["record_id"] = str(uuid.uuid4())[:8].upper()
    record["recorded_at"] = datetime.utcnow().isoformat() + "Z"
    placements.append(record)
    _save("placements.json", placements)
    logger.info("Placement recorded: %s → %s (%s)", record["student_name"], record["company_name"], record["record_id"])
    return {"status": "recorded", "record_id": record["record_id"]}


@app.get("/placements")
def get_placements(
    drive_id: Optional[str] = Query(None),
    company_name: Optional[str] = Query(None),
):
    placements = _load("placements.json")
    if drive_id:
        placements = [p for p in placements if p.get("drive_id") == drive_id]
    if company_name:
        placements = [p for p in placements if company_name.lower() in p.get("company_name", "").lower()]
    return {"placements": placements, "count": len(placements)}


@app.get("/placements/summary")
def placement_summary():
    placements = _load("placements.json")
    if not placements:
        return {"total_offers": 0, "companies": [], "avg_package_lpa": 0}
    packages = [p["package_lpa"] for p in placements if "package_lpa" in p]
    companies = list({p["company_name"] for p in placements})
    return {
        "total_offers": len(placements),
        "companies": companies,
        "avg_package_lpa": round(sum(packages) / len(packages), 2) if packages else 0,
        "max_package_lpa": max(packages) if packages else 0,
    }


@app.delete("/placements/reset", status_code=200)
def reset_placements():
    _save("placements.json", [])
    return {"status": "reset", "message": "All placement records cleared (demo use only)"}
