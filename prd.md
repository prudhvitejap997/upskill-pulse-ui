
1. Executive Summary

UpSkill Pulse is a self-serve, AI-powered learning assessment platform that empowers learners to evaluate their understanding of any subject using their own study materials. Users upload content, select topics and difficulty levels, and receive AI-generated MCQ assessments. Upon completion, the platform evaluates performance and returns detailed, explanation-rich solutions — closing the loop between learning and self-assessment.

The platform is designed as a hackathon MVP targeting students, self-learners, and working professionals who want to transform passive study material into active assessments — on demand.


2. Problem Statement

Learners today consume vast amounts of content — PDFs, notes, slides, and documents — but lack a structured way to self-assess comprehension. Existing quiz tools require manual question creation, and generic assessment platforms don't personalize uploaded material. There is a clear gap between:

- Content consumption (reading, watching, listening)
- Validated comprehension (structured, contextual, self-paced assessment)

UpSkill Pulse fills this gap by making content-to-assessment conversion instant, intelligent, and self-serve.


3. Goals & Success Metrics

Product Goals


Goal
Description
Democratize self-assessment
Any learner can generate a custom quiz from their own material in under 2 minutes
Personalize difficulty
Assessment difficulty adapts to user preference (Easy / Medium / Hard)
Close the feedback loop
Detailed solutions help learners understand what they got wrong and why
Enable habit formation
Simple UX encourages repeated use across learning sessions


MVP Success Metrics 


Goal
Description
Time from upload to quiz generation
< 60 seconds
MCQ accuracy relevance (user-rated)
≥ 80% relevance to uploaded content
Assessment completion rate
≥ 70% per session
Solution clarity rating
≥ 4/5 average



4. Target Users


Primary Persona — The Self-Learner
Who -  Students, exam aspirants, working professionals upskilling
Goal - Convert study notes/materials into practice assessments without manual effort
Pain Point - No time to create quizzes; generic tests don't match their material
Behavior - Uploads PDFs/notes, wants instant, targeted questions

Secondary Persona — The Trainer / Educator (Future Scope)

Who -  L&D professionals, corporate trainers
Goal - Quickly validate trainee comprehension on custom content
Integration Need -  LMS compatibility (Future Scope)



5. User Journey 
1. User visits UpSkill Pulse → Signs up / Logs in 
         ↓
2. User uploads study content (PDF, DOCX, TXT)
         ↓
3. User selects topics from auto-extracted suggestions (or types custom)
         ↓
4. User selects difficulty: Easy / Medium / Hard
         ↓
5. User selects number of questions (5 / 10 / 15 / 20)
         ↓
6. Platform generates MCQ assessment          ↓
7. User completes assessment and submits
         ↓
8. Platform evaluates responses → Score + Performance breakdown
         ↓
9. Platform displays detailed solutions for each question
         ↓
10. User reviews, retakes, or ends session


***

6. Core Features (MVP Scope)

6.1 User Authentication

Feature
Details
Sign Up / Log In
Email 
User Dashboard
View past assessments, scores, and history



6.2 Content Upload


Feature
Details
Supported Formats (MVP)
PDF, DOCX, TXT
Max File Size
10 MB per file
Max Files per Session
1 (MVP); 3 (v1.1)
Processing
File parsed → text extracted → stored in session context
Feedback
Upload progress indicator; success/error states



**Acceptance Criteria:**
- File uploads complete within 10 seconds for files ≤ 5 MB
- Text extraction retains semantic structure (headings, paragraphs)
- Unsupported format triggers clear error message with supported types listed
- Uploaded content is not stored permanently after session ends (privacy-first MVP)

***

6.3 Topic Selection


Attribute
Specification
Auto-extraction
NLP-based key topic identification from uploaded content
User Override
User can deselect auto-suggested topics or type custom topics
Max Topics
3 topics per assessment
Display Format
Checkbox multi-select with topic chips



**Acceptance Criteria:**
- System surfaces 3-8 auto-suggested topics within 15 seconds of upload
- User can add custom topics not in the auto-suggestion list
- At least 1 topic must be selected to proceed

***

6.4 Assessment Configuration


Parameter
Options
Difficulty Level
Easy / Medium / Hard (single select)
Number of Questions
5 / 10 / 15 / 20 (radio select)
Question Type (MVP)
MCQs only (4 options, 1 correct)


Difficulty Definitions


Level
Bloom's Taxonomy Alignment
Question Character
Format
Easy
Remember / Understand
Definition-recall, direct fact questions
MCQs
Medium
Apply / Analyze
Scenario-based, inference questions
MCQs
Hard
Evaluate / Create
Multi-step reasoning, edge cases, trade-offs
MCQs




**Acceptance Criteria:**
- Configuration screen clearly shows all 3 parameters
- Default: Medium difficulty, 10 questions
- User cannot proceed without selecting difficulty

***

6.5 MCQ Assessment Generation

Attribute
Specification
Engine
LLM-based generation (OpenAI GPT-4 / Gemini API)
Grounding
Questions strictly generated from uploaded content context
Format
4-option MCQ; exactly 1 correct answer per question
Rendering
Google Forms-style UI — one question per page OR all questions on single page (MVP: single page)
Distractor Quality
Distractors must be plausible and content-relevant (not random)
Latency Target
Question set generated within 30 seconds



