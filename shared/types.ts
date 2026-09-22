/** Shared shapes for the take-home. Backend Pydantic models mirror these. */

export type Plan = 'starter' | 'pro' | 'enterprise'

export interface Account {
  id: string
  name: string
  arr: number
  plan: Plan
  health_score: number | null
  usage_30d: number
  usage_prev_30d: number | null
  days_to_renewal: number
  open_tickets: number
  csm_owner: string
  recent_context: string[]
}

export type TriggerMetric = 'health_score' | 'usage' | 'days_to_renewal'
export type TriggerCondition = 'LT' | 'LTE' | 'GT' | 'GTE' | 'DECREASES_BY'
export type SegmentProperty = 'arr' | 'plan'
export type SegmentCondition = 'GTE' | 'LTE' | 'EQ' | 'IN'

export interface Trigger {
  metric: TriggerMetric
  condition: TriggerCondition
  value: number
}

export interface Segment {
  property: SegmentProperty
  condition: SegmentCondition
  value: number | Plan | Plan[]
}

export interface EmailAgent {
  id: string
  name: string
  is_active: boolean
  mode: 'DRAFT'
  email_instructions: string
  triggers: Trigger[]
  segment: Segment | null
}

export interface AudienceRow extends Account {
  matched_rules: string[]
}

export type DraftStatus = 'draft' | 'approved' | 'discarded'

export interface EmailDraft {
  id: string
  agent_id: string
  account_id: string
  subject: string
  body: string
  status: DraftStatus
  facts: Record<string, unknown>
}
