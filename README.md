# `NEXORA // AI TEACHER`

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=28&duration=2500&pause=800&color=00FF9C&center=true&vCenter=true&width=800&lines=NEXORA+%7C+AI+TEACHER;ASK+%E2%86%92+UNDERSTAND+%E2%86%92+VISUALIZE+%E2%86%92+MASTER;INTELLIGENT+LEARNING+ENGINE;TOOLS+%2B+MEMORY+%2B+RAG+%2B+AI" alt="Nexora animated typing" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/STATUS-ACTIVE-00ff9c?style=for-the-badge&labelColor=050505" />
  <img src="https://img.shields.io/badge/ENGINE-FASTAPI-00ff9c?style=for-the-badge&labelColor=050505" />
  <img src="https://img.shields.io/badge/AI-ORCHESTRATED-00ff9c?style=for-the-badge&labelColor=050505" />
  <img src="https://img.shields.io/badge/PROJECT-NEXORA-00ff9c?style=for-the-badge&labelColor=050505" />
</p>

<p align="center">
  <b>⚡ An AI teacher designed to explain, visualize, remember and adapt.</b>
</p>

---

```text
┌──────────────────────────────────────────────────────────────────────┐
│  NEXORA TERMINAL :: LEARNING INTELLIGENCE SYSTEM                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  $ nexora --boot                                                     │
│                                                                      │
│  [✓] Initializing orchestration engine                              │
│  [✓] Loading teacher engine                                          │
│  [✓] Loading memory subsystem                                        │
│  [✓] Loading RAG pipeline                                            │
│  [✓] Registering intelligent tools                                   │
│  [✓] Initializing visual reasoning                                   │
│                                                                      │
│  SYSTEM STATUS: ONLINE                                               │
│                                                                      │
│  > Ask anything.                                                     │
│  > Nexora figures out how to teach it.                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## `> WHAT_IS_NEXORA`

**Nexora** is an AI-powered teaching system built around one idea:

> **Don't just give the answer. Teach the student how to understand it.**

Instead of treating every question as a simple chatbot request, Nexora can route a problem through different capabilities such as:

```text
                 ┌──────────────────┐
                 │     STUDENT       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    NEXORA UI     │
                 └────────┬─────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │     ORCHESTRATOR       │
              └───────────┬────────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
     ┌─────────┐    ┌──────────┐    ┌──────────┐
     │ TEACHER │    │   TOOLS  │    │  MEMORY  │
     └────┬────┘    └────┬─────┘    └────┬─────┘
          │              │               │
          │        ┌─────┼─────┐         │
          │        ▼     ▼     ▼         │
          │      Math  Search  Images     │
          │        │     │      │         │
          └────────┴─────┴──────┴─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  TEACH + VISUAL  │
                 │  + PRACTICE      │
                 └──────────────────┘
```

---

## `> CORE_CAPABILITIES`

<table>
<tr>
<td width="50%">

### `01 // ADAPTIVE TEACHING`

Nexora can adapt explanations according to the learner's selected level and learning mode.

```text
BEGINNER
   ↓
CONCEPT
   ↓
INTUITION
   ↓
EXAMPLE
   ↓
PRACTICE
```

</td>

<td width="50%">

### `02 // TOOL GROUNDING`

Questions can be routed to deterministic tools when appropriate.

```text
Math
Search
Images
Code
RAG
Memory
```

</td>
</tr>

<tr>
<td>

### `03 // VISUAL LEARNING`

Complex concepts can be supported with diagrams and visual references.

```text
QUESTION
   ↓
CONCEPT
   ↓
VISUAL
   ↓
EXPLANATION
```

</td>

<td>

### `04 // MEMORY`

Nexora can maintain learning/session context instead of treating every interaction as isolated.

```text
STUDENT
   ↓
SESSION
   ↓
MEMORY
   ↓
PERSONALIZED RESPONSE
```

</td>
</tr>
</table>

---

## `> THE_NEXORA_LOOP`

```text
             ┌──────────────────────┐
             │       QUESTION       │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │     UNDERSTAND       │
             │       INTENT         │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │       PLAN           │
             │   TEACHING PATH      │
             └──────────┬───────────┘
                        ↓
          ┌─────────────┴──────────────┐
          │                            │
          ▼                            ▼
   ┌──────────────┐             ┌──────────────┐
   │   TOOL USE   │             │  KNOWLEDGE   │
   │              │             │    / RAG     │
   └──────┬───────┘             └──────┬───────┘
          │                            │
          └─────────────┬──────────────┘
                        ↓
             ┌──────────────────────┐
             │       TEACH          │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │      VISUALIZE       │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │       PRACTICE       │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │       MEMORY         │
             └──────────────────────┘
```

---

## `> LIVE_DEMO`

### `Ask Nexora`

