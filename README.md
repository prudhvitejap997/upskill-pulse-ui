# Upskill Pulse

> **AI-powered technical skills assessment for developers.** Upload study material, pick topics, and generate precision technical questions with real-time performance tracking and downloadable PDF reports.

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

- **AI-generated quizzes** powered by Groq (Llama 3.3 70B) — with offline fallback
- **Six question types**: Code Output, Error Prediction, Concept, Syntax, Comparison, Behavior
- **Name-based user profiles** — each user has their own dashboard and session history
- **Per-question time tracking** with feedback (rushed / quick & accurate / slow but correct / needs study)
- **Downloadable PDF reports** with cover page, per-question analysis, and competitive evaluation
- **Dashboard** with topic performance, recent sessions, and question-type mastery
- **Dark / Light theme toggle** (persisted)
- **File upload** — PDF and TXT study material parsed for context

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML + CSS + JavaScript (no framework) |
| PDF Generation | jsPDF (CDN) |
| Backend | Python 3.11+ · Flask |
| AI Engine | **Groq API** — `llama-3.3-70b-versatile` |
| Offline fallback | Curated question bank (`question_bank.py`) |
| File Parsing | pypdf |
| Persistence | Browser `localStorage` (session history, theme, user name) |
| Production Server | Gunicorn (for Render/Heroku) |

---

## Installation & Usage

### Prerequisites

