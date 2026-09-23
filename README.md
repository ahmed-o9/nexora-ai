<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-dark.svg">
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-light.svg">
    <img
      src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-light.svg"
      alt="Nexora AI Teacher"
      width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/ahmed-o9/nexora-ai">
    <img src="https://img.shields.io/github/stars/ahmed-o9/nexora-ai?style=for-the-badge&label=STARS&color=00ff9c&labelColor=050505">
  </a>
  <a href="https://github.com/ahmed-o9/nexora-ai">
    <img src="https://img.shields.io/github/last-commit/ahmed-o9/nexora-ai?style=for-the-badge&label=UPDATED&color=00ff9c&labelColor=050505">
  </a>
  <img src="https://img.shields.io/badge/AI-TEACHING-00ff9c?style=for-the-badge&labelColor=050505">
  <img src="https://img.shields.io/badge/STATUS-ACTIVE-00ff9c?style=for-the-badge&labelColor=050505">
</p>

<p align="center">

<a href="https://github.com/ahmed-o9/nexora-ai">
  <img src="https://img.shields.io/badge/SOURCE_CODE-050505?style=for-the-badge&logo=github&logoColor=00ff9c">
</a>

<a href="https://nexora-ai.in">
  <img src="https://img.shields.io/badge/LIVE_DEMO-050505?style=for-the-badge&logo=googlechrome&logoColor=00ff9c">
</a>

<a href="https://nexora-ai.in/docs">
  <img src="https://img.shields.io/badge/API-050505?style=for-the-badge&logo=fastapi&logoColor=00ff9c">
</a>

</p>

---

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/engine-dark.svg">
    <img
      src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/engine-light.svg"
      alt="Nexora Engine"
      width="100%">
  </picture>
</p>

---

## `NEXORA`

**Nexora is an AI teaching engine that transforms questions into structured learning experiences.**

Instead of simply returning an answer, Nexora is designed to:

```text
QUESTION
   │
   ▼
UNDERSTAND
   │
   ▼
PLAN
   │
   ├─────────────┐
   ▼             ▼
TOOLS           KNOWLEDGE
   │             │
   └──────┬──────┘
          ▼
       TEACH
          │
          ▼
      VISUALIZE
          │
          ▼
       PRACTICE
          │
          ▼
        LEARN
```

---

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/architecture-dark.svg">
    <img
      src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/architecture-light.svg"
      alt="Nexora Architecture"
      width="100%">
  </picture>
</p>

---

## `CAPABILITIES`

| SYSTEM            | PURPOSE                    |
| ----------------- | -------------------------- |
| 🧠 Teacher Engine | Structured explanations    |
| ⚙️ Orchestrator   | Multi-step reasoning flow  |
| 🔧 Tool Router    | Selects appropriate tools  |
| 📐 Calculator     | Deterministic calculations |
| 🔎 Search         | Knowledge retrieval        |
| 🖼️ Image Search  | Visual learning            |
| 📚 RAG            | Document-grounded answers  |
| 💾 Memory         | Session / learner context  |
| 📝 Quiz Engine    | Active recall              |
| 🎤 Voice          | Voice-oriented interaction |

---

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/terminal-dark.svg">
    <img
      src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/terminal-light.svg"
      alt="Nexora Terminal"
      width="100%">
  </picture>
</p>

---

## `TECHNOLOGY`

<p align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,typescript,react,javascript,html,css,sqlite&theme=dark" />

</p>

```text
FRONTEND
    └── React / TypeScript

BACKEND
    └── FastAPI / Python

AI
    ├── Gemini
    └── Groq

INTELLIGENCE
    ├── Orchestration
    ├── RAG
    ├── Memory
    └── Tool Routing

TOOLS
    ├── Calculator
    ├── Search
    ├── Images
    └── Documents
```

---

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/pipeline-dark.svg">
    <img
      src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/pipeline-light.svg"
      alt="Nexora Learning Pipeline"
      width="100%">
  </picture>
</p>

---

## `PROJECT STRUCTURE`

```text
nexora-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── engine/
│   │   ├── tools/
│   │   └── ...
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
│
├── .github/
│   └── assets/
│       ├── nexora-dark.svg
│       ├── nexora-light.svg
│       ├── engine-dark.svg
│       ├── engine-light.svg
│       ├── architecture-dark.svg
│       ├── architecture-light.svg
│       ├── terminal-dark.svg
│       ├── terminal-light.svg
│       ├── pipeline-dark.svg
│       └── pipeline-light.svg
│
├── CNAME
└── README.md
```

---

## `API`

### `POST /api/teach`

```json
{
  "question": "Explain electromagnetic induction",
  "student_id": "student-001",
  "mode": "learn",
  "level": "beginner"
}
```

Nexora processes the request through its teaching pipeline and produces a structured learning response.

---

## `MODES`

```text
LEARN
BEGINNER
EXAM
INTERVIEW
SOCRATIC
RESEARCH
QUIZ
REVISE
```

---

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-dark.svg">
    <img
      src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-light.svg"
      alt="Nexora"
      width="100%">
  </picture>
</p>

---

## `ROADMAP`

```text
[✓] Core AI teaching engine
[✓] FastAPI backend
[✓] React frontend
[✓] Tool routing
[✓] Deterministic calculation
[✓] Memory foundation
[✓] RAG foundation
[✓] Visual learning foundation

[ ] Production deployment
[ ] Advanced voice interaction
[ ] Interactive diagrams
[ ] Learning analytics
[ ] Mobile client
```

---

## `RUN LOCALLY`

```bash
git clone https://github.com/ahmed-o9/nexora-ai.git

cd nexora-ai
```

### Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install
npm run dev
```

---

<p align="center">

<b>NEXORA // AI TEACHER</b>

<br>

<sub>Understand. Reason. Visualize. Teach.</sub>

<br><br>

<a href="https://github.com/ahmed-o9/nexora-ai">
  <img src="https://img.shields.io/badge/BUILDING_THE_FUTURE_OF_LEARNING-050505?style=for-the-badge&color=00ff9c">
</a>

</p>

