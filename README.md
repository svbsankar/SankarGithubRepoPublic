# 🔍 JobScan AI — Verified Job Search Agent

> An AI-powered job search agent that finds **real, verified job listings** and eliminates fake, scam, duplicate, and ghost jobs — powered by Claude Sonnet 4 with live web search.

---

## 🚀 What It Does

JobScan AI is a single-file HTML agent that:

- **Searches live job boards** — LinkedIn, Indeed, Glassdoor, and company career pages in real time
- **Eliminates fake jobs** — scams, MLM schemes, ghost listings, duplicates, and low-quality postings
- **Validates every result** using 8 automated checks before showing it to you
- **Scores each job** with a Trust Score (0–100) so you know how reliable each listing is
- **Shows what was rejected** — full transparency on why flagged jobs were eliminated

---

## 🛡 8-Layer Validation System

Every job goes through all of these before appearing in results:

| Check | What It Does |
|---|---|
| Live job board search | Searches multiple real-time sources |
| Company verification | Confirms company exists on LinkedIn / official site |
| Duplicate detection | Removes same job posted across multiple boards |
| Scam pattern scan | Flags "earn $5000/day", no company name, gmail apply addresses |
| Salary sanity check | Validates salary is realistic for the role and location |
| Domain legitimacy | Checks apply URL links to real company or major job board |
| Freshness validation | Prioritizes jobs posted within last 7–30 days |
| Ghost job detection | Flags stale postings from companies known to recycle listings |

---

## 🏗 Architecture

```
User Input (role + location + filters)
        │
        ▼
Claude Sonnet 4 API  ←──  web_search tool (live internet)
        │
        ▼
Agent runs multiple search queries across job boards
        │
        ▼
Validation & Fake Elimination Engine (inside LLM prompt)
        │
   ┌────┴────┐
   ▼         ▼
Verified   Eliminated
 Jobs       Jobs
   │         │
   ▼         ▼
Trust     Rejection
Score     Reason
   │
   ▼
Rendered Job Cards (HTML UI)
```

---

## 🧠 How the Agent Was Built

### Step 1 — Problem Definition
Job boards are flooded with ghost jobs, scam listings, duplicates, and MLM postings. The agent needed two distinct phases: **retrieval** and **validation**.

### Step 2 — Model + Tool Selection
Uses **Claude Sonnet 4** with the `web_search_20250305` tool via the Anthropic API. This enables live internet access so results are always current — not from stale training data.

### Step 3 — System Prompt Engineering
The system prompt defines:
- Hard elimination rules (boolean filters the model must apply)
- A Trust Score formula with explicit point values per signal
- A strict JSON output schema for deterministic parsing

### Step 4 — Validation Matrix UI
The 8 validation checks are all handled inside the single agent prompt. The UI animates them in sequence to make the process transparent and build user trust.

### Step 5 — Response Parsing
Strips markdown fences before parsing, uses regex to extract the JSON object even if the model adds surrounding commentary.

### Step 6 — Eliminated Jobs Section
Every rejected job is returned in a separate `eliminated` array with a specific reason — so users can audit the agent's decisions.

---

## 📁 File Structure

```
SankarGithubRepoPublic/
├── job_agent.html      ← The complete JobScan AI agent (single file)
├── README.md           ← This file
└── ... (other Python files)
```

---

## ▶ How to Run

No installation needed. It's a single HTML file.

1. Download `job_agent.html`
2. Open it in any modern browser (Chrome, Firefox, Edge, Safari)
3. Type a job title and location
4. Click **Run Job Agent**

> The agent calls the Anthropic API directly from the browser. An API key is pre-configured via the Claude.ai artifact runtime.

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Claude Sonnet 4 (`claude-sonnet-4-20250514`) |
| Live Search | Anthropic `web_search_20250305` tool |
| API | Anthropic Messages API (`/v1/messages`) |
| Frontend | Vanilla HTML + CSS + JavaScript (zero dependencies) |
| Fonts | Google Fonts — Syne, DM Sans, DM Mono |

---

## 📊 Trust Score Formula

Each job is scored out of 100:

| Signal | Points |
|---|---|
| Company verified on LinkedIn / official site | +30 |
| Realistic salary range provided | +20 |
| Direct company career page link | +15 |
| Posted within last 7 days | +15 |
| Detailed, non-templated job description | +10 |
| Specific hiring manager or team mentioned | +10 |
| Generic templated description | −20 |
| Company not verifiable | −30 |

---

## 🗂 Output JSON Schema

The agent returns structured data in this format:

```json
{
  "jobs": [
    {
      "title": "Senior Software Engineer",
      "company": "Acme Corp",
      "location": "Bengaluru, India",
      "remote": false,
      "type": "full-time",
      "salary": "₹30L – ₹45L",
      "isNew": true,
      "postedDate": "2025-06-01",
      "source": "LinkedIn",
      "applyUrl": "https://...",
      "description": "...",
      "trustScore": 88,
      "validations": ["Company verified", "Salary validated", "Fresh posting"]
    }
  ],
  "eliminated": [
    {
      "title": "Work From Home Data Entry",
      "company": "Unknown",
      "source": "Indeed",
      "reason": "No company name, unrealistic salary claim, gmail apply address"
    }
  ],
  "sourcesChecked": 6,
  "searchQueries": ["senior software engineer bengaluru linkedin 2025", "..."]
}
```

---

## 👤 Author

**Sankar** — [github.com/svbsankar](https://github.com/svbsankar)

---

## 📄 License

MIT — free to use, modify, and distribute.