- Python 3.11 or newer
- A free Groq API key from [console.groq.com/keys](https://console.groq.com/keys) (optional — offline mode works without it)

### Local setup

```bash
git clone https://github.com/prudhvitejap997/upskill-pulse-ui.git
cd upskill-pulse-ui
pip install -r requirements.txt
```

### Run the server

**Option 1 — using `start.bat` (Windows, easiest):**
Double-click `start.bat`. Paste your Groq API key when prompted (or press Enter to use offline mode). The browser opens automatically at `http://localhost:3000`.

**Option 2 — manual:**
```bash
# Linux / macOS
export GROQ_API_KEY=gsk_your_key_here
python server.py

# Windows
set GROQ_API_KEY=gsk_your_key_here
python server.py
```

Then open `http://localhost:3000` in your browser.

### Using the app

1. **Enter your name** on the landing screen — this scopes your dashboard and session history.
2. **Dashboard** — see your past sessions, topic performance, and question-type mastery.
3. **Start New Quiz** — pick up to 2 topics (e.g. `Python`, `JavaScript`, `React`, `SQL`, `Git`, `Docker`), optionally upload up to 2 PDF/TXT files as study material, choose difficulty, set question count.
4. **Take the quiz** — track per-question time, navigate via the side palette, submit when done.
5. **View results** — score ring, weak-topic chips, per-question time feedback, question-type breakdown.
6. **Download PDF Report** — professional A4 report with performance tier and recommendations.

### Deploy to production

See [Render deployment](#deploying-to-render) below for a free permanent URL.

---

## Subscription Plans

Upskill Pulse is open-source and free for personal use. Organisations can upgrade for advanced features.

| Feature | **Free** | **Pro** ($9 / mo) | **Enterprise** (custom) |
|---|:---:|:---:|:---:|
| AI-generated quizzes | ✔ 20 / month | ✔ Unlimited | ✔ Unlimited |
| Question types (all 6) | ✔ | ✔ | ✔ |
| File upload (PDF / TXT) | 2 files / quiz | 5 files / quiz | Unlimited |
| Topics per quiz | 2 | 5 | Unlimited |
| Session history | 10 sessions | Unlimited | Unlimited |
| PDF performance report | ✔ | ✔ + custom branding | ✔ + custom branding |
| Dark / light theme | ✔ | ✔ | ✔ |
| Dashboard & analytics | Basic | Advanced + trends | Advanced + trends |
| Team accounts | — | — | ✔ |
| Custom question bank | — | — | ✔ |
| API access | — | — | ✔ |
| SSO (Google / Microsoft) | — | — | ✔ |
| SLA & priority support | Community | Email (48h) | Dedicated CSM |
| Export to LMS (Moodle / Canvas) | — | — | ✔ |

> **Note:** The open-source version in this repository is fully functional and equivalent to the **Free tier**. Pro and Enterprise tiers are available via [upskillpulse.io](https://upskillpulse.io) *(hypothetical — demo plans)*.

---

## Usage of the Platform

### Who uses Upskill Pulse?

- **Software engineers** preparing for technical interviews
- **Bootcamp students** reinforcing daily lessons with targeted assessments
- **Engineering managers** running team skill audits and onboarding quizzes
- **University instructors** generating practice exams from lecture notes
- **Self-taught developers** identifying knowledge gaps across a topic

### Real-world use cases

1. **Interview prep** — Upload your notes on a topic (Python async, React hooks, SQL joins) and get 20 hard questions. Use the time-tracking to identify topics where you hesitate.
2. **Team onboarding** — A manager uploads internal docs and generates a 15-question quiz for new hires. The PDF report goes in the onboarding packet.
3. **Self-study validation** — Read a chapter on Docker, take a 10-question quiz, check the dashboard to confirm mastery before moving on.
4. **Instructor-led assessment** — Upload lecture PDF, generate a quiz, share the results PDF with grading comments.

---

## Customer Details

### Target Customers

| Segment | Profile | Primary Need |
|---|---|---|
| **Individual Developers** | 1–5 YoE, interview-active | Quick skill check, realistic MCQs |
| **Coding Bootcamps** | 20–200 students per cohort | Per-topic assessments, progress reports |
| **Mid-market Tech Companies** | 50–500 engineers | Team skill audits, onboarding quizzes |
| **Engineering Managers** | 5–30 direct reports | Performance visibility, topic weaknesses |
| **University CS Programs** | 100+ students | Lecture-aligned practice exams |

### Contact & Support

- **Website:** [upskillpulse.io](https://upskillpulse.io) *(demo)*
- **Email:** `support@upskillpulse.io` *(demo)*
- **GitHub Issues:** [github.com/prudhvitejap997/upskill-pulse-ui/issues](https://github.com/prudhvitejap997/upskill-pulse-ui/issues)
- **Maintainer:** Prudhvi Teja P. — [@prudhvitejap997](https://github.com/prudhvitejap997)

### Customer Testimonials *(illustrative)*

> *"We replaced our 3-hour manual quiz-building process with Upskill Pulse. Onboarding-quiz turnaround dropped from a day to 10 minutes."*
> — **Priya S.**, Engineering Manager at a fintech startup

> *"The per-question time feedback nailed exactly where I was rushing. I fixed my pacing and cleared two senior interviews."*
> — **Daniel K.**, Backend Engineer

> *"Our bootcamp uses Upskill Pulse for weekly reinforcement. Students love the dashboard; instructors love the PDF reports."*
> — **Ananya M.**, Lead Instructor

---

## Deploying to Render

1. Fork or push this repo to your GitHub.
2. Sign up at [render.com](https://render.com) (free tier).
3. **New → Web Service** → connect the repo.
4. Configure:
   - **Runtime:** Python 3
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn server:app`
5. **Environment Variables** → add `GROQ_API_KEY` = your Groq key.
6. Click **Create Web Service**. You get `https://upskill-pulse-xxxx.onrender.com`.

> Free-tier services sleep after 15 min of inactivity; first request takes ~30s to warm up.

---

## Project Structure

```
upskill-pulse-ui/
├── index.html          # Complete frontend (HTML + CSS + JS inline)
├── server.py           # Flask backend with Groq + offline fallback
├── question_bank.py    # Curated MCQs for offline / fallback mode
├── requirements.txt    # Python dependencies
├── Procfile            # For Render / Heroku deployment
├── start.bat           # One-click local launcher (Windows)
├── .gitignore
└── README.md           # This file
```

---

## Roadmap

- [ ] Teams & shared dashboards (Pro)
- [ ] Export session history to CSV
- [ ] Spaced-repetition mode for missed questions
- [ ] GitHub OAuth login
- [ ] LMS integrations (Moodle, Canvas)
- [ ] Mobile-optimised quiz mode
- [ ] Cloud-synced sessions (optional account)

---

## Contributing

Contributions welcome! Please open an issue first to discuss major changes.

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit with clear messages
4. Open a pull request against `master`

---

## Privacy

We take your privacy seriously. Upskill Pulse is built on a **privacy-first** architecture — most data never leaves your machine.

### What data is collected

| Data | Where it's stored | Who can see it |
|---|---|---|
| Your name | Browser `localStorage` only | You |
| Quiz sessions (score, time, answers) | Browser `localStorage` only | You |
| Theme preference (dark / light) | Browser `localStorage` only | You |
| Uploaded PDF / TXT files | **In-memory only** — parsed for the duration of one request, then discarded. Never written to disk on the server. | Temporarily processed by Groq API |
| Question text sent to AI | Groq API (for quiz generation) | Groq's servers (see [Groq Privacy Policy](https://groq.com/privacy-policy/)) |

### What we do NOT do

- We **do not** create user accounts or require sign-up.
- We **do not** run analytics, tracking pixels, or third-party cookies.
- We **do not** log or store your uploaded files on the server — they are parsed in memory and discarded immediately after the quiz is generated.
- We **do not** sell or share any data with advertisers.
- We **do not** send your personal information to any service other than Groq (for AI generation).

### Third-party services

- **Groq API** — When Groq mode is enabled, the content of your uploaded files and topic text is sent to Groq's servers to generate quiz questions. Groq processes this data per their [Terms of Service](https://groq.com/terms-of-use/) and [Privacy Policy](https://groq.com/privacy-policy/). Per Groq's policy, API data is **not used for model training** on their free tier.
- **jsPDF (CDN)** — Loaded from `cdnjs.cloudflare.com` to generate your PDF report client-side. No data is sent to Cloudflare beyond the standard CDN request.

### Clearing your data

To clear all locally stored data (sessions, name, theme), open your browser DevTools → **Application** tab → **Local Storage** → delete keys prefixed with `upskill_`. Alternatively, use your browser's "Clear site data" option.

### Offline mode = zero external requests

If you run the app without a `GROQ_API_KEY`, the server falls back to the built-in question bank (`question_bank.py`). In this mode, **no data ever leaves your machine** — not even to Groq.

### Data retention

- Uploaded files: **not retained** (in-memory only, dropped after each request).
- Session history: stored in your browser indefinitely until you clear it. Last 200 sessions kept per browser.
- Server logs: standard Flask request logs (IP, path, status) only — no request body.

### GDPR / CCPA

Because we don't collect personal data server-side, no data-subject rights request is needed. If you deploy this project commercially, you are responsible for adding your own privacy notice and compliance controls.

---

## License

**MIT License** © 2026 Prudhvi Teja P.

```
Copyright (c) 2026 Prudhvi Teja P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Third-party licenses

This project bundles and depends on the following open-source components:

| Library | License | Purpose |
|---|---|---|
| Flask | BSD-3-Clause | Web framework |
| pypdf | BSD-3-Clause | PDF text extraction |
| requests | Apache 2.0 | HTTP client (Groq API calls) |
| gunicorn | MIT | Production WSGI server |
| jsPDF | MIT | Client-side PDF generation |

### Commercial use

You are free to use, modify, and deploy Upskill Pulse commercially under the MIT License. If you distribute a modified version, please include this license notice and credit the original project.

For commercial licensing of the **Pro** or **Enterprise** tiers (with support, custom question banks, SSO, LMS integration, etc.), contact `licensing@upskillpulse.io` *(demo)*.
