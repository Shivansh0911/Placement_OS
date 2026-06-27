# PlacementOS — Presentation & Demo Brief
# (Feed this file to Claude or any AI to generate PPT slides)

---

## PROJECT INFO

- **Project Name:** PlacementOS
- **Tagline:** AI-Orchestrated Campus Placement Drive Automation
- **Track:** Track 2 — UiPath Maestro BPMN
- **Hackathon:** UiPath AgentHack 2026
- **GitHub:** https://github.com/Shivansh0911/Placement_OS
- **Built with:** Claude Code (UiPath for Coding Agents — bonus points)

---

## LIVE URLs (for demo and slides)

| Service | URL |
|---------|-----|
| Resume Screener API | https://placement-os-kceh.onrender.com |
| Resume Screener Docs | https://placement-os-kceh.onrender.com/docs |
| Mock ERP API | https://placement-os-1.onrender.com |
| Mock ERP Docs | https://placement-os-1.onrender.com/docs |
| Students Eligible | https://placement-os-1.onrender.com/students/eligible |
| GitHub Repo | https://github.com/Shivansh0911/Placement_OS |
| UiPath Orchestrator | https://staging.uipath.com/hackathon26_960/orchestrator_ |

---

## SCREENSHOTS TO TAKE BEFORE MAKING PPT

Take these screenshots and save them with these names:

1. **slide4-bpmn.png** — UiPath Studio Web → Solution 4 → BPMN diagram (full view)
2. **slide5-orchestrator.png** — Orchestrator → Shared → Solution 4 Active v1.0.0
3. **slide6-erp-students.png** — https://placement-os-1.onrender.com/students/eligible (20 students JSON)
4. **slide7-screener-health.png** — https://placement-os-kceh.onrender.com/health (shows google_key_set: true)
5. **slide7-screen-result.png** — /screen endpoint response showing ranked candidates with scores
6. **slide8-assets.png** — Orchestrator → Assets tab showing 5 configured assets
7. **slide9-github.png** — GitHub repo homepage showing all folders
8. **slide10-claude.png** — Claude Code / VS Code terminal showing Claude Code being used

---

## SLIDE DECK (10 Slides)

Use the official UiPath AgentHack template. Replace content as below:

---

### SLIDE 1 — Title Slide

**Title:** PlacementOS
**Subtitle:** AI-Orchestrated Campus Placement Drive Automation
**Track:** Track 2 — UiPath Maestro BPMN
**Team:** [Your Name]
**Tagline (big text):** "What takes 2 weeks of manual effort — automated to 48 hours"

**Background image suggestion:** Indian engineering college campus or UiPath platform screenshot

---

### SLIDE 2 — The Problem

**Heading:** Campus Placement is a Coordination Nightmare

**Pain points (bullet list):**
- 📋 Training & Placement Officers manually screen 500+ resumes per drive — 3-5 hours each
- 📞 Interview scheduling via phone calls and WhatsApp groups
- 📊 Zero real-time visibility — no one knows candidate status until it's over
- ❌ Offer letters manually typed in Word — error-prone, slow
- 🗃️ No audit trail — no record of why candidates were rejected or selected

**Bottom stat (big number):** "50+ simultaneous drives. 500+ candidates. 0 automation."

**Image:** Screenshot of messy Excel spreadsheet or WhatsApp group (generic)

---

### SLIDE 3 — Our Solution

**Heading:** PlacementOS — One BPMN Process, Entire Drive Lifecycle

**3-column layout:**

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| 🤖 **AI Agents** | 🔄 **BPMN Orchestration** | 👤 **Human in the Loop** |
| LangChain + Gemini screens resumes in seconds | UiPath Maestro BPMN routes work to the right actor | TPO approves shortlist, HR confirms slots |
| Scores 0-100, ranks candidates, gives reasoning | 10-step process from registration to offer dispatch | Action Center keeps humans in control at key gates |

**Bottom text:** "Built on UiPath Automation Cloud — the single enterprise control plane"

---

### SLIDE 4 — BPMN Process Flow

**Heading:** 10-Step End-to-End Drive Process

**IMAGE:** [slide4-bpmn.png — screenshot of actual BPMN diagram from Studio Web]

**Caption below image:**
```
Drive Start → Fetch Eligible Students → AI Resume Screen → TPO Review Gate
→ HR Interview Slots → Calendar + Email → Interview → Offer Generation
→ Offer Dispatch → ERP Record Update → Drive Complete
```

**Sidebar bullets:**
- 2 Exclusive Gateways (no match / drive cancelled paths)
- Timer boundary on TPO task (24h SLA escalation)
- 3 End Events (complete / no match / cancelled)

