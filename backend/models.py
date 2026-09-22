from typing import Any, Literal

from pydantic import BaseModel, Field

Plan = Literal["starter", "pro", "enterprise"]
TriggerMetric = Literal["health_score", "usage", "days_to_renewal"]
TriggerCondition = Literal["LT", "LTE", "GT", "GTE", "DECREASES_BY"]
SegmentProperty = Literal["arr", "plan"]
SegmentCondition = Literal["GTE", "LTE", "EQ", "IN"]
DraftStatus = Literal["draft", "approved", "discarded"]


class Account(BaseModel):
    id: str
    name: str
    arr: float
    plan: Plan
    health_score: float | None
    usage_30d: float
    usage_prev_30d: float | None
    days_to_renewal: int
    open_tickets: int
    csm_owner: str
    recent_context: list[str]


class Trigger(BaseModel):
    metric: TriggerMetric
    condition: TriggerCondition
    value: float


class Segment(BaseModel):
    property: SegmentProperty
    condition: SegmentCondition
    value: float | Plan | list[Plan]


class EmailAgent(BaseModel):
    id: str
    name: str
    is_active: bool = True
    mode: Literal["DRAFT"] = "DRAFT"
    email_instructions: str = ""
    triggers: list[Trigger] = Field(default_factory=list)
    segment: Segment | None = None


class EmailAgentCreate(BaseModel):
    name: str
    is_active: bool = True
    email_instructions: str = ""
    triggers: list[Trigger]
    segment: Segment | None = None


class EmailAgentUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None
    email_instructions: str | None = None
    triggers: list[Trigger] | None = None
    segment: Segment | None = None


class AudienceRow(Account):
    matched_rules: list[str]


class EmailDraft(BaseModel):
    id: str
    agent_id: str
    account_id: str
    subject: str
    body: str
    status: DraftStatus = "draft"
    facts: dict[str, Any] = Field(default_factory=dict)


class EmailDraftUpdate(BaseModel):
    subject: str | None = None
    body: str | None = None
    status: DraftStatus | None = None
