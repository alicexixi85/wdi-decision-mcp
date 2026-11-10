#!/usr/bin/env python3
"""WDI — Women's Decision Intelligence MCP (open source).

A zero-dependency MCP server (stdio) with deterministic tools for structuring
high-stakes career and life decisions: cash-runway math, evidence grading,
six-dimension option comparison and a reversibility check. All computation is
local; nothing is sent anywhere.

Decision-structuring aid only. Not legal, tax, financial, medical or mental
health advice.

Run:  python server.py
"""
from __future__ import annotations

import json
import sys

from mcp_stdio import StdioServer

VERSION = "1.0.0"
DISCLAIMER = ("Decision-structuring aid only. Not legal, tax, financial, medical or mental-health advice. "
              "For contracts, divorce/prenups, taxes, benefits or safety concerns, consult a qualified professional.")

DIMENSIONS = {
    "cash_runway": "Cash runway and a sole-name safety floor: how many months can you cover essential costs if income stops or drops?",
    "time_windows": "Irreversible time windows: vesting cliffs, visa or benefit deadlines, fertility or caregiving timelines, re-entry penalties.",
    "care_load": "Caregiving and unpaid labor: who carries childcare, eldercare and household load under each option, and what it costs in hours and income.",
    "safety_floor": "Health insurance, housing stability and personal safety: what is the minimum you must not drop below?",
    "control_rights": "Actual control rights: which assets, accounts and decisions are legally yours versus promised or jointly held?",
    "institutional_bridges": "Institutional bridges: leave policies, severance, unemployment benefits, part-time or internal-transfer options that make a change reversible.",
}
EVIDENCE_TIERS = {
    "KNOWN": "Verified in writing or by numbers you can check (contract, statement, offer letter, policy document).",
    "ASSUMED": "Reasonable belief based on a track record, but not verified.",
    "UNKNOWN": "You do not know yet; can be found out by asking or reading a document.",
    "SYNTHETIC": "A hope, projection or verbal promise with no evidence behind it.",
}
_TIER_HINTS = [
    ("KNOWN", ["contract", "signed", "statement", "offer letter", "in writing", "policy", "pay stub", "bank", "documented", "receipt"]),
    ("SYNTHETIC", ["promise", "will probably", "hope", "should be fine", "they said", "verbal", "someday", "might", "expect"]),
    ("ASSUMED", ["usually", "has always", "track record", "last year", "historically", "typically"]),
]


def calculate_runway(liquid_cash: float, monthly_essential_costs: float, monthly_income_after: float = 0.0,
                     extra_monthly_costs: float = 0.0, one_time_costs: float = 0.0, safety_floor_months: float = 6.0) -> dict:
    """Months of runway after a change (e.g. quitting, a pay cut, relocating)."""
    for name, v in (("liquid_cash", liquid_cash), ("monthly_essential_costs", monthly_essential_costs)):
        if v is None or v < 0:
            raise ValueError(f"{name} must be a non-negative number")
    burn = monthly_essential_costs + extra_monthly_costs - monthly_income_after
    usable = liquid_cash - one_time_costs
    floor_cash = safety_floor_months * (monthly_essential_costs + extra_monthly_costs)
    result = {
        "inputs": {"liquid_cash": liquid_cash, "monthly_essential_costs": monthly_essential_costs,
                   "monthly_income_after": monthly_income_after, "extra_monthly_costs": extra_monthly_costs,
                   "one_time_costs": one_time_costs, "safety_floor_months": safety_floor_months},
        "net_monthly_burn": round(burn, 2),
        "usable_cash_after_one_time_costs": round(usable, 2),
        "safety_floor_cash": round(floor_cash, 2),
    }
    if usable <= 0:
        result["runway_months"] = 0
        result["verdict"] = "One-time costs exceed liquid cash. The change is not funded as described."
    elif burn <= 0:
        result["runway_months"] = None
        result["verdict"] = "Income after the change covers essential costs; runway is not the binding constraint."
    else:
        months = usable / burn
        months_above_floor = (usable - floor_cash) / burn if usable > floor_cash else 0
        result["runway_months"] = round(months, 1)
        result["months_before_hitting_safety_floor"] = round(months_above_floor, 1)
        if usable < floor_cash:
            result["verdict"] = (f"Usable cash is below a {safety_floor_months:g}-month safety floor. "
                                 "Consider building the floor first or choosing a reversible version of the change.")
        else:
            result["verdict"] = f"About {months_above_floor:.1f} months of experimentation before touching the safety floor."
    result["assumptions_to_check"] = ["Health insurance cost after the change (e.g. COBRA or marketplace plans)",
                                      "Taxes on any severance or retirement withdrawals",
                                      "Unvested equity or bonuses forfeited by leaving"]
    result["disclaimer"] = DISCLAIMER
    return result


def grade_evidence(claims: list) -> dict:
    """Tag each claim with an evidence tier. Each item: string, or {claim, tier?, source?}."""
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims must be a non-empty list")
    graded = []
    for item in claims:
        if isinstance(item, str):
            item = {"claim": item}
        text = str(item.get("claim", "")).strip()
        tier = str(item.get("tier", "")).upper() or None
        basis = "provided"
        if tier not in EVIDENCE_TIERS:
            lowered = (text + " " + str(item.get("source", ""))).lower()
            tier, basis = "UNKNOWN", "default"
            for candidate, words in ([] if text.endswith("?") else _TIER_HINTS):
                if any(w in lowered for w in words):
                    tier, basis = candidate, "keyword heuristic (confirm manually)"
                    break
        graded.append({"claim": text, "tier": tier, "tier_meaning": EVIDENCE_TIERS[tier], "basis": basis,
                       "next_step": {"KNOWN": "Keep the document.",
                                     "ASSUMED": "Ask for it in writing or check the record.",
                                     "UNKNOWN": "Find out before deciding: who can answer this?",
                                     "SYNTHETIC": "Do not let the decision depend on this."}[tier]})
    counts = {t: sum(1 for g in graded if g["tier"] == t) for t in EVIDENCE_TIERS}
    weak = counts["UNKNOWN"] + counts["SYNTHETIC"]
    return {"graded": graded, "counts": counts,
            "warning": (f"{weak} of {len(graded)} claims are UNKNOWN or SYNTHETIC." if weak else None),
            "disclaimer": DISCLAIMER}