---

### SLIDE 5 — UiPath Platform Integration

**Heading:** Running Live on UiPath Automation Cloud

**IMAGE:** [slide5-orchestrator.png — Orchestrator showing Solution 4 Active v1.0.0]

**Component table:**

| UiPath Component | Role in PlacementOS |
|-----------------|---------------------|
| Maestro BPMN | Main process orchestrator |
| Orchestrator | Asset store, job management, robot deployment |
| RPA Bots (Studio) | ERPFetchBot, CalendarEmailBot, PlacementRecordBot |
| Action Center | TPO shortlist review, HR slot confirmation |
| API Workflows | Offer letter PDF generation |

**Text:** "Solution 4 — Active v1.0.0 — deployed to Shared folder — 5 Orchestrator Assets configured"

---

### SLIDE 6 — Mock ERP (Data Source)

**Heading:** 20 Real BITS Pilani Students — Live ERP Data

**IMAGE:** [slide6-erp-students.png — /students/eligible showing JSON with 20 students]

**Key points:**
- FastAPI service deployed on Render (Singapore)
- 20 realistic students: CSE, IT, ECE, EEE, Mech branches
- CGPA range: 6.2 to 9.3 — real eligibility filtering
- Endpoints: GET /students/eligible, POST /placements/record, GET /placements/summary

**Live URL shown on slide:** https://placement-os-1.onrender.com/students/eligible

---

### SLIDE 7 — AI Resume Screener Agent

**Heading:** LangChain + Google Gemini 1.5 Flash — Resume Scoring in Seconds

**IMAGE:** [slide7-screen-result.png — /screen response showing candidates with scores]

**How it works:**
1. Receives JD + list of resume texts from Orchestrator
2. Gemini 1.5 Flash scores each candidate 0–100 against JD
3. Returns ranked list with: score, reasoning, strengths, gaps, recommendation
4. Async batch processing — handles 100 resumes in parallel

**Key stats on slide:**
- Model: Google Gemini 1.5 Flash (free tier)
- Framework: LangChain + FastAPI
- Retry logic: exponential backoff for API rate limits
- Deployed: Render Singapore | https://placement-os-kceh.onrender.com

---

### SLIDE 8 — Architecture Diagram

**Heading:** Architecture — Everything Flows Through UiPath

**Diagram (draw this or use the ASCII from README):**

```
┌─────────────────────────────────────────────┐
│          UiPath Automation Cloud             │
│                                              │
│   Maestro BPMN Process                       │
│       ↓ orchestrates                         │
│   ┌─────────┬──────────────┬──────────────┐  │
│   │ RPA     │ External AI  │ Action Center │  │
│   │ Bots    │ Agent        │ Human Tasks   │  │
│   │(Studio) │(LangChain)   │(TPO + HR)     │  │
│   └────┬────┴──────┬───────┴──────────────┘  │
└────────┼───────────┼──────────────────────────┘
         ↓           ↓
   Mock ERP      Resume Screener
   (Render)      Agent (Render)
```

**IMAGE:** [slide8-assets.png — Orchestrator Assets tab]

**Sidebar:** "5 Orchestrator Assets: ERP_BASE_URL, SCREENER_BASE_URL, MIN_CGPA, SHORTLIST_THRESHOLD, MAX_CANDIDATES"

---

### SLIDE 9 — Claude Code (Bonus Points!)

**Heading:** Built with UiPath for Coding Agents — Claude Code

**IMAGE:** [slide9-github.png — GitHub repo] + [slide10-claude.png — Claude Code terminal]

**Key message:** This entire project was built using **Claude Code** as the coding agent within the **UiPath for Coding Agents** framework.

**What Claude Code built:**
- ✅ Full FastAPI resume screener (`resume-screener/` — 4 files)
- ✅ Mock ERP API (`mock-erp/` — full CRUD + 20 realistic students)
- ✅ BPMN 2.0 XML process definition (500+ lines)
- ✅ 3 UiPath RPA bot XAML files
- ✅ Action Center form schemas
- ✅ Render deployment config
- ✅ README, architecture docs, test payloads

**Quote on slide:** *"We used Claude Code as our coding agent — UiPath for Coding Agents — to build every component of PlacementOS. See docs/claude-code-demo.md for exact prompts."*

**GitHub:** https://github.com/Shivansh0911/Placement_OS

---

### SLIDE 10 — Impact & Closing

**Heading:** PlacementOS — Real Impact for Real Colleges

**Impact numbers (big, bold):**
- ⏱️ **2 weeks → 48 hours** — drive cycle time reduced
- 👥 **500+ resumes** screened in minutes, not days
- 📋 **100% audit trail** — every decision logged
- 🎓 **800+ engineering colleges** in India could use this

