<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-hero-dark.svg">
  <img alt="Nexora AI learning engine" src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-hero-light.svg" width="100%">
</picture>

<a href="https://github.com/ahmed-o9/nexora-ai"><img src="https://img.shields.io/github/stars/ahmed-o9/nexora-ai?style=for-the-badge&label=STARS"></a>
<a href="https://github.com/ahmed-o9/nexora-ai"><img src="https://img.shields.io/github/last-commit/ahmed-o9/nexora-ai?style=for-the-badge&label=UPDATED"></a>
<a href="https://github.com/ahmed-o9/nexora-ai"><img src="https://img.shields.io/github/license/ahmed-o9/nexora-ai?style=for-the-badge&label=LICENSE"></a>

</div>

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-engine-dark.svg">
  <img alt="Nexora orchestration architecture" src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-engine-light.svg" width="100%">
</picture>

</div>

## THE SYSTEM

Nexora is an AI learning system built around an orchestration layer rather than a single chat prompt. A learning request can be routed through deterministic tools, retrieval, memory, visual resources and teaching behavior before the final response is produced.

```text
QUESTION
   ↓
INTENT / ROUTING
   ↓
ORCHESTRATOR
   ├── MEMORY
   ├── RAG / DOCUMENT CONTEXT
   ├── DETERMINISTIC TOOLS
   ├── WEB / IMAGE RESOURCES
   └── MODEL PROVIDERS
   ↓
TEACHER
   ↓
GROUNDED RESPONSE
```

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-arcade-dark.svg">
  <img alt="Nexora learning modes" src="https://raw.githubusercontent.com/ahmed-o9/nexora-ai/main/.github/assets/nexora-arcade-light.svg" width="100%">
</picture>

</div>

## CAPABILITIES

| Layer | Role |
|---|---|
| **Orchestration** | Coordinates routing, planning, tools and response synthesis |
| **Teaching** | Adapts explanations to beginner, exam, interview, Socratic and research-style interaction |
| **Grounding** | Uses deterministic computation, retrieval and external resources when appropriate |
| **Memory** | Maintains session and learning context |
| **Visual learning** | Supports image-oriented explanations and visual resources |
| **Documents** | Provides document/RAG workflows |
| **API** | FastAPI backend with modular routes and services |
| **Frontend** | Interactive web interface |

## ENGINEERING MAP

```text
                           ┌─────────────────┐
                           │      USER       │
                           └────────┬────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   TEACH REQUEST     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
             ┌────────────┐                 ┌────────────┐
             │   ROUTER   │                 │   MEMORY   │
             └─────┬──────┘                 └─────┬──────┘
                   └──────────────┬───────────────┘
                                  ▼
                        ┌──────────────────┐
                        │  ORCHESTRATOR    │
                        └────────┬─────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            ▼                    ▼                    ▼
       ┌──────────┐         ┌──────────┐         ┌──────────┐
       │   TOOLS  │         │   RAG    │         │  IMAGES  │
       └────┬─────┘         └────┬─────┘         └────┬─────┘
            └────────────────────┼────────────────────┘
                                 ▼
                         ┌────────────────┐
                         │     TEACHER    │
                         └───────┬────────┘
                                 ▼
                         ┌────────────────┐
                         │    RESPONSE    │
                         └────────────────┘
```

## BUILT WITH

<div align="center">

`Python` · `FastAPI` · `TypeScript` · `React` · `Vite` · `SQLite` · `RAG` · `LLM APIs`

### BUILD · LEARN · EXPLORE

<a href="https://github.com/ahmed-o9/nexora-ai">Repository</a>

</div>
