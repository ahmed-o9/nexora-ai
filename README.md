# Nexora — AI Teacher

Nexora is a full-stack AI teaching system designed to help students **understand concepts rather than simply receive answers**.

A question is passed through a teaching-oriented backend that can generate structured explanations, examples, analogies, key points, and understanding checks. When appropriate, tools can provide verified results separately from the generated explanation.

## What Nexora currently provides

* Structured AI explanations
* Examples and analogies
* Key-point extraction
* Understanding checks
* Tool-grounded results
* Multiple LLM providers
* Provider fallback handling
* Browser-based text-to-speech
* React + TypeScript frontend
* FastAPI + Python backend
* Automated backend testing

## Architecture

```text
React + TypeScript
        │
        ▼
   FastAPI API
        │
        ▼
Teaching / Orchestration Layer
        │
        ▼
   Provider Router
     ┌───┼────┐
     ▼   ▼    ▼
 Gemini Groq Mock
```

The provider layer allows Nexora to avoid depending on a single model provider and provides fallback behavior when a provider is unavailable.

## Tech Stack

**Frontend**

* React
* TypeScript
* Vite
* Tailwind CSS

**Backend**

* Python
* FastAPI
* Pydantic
* SQLite

**AI / APIs**

* Google Gemini
* Groq
* OpenAI-compatible API patterns

**Testing & Engineering**

* Pytest
* Git
* GitHub

## Project Status

Nexora is an actively developing project.

The current version focuses on establishing a reliable teaching pipeline and a usable student-facing interface. Future development will expand the teaching engine, memory, tools, deployment, and interactive learning capabilities.