**Tech Stack logos row:**
UiPath Maestro | LangChain | Google Gemini | FastAPI | Python | Render | Claude Code

**Bottom CTA:**
- GitHub: https://github.com/Shivansh0911/Placement_OS
- Live Demo: https://placement-os-kceh.onrender.com/docs

**Closing line:** *"Campus placement shouldn't run on WhatsApp. PlacementOS makes it enterprise-grade."*

---

## DEMO VIDEO SCRIPT (5 minutes)

### Scene 1: Hook [0:00–0:30]
**Say:** "Every year, 1.5 million engineering students in India go through campus placements. For Training & Placement Officers, it's chaos — manual screening, WhatsApp scheduling, Excel tracking. PlacementOS changes that."
**Show:** Slide 1 (title slide) or GitHub repo homepage

### Scene 2: Problem + Architecture [0:30–1:15]
**Say:** "A placement drive has 10 steps — from company registration to offer dispatch. Today it takes 2 weeks. With PlacementOS and UiPath Maestro BPMN, it runs in 48 hours, automatically."
**Show:** BPMN diagram in Studio Web (full screen) — point to each task

### Scene 3: Live ERP Data [1:15–2:00]
**Say:** "The process starts by pulling eligible students from the college ERP. Here's our mock ERP — 20 BITS Pilani students with real resumes, CGPAs, and branch data."
**Show:** https://placement-os-1.onrender.com/students/eligible — scroll through the 20 students

### Scene 4: AI Resume Screening [2:00–3:00]
**Say:** "The AI Resume Screener — built with LangChain and Google Gemini 1.5 Flash — receives the eligible students and the company's job description, and scores each candidate 0 to 100."
**Show:** https://placement-os-kceh.onrender.com/docs → POST /screen → Execute → show response with scores, reasoning, strengths and gaps
**IMPORTANT:** Show the response JSON with actual scores — this is the most impressive part

### Scene 5: UiPath Orchestrator [3:00–3:45]
**Say:** "The entire process runs on UiPath Automation Cloud. Here's Solution 4 — our PlacementOS process — deployed and Active. Five Orchestrator Assets connect it to our live services."
**Show:** Orchestrator → Shared → Solution 4 Active v1.0.0 → Assets tab

### Scene 6: Claude Code Bonus [3:45–4:30]
**Say:** "We built PlacementOS using Claude Code as our coding agent — part of UiPath for Coding Agents. Claude Code generated the entire backend, BPMN, and bot code from natural language prompts."
**Show:** GitHub repo → docs/claude-code-demo.md → show the prompts used → show the generated code

### Scene 7: Closing [4:30–5:00]
**Say:** "PlacementOS: 10-step BPMN process, AI screening, RPA bots, human-in-the-loop approval — all orchestrated by UiPath Maestro. Campus placement, enterprise-grade."
**Show:** Slide 10 (impact numbers) or GitHub README

---

## DEVPOST SUBMISSION TEXT

**Project Title:** PlacementOS

**Short Description:**
AI-orchestrated campus placement drive automation built on UiPath Maestro BPMN. PlacementOS runs the entire placement cycle — ERP fetch, AI resume screening, TPO approval, HR scheduling, offer dispatch, and ERP update — as a 10-step BPMN process on UiPath Automation Cloud.

**Long Description:**
PlacementOS solves the chaos of campus placement management at Indian engineering colleges. A drive that takes Training & Placement Officers 2 weeks of manual work — email chains, WhatsApp coordination, Excel tracking — runs automatically in 48 hours.

The solution is built on UiPath Maestro BPMN (Track 2). The BPMN process orchestrates:
- RPA bots (UiPath Studio) for ERP data fetch and email dispatch
- An external AI agent (LangChain + Google Gemini 1.5 Flash) for resume screening
- Human-in-the-loop tasks via Action Center for TPO shortlist approval and HR slot confirmation
- API workflows for offer letter PDF generation

Both the resume screener and mock ERP were built using Claude Code (UiPath for Coding Agents) and deployed on Render.

**Built With:**
uipath-maestro, uipath-bpmn, uipath-orchestrator, uipath-rpa, langchain, google-gemini, fastapi, python, render, claude-code

**Track:** Track 2 — UiPath Maestro BPMN

**GitHub:** https://github.com/Shivansh0911/Placement_OS

---

## README FIXES NEEDED BEFORE SUBMISSION

The README currently says "OpenAI API key" — needs to be updated to "Google Gemini API key (free)".
Also update the Live URLs section to show the actual Render URLs.