```text
┌──────────────────────────────────────────────────────────────┐
│ USER                                                         │
├──────────────────────────────────────────────────────────────┤
│ Explain how a transformer works                               │
└───────────────────────────────┬──────────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────┐
│ NEXORA                                                       │
├──────────────────────────────────────────────────────────────┤
│ Analysing question...                                        │
│                                                              │
│ [✓] Identify concept                                         │
│ [✓] Select teaching strategy                                 │
│ [✓] Retrieve supporting knowledge                             │
│ [✓] Generate visual explanation                              │
│ [✓] Build beginner-friendly response                         │
│                                                              │
│ → Transformer consists of:                                   │
│   • Primary winding                                          │
│   • Magnetic core                                            │
│   • Secondary winding                                        │
│                                                              │
│ → Energy is transferred through electromagnetic induction.   │
└──────────────────────────────────────────────────────────────┘
```

### `REAL_UI_PREVIEW`

> Replace the image below with an actual screenshot/GIF of your Nexora interface.

```html
<p align="center">
  <img src="./assets/nexora-demo.gif" width="900" alt="Nexora live demo">
</p>
```

---

## `> FEATURE_MATRIX`

| Module            | Capability                            |
| ----------------- | ------------------------------------- |
| 🧠 Teacher Engine | Adaptive explanations                 |
| ⚙️ Orchestrator   | Multi-step task routing               |
| 🔧 Tool Router    | Selects appropriate tools             |
| 📐 Calculator     | Deterministic mathematical operations |
| 🔎 Search         | External knowledge retrieval          |
| 🖼️ Image Search  | Visual learning support               |
| 📚 RAG            | Document-based knowledge              |
| 💾 Memory         | Persistent learning/session context   |
| 📝 Quiz Engine    | Practice and assessment               |
| 🔌 API            | FastAPI backend                       |
| 🌐 Web UI         | Interactive learning interface        |
| 🎤 Voice          | Voice-oriented learning workflow      |

---

## `> MODES`

```text
┌─────────────────────────────────────────────────────────┐
│                   NEXORA MODES                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [LEARN]       Understand from fundamentals             │
│  [BEGINNER]    Zero-knowledge explanations              │
│  [EXAM]        Exam-oriented learning                   │
│  [INTERVIEW]   Technical interview preparation          │
│  [SOCRATIC]    Guided discovery                         │
│  [RESEARCH]    Deeper technical exploration             │
│  [QUIZ]        Active recall and assessment              │
│  [REVISE]      Rapid revision                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## `> TECH_STACK`

<p align="center">

<img src="https://img.shields.io/badge/Python-050505?style=for-the-badge&logo=python&logoColor=00ff9c" />
<img src="https://img.shields.io/badge/FastAPI-050505?style=for-the-badge&logo=fastapi&logoColor=00ff9c" />
<img src="https://img.shields.io/badge/JavaScript-050505?style=for-the-badge&logo=javascript&logoColor=00ff9c" />
<img src="https://img.shields.io/badge/HTML5-050505?style=for-the-badge&logo=html5&logoColor=00ff9c" />
<img src="https://img.shields.io/badge/CSS3-050505?style=for-the-badge&logo=css3&logoColor=00ff9c" />
<img src="https://img.shields.io/badge/SQLite-050505?style=for-the-badge&logo=sqlite&logoColor=00ff9c" />

</p>

```text
┌──────────────────────────────────────────────────────┐
│                   NEXORA STACK                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  FRONTEND        →  Web UI                           │
│  BACKEND         →  FastAPI                          │
│  ENGINE          →  Python orchestration             │
│  MEMORY          →  SQLite / session layer           │
│  RAG             →  Retrieval pipeline               │
│  TOOLS           →  Search / Math / Images / Code    │
│  AI              →  Pluggable model providers       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## `> ARCHITECTURE`

```text
                           NEXORA
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
        ┌───────────┐                 ┌───────────┐
        │ FRONTEND  │                 │   API     │
        └─────┬─────┘                 └─────┬─────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    └────────┬────────┘
                             │
              ┌──────────────┼───────────────┐
              │              │               │
              ▼              ▼               ▼
         ┌─────────┐    ┌─────────┐     ┌─────────┐
         │ TEACHER │    │  TOOLS  │     │ MEMORY  │
         └────┬────┘    └────┬────┘     └────┬────┘
              │              │               │
              │        ┌─────┼──────┐        │
              │        │     │      │        │
              │        ▼     ▼      ▼        │
              │      Math  Search  Image     │
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌─────────────────┐
                    │  RESPONSE       │
                    │  + VISUALS      │
                    │  + PRACTICE     │
                    └─────────────────┘
```

---

## `> PROJECT_STRUCTURE`

