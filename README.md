# PlacementOS — AI-Orchestrated Campus Placement Drive Management

**UiPath AgentHack 2025 | Track 2: UiPath Maestro BPMN**

---

## What It Does

PlacementOS orchestrates end-to-end campus placement drives on **UiPath Maestro BPMN**. Every drive runs as a live process instance — from company registration through AI resume screening, TPO approval, interview scheduling, offer dispatch, and ERP record update — with the right actor doing the right task at the right time.

It replaces the chaos of WhatsApp groups, spreadsheets, and email threads that Training & Placement Officers at Indian engineering colleges currently use to manage 50+ simultaneous drives.

---

## The Business Problem

A college placement office running simultaneous drives for 50 companies faces:

- **No visibility**: No one knows where each candidate stands across companies until it's over
- **Manual shortlisting**: Resume screening is entirely manual, taking 3–5 hours per drive
- **Coordination failures**: Interview scheduling happens over phone calls and email chains
- **Offer dispatch errors**: Offer letters are manually filled Word documents, prone to errors
- **Zero audit trail**: No record of AI scores, TPO decisions, or why candidates were rejected

PlacementOS fixes all of these. A drive that takes 2 weeks of coordinator effort runs automatically in 48 hours, with every decision logged.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     UiPath Automation Cloud                          │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                  UiPath Maestro BPMN Engine                    │ │
│  │                                                                │ │
│  │  [Drive Start] → [Fetch Students] → [AI Screen] → [TPO Gate]  │ │
│  │  → [HR Slots] → [Calendar+Email] → [Interview] → [Offers]     │ │
│  │  → [Dispatch] → [ERP Update] → [Complete]                     │ │
│  └───────────────────────┬────────────────────────────────────────┘ │
│                           │ orchestrates                             │
│        ┌──────────────────┼──────────────────────┐                  │
│        │                  │                      │                  │
│   ┌────▼────┐       ┌─────▼──────┐       ┌──────▼──────┐          │
│   │  RPA    │       │  External  │       │   Action    │          │
│   │  Bots   │       │   Agent    │       │   Center    │          │
│   │(Studio) │       │(LangChain) │       │ Human Tasks │          │
│   └────┬────┘       └─────┬──────┘       └─────────────┘          │
│        │                  │                                         │
└────────┼──────────────────┼─────────────────────────────────────────┘
         │                  │
   ┌─────▼──────────────────▼────────────────┐
   │         External Services                │
   │  • Mock College ERP (FastAPI)            │
   │  • Resume Screener Agent (FastAPI)       │
   │  • Google Calendar API                  │
   │  • SMTP Email                            │
   │  • html2pdf.app (offer letter PDF)       │
   └─────────────────────────────────────────┘
```

---

## UiPath Components Used

| Component | Role |
|---|---|
| **UiPath Maestro BPMN** | Main process orchestrator — defines the entire drive lifecycle |
| **UiPath Action Center** | TPO shortlist review, HR slot confirmation, HR interview results entry |
| **UiPath RPA (Studio)** | ERPFetchBot, CalendarEmailBot, PlacementRecordBot |
| **UiPath API Workflow** | OfferLetterGenerator — builds and converts offer letter to PDF |

---

## External Components (Bonus: Built with Claude Code)

| Component | Stack | Location |
|---|---|---|
| Resume Screener Agent | FastAPI + LangChain + Google Gemini 1.5 Flash | `resume-screener/` |
| Mock College ERP | FastAPI + JSON file store | `mock-erp/` |

Both services were generated using **Claude Code** as part of **UiPath for Coding Agents**. See `docs/claude-code-demo.md` for the exact prompts and outputs.

---

## BPMN Process Flow

```
START: Drive Registered
  │
  ▼ [ERPFetchBot]
Fetch Eligible Students (queries ERP with min_cgpa, branches, max_backlogs)
  │
  ▼ [LangChain Agent]
AI Resume Screening (scores each resume 0-100 against JD)
  │
  ▼ [Exclusive Gateway]
Screened List Empty? → YES → End (No Match)
  │ NO
  ▼ [Action Center — TPO]
TPO Shortlist Review (24h SLA, timer escalation to admin)
  │
  ▼ [Exclusive Gateway]
Shortlist Approved? → REJECTED → End (Drive Cancelled)
  │ APPROVED
  ▼ [Action Center — Company HR]
HR Confirms Interview Slots (date, time, mode, panel)
  │
  ▼ [CalendarEmailBot]
Push Calendar Invites + Send Confirmation Emails
  │
  ▼ [Action Center — Company HR]
