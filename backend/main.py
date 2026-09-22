import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Account,
    AudienceRow,
    EmailAgent,
    EmailAgentCreate,
    EmailAgentUpdate,
    EmailDraft,
    EmailDraftUpdate,
)
from store import accounts, agents, drafts

app = FastAPI(title="Email agent take-home")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/accounts", response_model=list[Account])
def list_accounts() -> list[Account]:
    return accounts


@app.get("/agents", response_model=list[EmailAgent])
def list_agents() -> list[EmailAgent]:
    return list(agents.values())


@app.post("/agents", response_model=EmailAgent, status_code=201)
def create_agent(payload: EmailAgentCreate) -> EmailAgent:
    agent = EmailAgent(id=str(uuid.uuid4()), **payload.model_dump())
    agents[agent.id] = agent
    return agent


@app.get("/agents/{agent_id}", response_model=EmailAgent)
def get_agent(agent_id: str) -> EmailAgent:
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents[agent_id]


@app.patch("/agents/{agent_id}", response_model=EmailAgent)
def update_agent(agent_id: str, payload: EmailAgentUpdate) -> EmailAgent:
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    updated = agents[agent_id].model_copy(
        update=payload.model_dump(exclude_unset=True)
    )
    agents[agent_id] = updated
    return updated


@app.post("/agents/{agent_id}/evaluate", response_model=list[AudienceRow])
def evaluate_agent(agent_id: str) -> list[AudienceRow]:
    """Return accounts that match this agent's triggers + segment.

    Use only the structured rules. Do not call an LLM here.
    Each row should include `matched_rules` describing why it qualified.
    """
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    raise HTTPException(status_code=501, detail="TODO: implement evaluate")


@app.post("/agents/{agent_id}/execute", response_model=list[EmailDraft])
def execute_agent(agent_id: str) -> list[EmailDraft]:
    """Draft one email per matching account.

    Ground the model on a fact pack from the account + email_instructions.
    Do not invent missing facts. Isolate per-account failures.
    Do not create infinite duplicates on re-run.
    """
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    raise HTTPException(status_code=501, detail="TODO: implement execute")


@app.get("/agents/{agent_id}/emails", response_model=list[EmailDraft])
def list_emails(agent_id: str) -> list[EmailDraft]:
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return [d for d in drafts.values() if d.agent_id == agent_id]


@app.patch("/emails/{draft_id}", response_model=EmailDraft)
def update_email(draft_id: str, payload: EmailDraftUpdate) -> EmailDraft:
    if draft_id not in drafts:
        raise HTTPException(status_code=404, detail="Draft not found")
    updated = drafts[draft_id].model_copy(
        update=payload.model_dump(exclude_unset=True)
    )
    drafts[draft_id] = updated
    return updated
