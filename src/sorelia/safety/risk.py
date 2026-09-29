from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class RiskDecision:
    level: str
    reversible: bool
    requires_confirmation: bool
    reason: str

HIGH_RISK_HINTS = {"delete", "submit", "purchase", "pay", "send", "publish", "transfer"}
MODERATE_RISK_HINTS = {"overwrite", "rename", "move", "save"}

def classify_action(action: str, context: Dict | None = None) -> RiskDecision:
    text = action.lower()
    if any(x in text for x in HIGH_RISK_HINTS):
        return RiskDecision("high", False, True, "potential irreversible external side effect")
    if any(x in text for x in MODERATE_RISK_HINTS):
        return RiskDecision("moderate", True, False, "state-changing but usually reversible")
    return RiskDecision("safe", True, False, "no high-risk semantic trigger")