def compare_options(options: list, weights: dict | None = None) -> dict:
    """Score options 1-5 on the six dimensions (5 = best for you) and rank them."""
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError("Provide at least two options, each {name, scores: {dimension: 1-5}, reversible?}")
    weights = {k: float((weights or {}).get(k, 1.0)) for k in DIMENSIONS}
    total_w = sum(weights.values()) or 1.0
    rows = []
    for opt in options:
        scores = opt.get("scores") or {}
        missing = [d for d in DIMENSIONS if d not in scores]
        clean = {}
        for d in DIMENSIONS:
            v = scores.get(d)
            if v is not None:
                v = float(v)
                if not 1 <= v <= 5:
                    raise ValueError(f"Score for {d} in '{opt.get('name')}' must be 1-5")
                clean[d] = v
        scored_w = sum(weights[d] for d in clean) or 1.0
        weighted = sum(clean[d] * weights[d] for d in clean) / scored_w
        redlines = [d for d, v in clean.items() if v <= 1]
        rows.append({"name": opt.get("name", "unnamed"), "weighted_score_1_to_5": round(weighted, 2),
                     "redline_dimensions": redlines, "unscored_dimensions": missing,
                     "reversible": opt.get("reversible")})
    rows.sort(key=lambda r: (len(r["redline_dimensions"]) > 0, -r["weighted_score_1_to_5"]))
    return {"ranking": rows, "dimensions": DIMENSIONS, "weights_used": weights,
            "how_to_read": "Options with a score of 1 on any dimension are listed last regardless of average: a single redline "
                           "(e.g. losing health insurance) can outweigh strengths elsewhere. Prefer reversible options when scores are close.",
            "disclaimer": DISCLAIMER}


def six_dimension_checklist(decision: str = "") -> dict:
    return {"decision": decision or None,
            "questions": DIMENSIONS,
            "evidence_tiers": EVIDENCE_TIERS,
            "process": ["List 2-4 concrete options, including a reversible or partial version.",
                        "Answer each dimension per option and grade the evidence behind each answer.",
                        "Run the runway calculation for any option that reduces income.",
                        "Set a dated review point and a cash threshold that triggers your backup plan."],
            "disclaimer": DISCLAIMER}


NUM = {"type": "number"}
server = StdioServer(
    "wdi-decision-intelligence", VERSION,
    instructions="Deterministic tools for structuring high-stakes career and life decisions. Start with "
                 "six_dimension_checklist, then use calculate_runway, grade_evidence and compare_options. "
                 "Always pass along the disclaimer; refer legal, tax, medical and safety questions to professionals.")
server.tool("six_dimension_checklist",
            "Return the six-dimension decision checklist (cash runway, time windows, care load, safety floor, control rights, "
            "institutional bridges), the four evidence tiers and a step-by-step process.",
            {"type": "object", "properties": {"decision": {"type": "string", "description": "Optional one-line description of the decision"}}})(six_dimension_checklist)
server.tool("calculate_runway",
            "Compute months of cash runway after a change (quitting, pay cut, relocation, career break) and how long until a safety floor is reached.",
            {"type": "object", "properties": {
                "liquid_cash": {**NUM, "description": "Cash you can access without penalty"},
                "monthly_essential_costs": {**NUM, "description": "Essential monthly costs (housing, food, insurance, debt minimums)"},
                "monthly_income_after": {**NUM, "description": "Monthly income after the change (default 0)"},
                "extra_monthly_costs": {**NUM, "description": "New monthly costs caused by the change, e.g. self-paid health insurance"},
                "one_time_costs": {**NUM, "description": "One-time costs, e.g. moving, repaying a signing bonus"},
                "safety_floor_months": {**NUM, "description": "Months of essential costs to keep untouched (default 6)"}},
             "required": ["liquid_cash", "monthly_essential_costs"]})(calculate_runway)
server.tool("grade_evidence",
            "Tag each claim behind a decision as KNOWN, ASSUMED, UNKNOWN or SYNTHETIC and suggest the next step for each.",
            {"type": "object", "properties": {"claims": {"type": "array", "items": {"anyOf": [
                {"type": "string"},
                {"type": "object", "properties": {"claim": {"type": "string"}, "tier": {"type": "string", "enum": list(EVIDENCE_TIERS)},
                                                  "source": {"type": "string"}}, "required": ["claim"]}]}}},
             "required": ["claims"]})(grade_evidence)
server.tool("compare_options",
            "Rank 2+ options scored 1-5 on the six dimensions (5 = best for you), with optional weights; options with a redline (score 1) are ranked last.",
            {"type": "object", "properties": {
                "options": {"type": "array", "items": {"type": "object", "properties": {
                    "name": {"type": "string"},
                    "scores": {"type": "object", "properties": {d: {"type": "number", "minimum": 1, "maximum": 5} for d in DIMENSIONS}},
                    "reversible": {"type": "boolean"}}, "required": ["name", "scores"]}},
                "weights": {"type": "object", "properties": {d: {"type": "number", "minimum": 0} for d in DIMENSIONS}}},
             "required": ["options"]})(compare_options)


def main() -> None:
    server.serve()


if __name__ == "__main__":
    main()
