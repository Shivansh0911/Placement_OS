# PlacementOS Architecture

## Design Principles

**1. Maestro BPMN as the single source of truth.**
Every state transition — who has the work, what was decided, where the drive stands — lives in the BPMN process instance. Bots and agents are stateless executors; the process holds the state.

**2. Fail gracefully, never block the BPMN.**
Every service task has explicit error handling. If the LangChain screener is down, the process falls back to the full eligible list and lets the TPO screen manually. If the ERP returns an error, a BPMN error boundary event catches it and sets a process variable — the human can intervene. No silent failures.

**3. Human gates are real, not decorative.**
The TPO approval and HR slot confirmation aren't formalities — they're exclusive gateways with real process branches. If the TPO rejects all candidates, the process ends. The BPMN diagram makes this visible, not buried in code.

**4. Agents are external services, not embedded logic.**
The LangChain resume screener is a separate deployed service called over HTTP. This means it can be swapped, tested independently, and scaled separately. UiPath calls it; UiPath doesn't host it.

---

## Data Flow

```
Company HR Input (form)
    │
    ▼
Process Variables in Maestro BPMN
    ├── drive_id
    ├── company_name
    ├── job_description
    └── eligibility_criteria (JSON)
            │
            ▼
    ERPFetchBot reads eligibility_criteria
    Calls: GET /students/eligible?min_cgpa=X&branches=Y&max_backlogs=Z
    Writes: eligible_students (JSON array) → process variable
            │
            ▼
    ResumeScreenerAgent reads eligible_students + job_description
    Calls: POST /screen with resumes array
    Writes: screened_results (JSON ranked array) → process variable
            │
            ▼
    Action Center reads screened_results
    TPO interacts → writes: tpo_decision, shortlisted_ids
            │
            ▼
    Action Center reads shortlisted_ids
    HR interacts → writes: interview_schedule (JSON)
            │
            ▼
    CalendarEmailBot reads shortlisted_ids + interview_schedule
    Sends confirmation emails
            │
            ▼
    Action Center (HR enters results)
    Writes: interview_results (JSON per-candidate outcomes)
            │
            ▼
    OfferLetterWorkflow reads interview_results
    Generates PDFs, writes: offer_pdfs_base64
            │
            ▼
    EmailDispatchBot reads interview_results + offer_pdfs_base64
    Sends offers and rejections
            │
            ▼
    PlacementRecordBot reads interview_results + drive_id + company_name
    Calls: POST /placements/record for each selected candidate
```

---

## Process Variables Reference

| Variable | Type | Set By | Read By |
|---|---|---|---|
| `drive_id` | String | Process start input | All bots |
| `company_name` | String | Process start input | All bots, Action Center |
| `job_description` | String | Process start input | Screener agent |
| `eligibility_criteria` | String (JSON) | Process start input | ERPFetchBot |
| `eligible_students` | String (JSON array) | ERPFetchBot | Screener agent |
| `screened_results` | String (JSON array) | Screener agent | Action Center (TPO) |
| `screened_results_count` | Int32 | Screener agent | Gateway |
| `tpo_decision` | String | Action Center (TPO) | Gateway |
| `shortlisted_ids` | String (JSON array) | Action Center (TPO) | Action Center (HR), CalendarBot |
| `interview_schedule` | String (JSON) | Action Center (HR) | CalendarBot |
| `interview_results` | String (JSON) | Action Center (HR) | OfferWorkflow, EmailBot, RecordBot |
| `offer_pdfs_base64` | String (JSON map) | API Workflow | EmailBot |
| `process_status` | String | Error boundaries | Monitoring/alerting |

---

## Error Handling Summary

| Failure | Detection Point | Recovery |
|---|---|---|
| ERP API down | ERPFetchBot HTTP exception | Throws ApplicationException → BPMN error boundary → sets process_status = ERP_FETCH_FAILED, notifies admin |
| Screener API down | Service task timeout/HTTP error | Fallback: use full eligible_students list, add note to screened_results indicating manual review needed |
| Zero eligible students | ERP returns empty array | Gateway routes to "No Match" end event, ERP count = 0 |
| TPO SLA exceeded | Timer boundary event (24h) | Non-interrupting: sends escalation email to admin. Task stays alive. |
| OpenAI rate limit | agent.py retry logic | 3 exponential backoff attempts. On final failure: neutral score (50/MAYBE) returned |
| Email send failure | CalendarEmailBot try/catch | Logs error, continues to next candidate — partial delivery is better than full failure |
| PDF generation failure | API Workflow try/catch | Sets generation_status = FALLBACK_TEXT_ONLY, sends text-only email |
| ERP record write failure | PlacementRecordBot try/catch | Logs error per candidate, continues — final summary logged |
