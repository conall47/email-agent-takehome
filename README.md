# Email agent take-home

**Submit:** a fork or clone of this repo, with notes at the bottom of this file.

Build a **customer-success email agent**. A CSM sets **rules** (who to email) and **instructions** (what to say). The agent finds matching accounts, drafts a personalized email for each, and leaves those drafts for a human to review. Nothing is sent.

This is not a chatbot.

## How this is wired

Everything runs on **your laptop**. This API is a small FastAPI app in `backend/`. It does **not** talk to Dyle, Gmail, or any of our servers.

- Accounts come from `data/accounts.json` (a file in this repo).
- Agents and drafts are stored in memory in the API process.
- Your UI should call `http://localhost:8000` (see `/docs` once the server is up).
- The only thing that may call the internet is **you**, if you use an LLM for `execute`. No API key? Stub that function and still do evaluate + the UI.

## What you ship

A CSM should be able to:

1. Create and edit an agent in the UI (not only the seed agent).
2. Preview the audience — who matches, and why.
3. Generate drafts, then edit / approve / discard them.

**Evaluate is your code, not a model.** `email_instructions` are only for writing the email. If a fact is not on the account, the email must not invent it.

## What’s in this repo

| Path | What it is |
|------|------------|
| `data/accounts.json` | 30 accounts. Some fields are `null` or messy on purpose. |
| `backend/` | FastAPI. Accounts, agent CRUD, and draft PATCH already work. |
| `shared/types.ts` | Types that match the API. Copy them into your UI. |

`POST /agents/{id}/evaluate` and `POST /agents/{id}/execute` return **501 on purpose**. There is **no frontend** — scaffold one (React + TypeScript is closest to how we work) and point it at `http://localhost:8000`.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Python 3.10+. Docs at http://localhost:8000/docs. `GET /accounts` and `GET /agents` should work immediately.

Agents and drafts live **in memory**. A restart resets them; the seed agent `ag_renewal_watch` comes back. CORS is open for ports `5173` and `3000`.

## Backend work

Triggers and segment are structured fields on the agent (`shared/types.ts`). Triggers are metric conditions; the segment is a static filter (plan / ARR). You decide how they combine, what `DECREASES_BY` means, and what to do with `null`s — put that in your notes.

- **`evaluate`** — return matching accounts, each with `matched_rules`. No LLM.
- **`execute`** — one draft per match. Persist them on `store.drafts` so `GET /agents/{id}/emails` works. Re-running must not create infinite duplicates (skip, replace, or cooldown — pick one).

Bad LLM JSON must not 500 the batch. One bad account must not block the others. A couple of tests on evaluate are enough.

Any LLM provider is fine. No key? Stub generation behind an interface; still do evaluate and the UI for real.

## Out of scope

Auth, multi-tenant vendors, Gmail, scheduling, digests, voice, RAG, agent frameworks, pixel-perfect UI. Don’t replace the seed data or the existing CRUD unless you have a reason.

## Stretch

Natural language → structured triggers/segment. If the model proposes something you don’t support, still save a draft agent and show a warning.

## What we care about

- Rules pick the audience; the model only writes the email
- LLM output is treated as untrusted
- The UI is a review workflow, not a chat log
- Notes that are honest about gaps and what you’d do next

## Your notes

_How to run the UI, how to demo, design choices, what you’d do next._