```text
NEXORA/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── engine/
│   │   ├── tools/
│   │   └── models/
│   │
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   └── ...
│
├── assets/
│   ├── nexora-demo.gif
│   ├── architecture.svg
│   └── screenshots/
│
└── README.md
```

---

## `> QUICK_START`

```bash
# clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# enter
cd YOUR_REPOSITORY

# backend
cd backend

# create environment
python -m venv .venv

# activate — Windows
.venv\Scripts\activate

# install
pip install -r requirements.txt

# run
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

---

## `> API`

### `POST /api/teach`

```json
{
  "question": "Explain Kirchhoff's voltage law",
  "student_id": "student-001",
  "mode": "learn",
  "level": "beginner"
}
```

### Response

```json
{
  "answer": "Kirchhoff's Voltage Law states...",
  "visuals": [],
  "tools_used": [],
  "mode": "learn"
}
```

---

## `> ENGINE_FLOW`

```text
REQUEST
   │
   ▼
┌────────────────┐
│ REQUEST PARSER │
└───────┬────────┘
        ▼
┌────────────────┐
│ INTENT / PLAN  │
└───────┬────────┘
        ▼
┌────────────────┐
│ TOOL ROUTER    │
└───────┬────────┘
        │
   ┌────┴─────┐
   ▼          ▼
 TOOLS       RAG
   │          │
   └────┬─────┘
        ▼
┌────────────────┐
│ TEACHER ENGINE │
└───────┬────────┘
        ▼
┌────────────────┐
│ RESPONSE       │
│ + VISUALS      │
│ + MEMORY       │
└────────────────┘
```

---

## `> ROADMAP`

```text
[✓] Core FastAPI backend
[✓] Orchestration layer
[✓] Tool routing
[✓] Deterministic calculation tools
[✓] Memory/session foundation
[✓] RAG foundation
[✓] Visual search foundation

[ ] Production deployment
[ ] Advanced voice interaction
[ ] Real-time teaching interface
[ ] Interactive diagrams
[ ] Expanded document intelligence
[ ] Personal learning analytics
[ ] Mobile client
```

---

## `> DEMO_GALLERY`

<p align="center">
  <img src="./assets/screenshots/home.png" width="43%" alt="Nexora Home">
  <img src="./assets/screenshots/teacher.png" width="43%" alt="Nexora Teacher">
</p>

<p align="center">
  <img src="./assets/screenshots/tools.png" width="43%" alt="Nexora Tools">
  <img src="./assets/screenshots/visual.png" width="43%" alt="Nexora Visual Learning">
</p>

---

## `> WHY_NEXORA`

```text
Traditional chatbot
        │
        ▼
    QUESTION
        │
        ▼
     ANSWER


NEXORA
        │
        ▼
    QUESTION
        │
        ▼
   UNDERSTAND
        │
        ▼
      PLAN
        │
        ├──────► SEARCH
        ├──────► CALCULATE
        ├──────► RETRIEVE
        ├──────► VISUALIZE
        └──────► REMEMBER
        │
        ▼
      TEACH
        │
        ▼
     PRACTICE
        │
        ▼
      MASTER
```

---

## `> SECURITY / DESIGN`

```text
┌────────────────────────────────────────────┐
│ PRINCIPLES                                 │
├────────────────────────────────────────────┤
│                                            │
│  • Deterministic tools where appropriate   │
│  • Modular provider architecture           │
│  • Separated frontend / backend             │
│  • Explicit tool routing                    │
│  • Session-aware architecture               │
│  • Extensible learning modes                │
│                                            │
└────────────────────────────────────────────┘
```

---

## `> CONNECT`

<p align="center">

<a href="https://github.com/YOUR_USERNAME">
<img src="https://img.shields.io/badge/GITHUB-000000?style=for-the-badge&logo=github&logoColor=00ff9c"/>
</a>

<a href="https://YOUR-LIVE-DEMO-URL">
<img src="https://img.shields.io/badge/LIVE_DEMO-000000?style=for-the-badge&logo=vercel&logoColor=00ff9c"/>
</a>

<a href="https://YOUR-API-URL/docs">
<img src="https://img.shields.io/badge/API_DOCS-000000?style=for-the-badge&logo=fastapi&logoColor=00ff9c"/>
</a>

</p>

---

```text
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   > SYSTEM MESSAGE                                      │
│                                                          │
│   Nexora is being engineered as an AI learning system   │
│   where intelligence is not limited to generating text.  │
│                                                          │
│   UNDERSTAND.                                           │
│   REASON.                                               │
│   VISUALIZE.                                            │
│   TEACH.                                                │
│   ADAPT.                                                │
│                                                          │
│   $ ./nexora --continue                                 │
│                                                          │
│   ████████████████████████████████████  ONLINE          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

<p align="center">
  <sub>Built with curiosity, engineering and too many terminal windows.</sub>
</p>