HR Submits Interview Results (per-candidate: Selected / Not Selected)
  │
  ▼ [API Workflow]
Generate Offer Letters (PDF via html2pdf.app)
  │
  ▼ [CalendarEmailBot / EmailDispatchBot]
Dispatch Offers (PDF attachment) + Rejections (with feedback)
  │
  ▼ [PlacementRecordBot]
Update ERP Placement Records
  │
  ▼
END: Drive Completed
```

---

## Project Structure

```
placement-os/
├── README.md
├── LICENSE                            MIT
├── .env.example
│
├── resume-screener/                   LangChain resume screening agent
│   ├── main.py                        FastAPI app, /health and /screen
│   ├── agent.py                       Async LangChain scoring with retry
│   ├── models.py                      Pydantic request/response schemas
│   ├── prompts.py                     System and scoring prompt templates
│   ├── requirements.txt
│   └── render.yaml
│
├── mock-erp/                          Simulated college ERP
│   ├── main.py                        FastAPI: /students/eligible, /placements
│   ├── data/
│   │   ├── students.json              20 realistic BITS Pilani students
│   │   └── placements.json            Placement records (starts empty)
│   ├── requirements.txt
│   └── render.yaml
│
├── uipath/
│   ├── bpmn/
│   │   └── placement-drive-process.bpmn   BPMN 2.0 process definition
│   ├── bots/
│   │   ├── ERPFetchBot/               Studio project: fetches eligible students
│   │   ├── CalendarEmailBot/          Studio project: sends confirmation emails
│   │   └── PlacementRecordBot/        Studio project: writes outcomes to ERP
│   └── workflows/
│       └── offer-letter-generator.json    API Workflow definition
│
├── action-center-forms/
│   ├── tpo-shortlist-review.json      TPO candidate approval form schema
│   ├── hr-interview-slots.json        HR scheduling form schema
│   └── hr-interview-results.json      HR outcome entry form schema
│
└── docs/
    ├── architecture.md
    ├── claude-code-demo.md            Prompts used with Claude Code
    └── test-drive-payload.json        Sample payload for triggering a test drive
```

---

## Live Deployments

| Service | URL |
|---------|-----|
| Resume Screener | https://placement-os-kceh.onrender.com |
| Mock ERP | https://placement-os-1.onrender.com |

## Prerequisites

- UiPath Automation Cloud account (UiPath Labs access from the hackathon)
- Python 3.11+
- Groq API key (free — get at https://console.groq.com)
- SMTP credentials (Gmail app password works)
- Google Calendar API credentials — OAuth2 (optional; email-only fallback built in)

---

## Setup Instructions

### 1. Deploy the Resume Screener

```bash
cd resume-screener
cp ../.env.example .env
# Set OPENAI_API_KEY in .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Test it:
```bash
curl -X POST http://localhost:8000/screen \
  -H "Content-Type: application/json" \
  -d @docs/test-screen-payload.json
```

To deploy to Render: push this folder to a GitHub repo and connect it in Render using `render.yaml`.

### 2. Deploy the Mock ERP

```bash
cd mock-erp
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Test it:
```bash
curl "http://localhost:8001/students/eligible?min_cgpa=7.5&branches=CSE,IT&max_backlogs=0"
```

### 3. Configure UiPath Automation Cloud

1. **Import BPMN process**: In Maestro → New Process → Import → select `uipath/bpmn/placement-drive-process.bpmn`
2. **Publish RPA bots**: Open each folder in `uipath/bots/` in UiPath Studio, publish to your Orchestrator tenant
3. **Configure API Workflow**: In UiPath Integration Service → create API Workflow from `uipath/workflows/offer-letter-generator.json`
4. **Set up Action Center task forms**: Use the JSON schemas in `action-center-forms/` to configure task forms
5. **Set Orchestrator assets** (name → value):
   - `ERP_BASE_URL` → your deployed mock ERP URL
   - `SCREENER_URL` → your deployed resume screener URL
   - `SMTP_HOST` → your SMTP host
   - `SMTP_USER` → your email address
   - `SMTP_PASSWORD` → your app password (store as credential)

### 4. Trigger a Test Drive

Use the payload in `docs/test-drive-payload.json` to start a process instance from Orchestrator or via UiPath Apps.

---

## Built with UiPath for Coding Agents

The resume screening agent and mock ERP were generated using **Claude Code** as part of UiPath for Coding Agents.

See `docs/claude-code-demo.md` for:
- The exact prompts used
- Screen recordings of the generation session
- How the generated code was validated and deployed

---

## License

MIT — see `LICENSE`
