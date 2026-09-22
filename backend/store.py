import json
from pathlib import Path

from models import Account, EmailAgent, EmailDraft

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "accounts.json"


def load_accounts() -> list[Account]:
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return [Account.model_validate(row) for row in raw]


accounts: list[Account] = load_accounts()
# In-memory only — gone when the server restarts. That is expected.
agents: dict[str, EmailAgent] = {}
drafts: dict[str, EmailDraft] = {}

# One example agent so GET /agents isn't empty on first boot.
# Evaluate / execute are still yours to implement.
_seed = EmailAgent(
    id="ag_renewal_watch",
    name="Renewal watch",
    email_instructions=(
        "Write a short, specific email from the assigned CSM. "
        "Only use the facts provided. If a fact is missing, do not invent it. "
        "Offer a 20-minute check-in, not a discount."
    ),
    triggers=[
        {"metric": "health_score", "condition": "LT", "value": 50},
        {"metric": "days_to_renewal", "condition": "LTE", "value": 45},
    ],
    segment={"property": "plan", "condition": "IN", "value": ["pro", "enterprise"]},
)
agents[_seed.id] = _seed