**Acceptance Criteria:**
- All generated questions are traceable to uploaded content
- No duplicate questions in a single assessment
- Each question has exactly 4 answer options
- Questions are numbered sequentially
- User can navigate freely between questions before submitting



6.6 Assessment Submission & Evaluation


Attribute
Specification
Submission
User clicks "Submit Assessment" button
Evaluation
Automated scoring: 1 mark per correct answer, 0 for incorrect
Score Display
X/N correct, percentage score, performance tier label
Time-on-task with engagement depth — time spent, scroll depth, re-reads, and interaction frequency
Cumulative progress across sessions
Performance Tiers
Needs Work (< 40%), Getting There (40–69%), Proficient (70–84%), Mastery (≥ 85%)
Response Lock
Answers cannot be changed post-submission


**Acceptance Criteria:**
- Score calculated and displayed within 3 seconds of submission
- Performance tier label displayed prominently alongside score
- Breakdown shows correct/incorrect/unattempted count
- Breakdown shows engagement level analysis & Progress across Sessions
- User cannot resubmit the same assessment

***

6.7 Detailed Solutions


Attribute
Specification
Trigger
Auto-displayed after submission
Content per Question
Question text, user's selected answer, correct answer, explanation (2–5 sentences)
Source Grounding
Explanation references the uploaded content where applicable
Visual Indicator
Green tick for correct, red cross for incorrect answers
Format
Accordion or sequential card display


**Acceptance Criteria:**
- Every question has a solution explanation — no question left without context
- Explanations are distinct per question (not templated)
- User's chosen answer is clearly marked alongside the correct answer
- Explanations are readable at --text-base (16px) with comfortable line height

***

7. Information Architecture

UpSkill Pulse
├── /auth
│   ├── /login
│   ├── /dashboard          ← Past sessions, scores, quick-start CTA
├── /assess (new session)
│   ├── Step 1: Upload Content
│   ├── Step 2: Select Topics
│   ├── Step 3: Configure Assessment
│   └── Step 4: Take Assessment
└── /results/:session_id
    ├── Score Summary
    └── Detailed Solutions
    └── Detailed Feedback Report
```

***

8. Technical Architecture (MVP)
### Frontend
- **Framework:** React.js (Vite)
- **Styling:** Tailwind CSS
- **State Management:** React Context / Zustand
- **Assessment UI:** Custom form component (Forms-style rendering)

### Backend
- **Runtime:** Node.js / Python FastAPI
- **API:** REST
- **LLM Integration:** OpenAI GPT-4 API or Google Gemini Pro API
- **File Parsing:** PyMuPDF (PDF), python-docx (DOCX), plain text reader
- **NLP Topic Extraction:** spaCy / KeyBERT

### Data Storage (MVP — Minimal)
- **Session Data:** In-memory / Redis (ephemeral)
- **User Auth:** PostgreSQL (users table)
- **Assessment History:** PostgreSQL (assessments, responses tables)

### Security
- File uploads scanned for malicious content before parsing
- No permanent storage of uploaded file content
- HTTPS only; JWT token expiry: 24 hours

***

9. Non-Functional Requirements

Requirement
Target
Availability
95% uptime
Latency (Quiz generation)
< 30 seconds end-to-end
Latency (Page loads)
< 2 seconds
Security
No PII stored beyond email; files purged post-session




10. Future Scope (Post-Hackathon Roadmap)


Feature
Description
Audio File Support
Upload MP3/WAV lecture recordings; transcribed via Whisper API before assessment generation
URL / Link Ingestion
Paste a URL (article, blog, documentation page) as source content



Feature
Description
Subtopic Recommendations
AI-suggested subtopics to explore further based on wrong answers
Adaptive Difficulty
System suggests harder/easier next session based on historical scores




Feature
Description
LMS Integration
SCORM/xAPI-compatible exports for Moodle, Canvas, Cornerstone
Team / Cohort Mode
Trainers can assign assessments to groups; aggregate analytics
API Access
Programmatic assessment generation for third-party integrations


11. Constraints & Assumptions

Constraints
- LLM API rate limits cap concurrent assessment generations (GPT-4: 60 RPM)
- File parsing accuracy varies for heavily formatted PDFs (tables, equations)

Assumptions
- Uploaded content is in English (multilingual support is post-MVP)
- User understands that MCQ generation quality depends on the quality of uploaded content
- The platform is not intended to replace formal certification exams

***

12. Out of Scope (MVP)

- True/False, fill-in-the-blank, or subjective question types
- Real-time collaboration or group assessments
- Content editing or annotation within the platform
- Gamification (badges, leaderboards)
- Offline mode


***

 Future Considerations Questions

#
Question
Owner
Priority
1
Which LLM provider (OpenAI vs. Gemini)? Cost vs. quality trade-off for budget?
Tech 
High
2
Should session data persist for 7 days post-assessment (for review) or be purged immediately?
Product
High
3
Max questions cap at 20 or allow up to 30 for Hard difficulty?
Product
Medium
4
Should topic auto-extraction use a local model (KeyBERT) or LLM call? Latency vs. cost?
Tech 
Medium
5
Assessment retake policy — unlimited retakes or limit per session?
Product
Low




