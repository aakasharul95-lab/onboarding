"""
glossary.py — Role Glossary
=============================
Add technical terms that new hires need to understand quickly.
These appear in the "Good to Know → Role Glossary" tab.

Format:
  GLOSSARY["SPE"]["Term"] = "Plain English definition"
  GLOSSARY["SE"]["Term"]  = "Plain English definition"

TIPS:
  - Write definitions as if explaining to someone on their first week
  - Include practical context (when/how the term appears in daily work)
  - Keep each definition to 1–3 sentences maximum
"""

from typing import Dict

GLOSSARY: Dict[str, Dict[str, str]] = {

    # ── SPE Glossary ──────────────────────────────────────────────────────────
    "SPE": {
        "Reman": (
            "Remanufactured part — a used component stripped down and restored to "
            "original OEM specification. Often cheaper than new and preferred for "
            "sustainability unless the customer contract specifies new parts."
        ),
        "BOM": (
            "Bill of Materials — a structured list of every component needed to build "
            "or service a product. The starting point for any parts order."
        ),
        "Supersession": (
            "When a part number is replaced by a newer one due to a design change or "
            "discontinuation. Always check KOLA for the current active part number "
            "before ordering — the physical part may carry an old number."
        ),
        "Incoterms": (
            "International commercial terms (e.g. EXW, DDP, CIF) that define who pays "
            "for shipping, insurance, and import duties in a transaction. "
            "Relevant when ordering from overseas suppliers."
        ),
        "MOQ": (
            "Minimum Order Quantity — the smallest number of units a supplier will sell "
            "in a single order. Important for budgeting and avoiding dead stock."
        ),
        "Lead Time": (
            "The time between placing an order and receiving the parts at the warehouse. "
            "Critical for planning — always check lead time before committing to a customer ETA."
        ),
        "Dead Stock": (
            "Inventory that hasn't moved in 12+ months. SPEs review dead stock quarterly "
            "to identify write-off candidates and free up warehouse space."
        ),
        "Cross-Reference": (
            "The process of matching a competitor's or customer's part number to our "
            "equivalent in KOLA or GLOPPS. Common when a customer provides a third-party "
            "part number and expects us to source it."
        ),
        "MRP": (
            "Material Requirements Planning — an SAP process that automatically calculates "
            "what parts need to be ordered and when, based on demand forecasts and stock levels."
        ),
        "GRN": (
            "Goods Receipt Note — the document confirming that ordered parts have arrived "
            "at the warehouse and been checked against the Purchase Order."
        ),
    },

    # ── SE Glossary ───────────────────────────────────────────────────────────
    "SE": {
        "LOTO": (
            "Lock Out Tag Out — a mandatory safety procedure applied before working on any "
            "energised equipment. Physically isolates energy sources to prevent accidental "
            "start-up. Never skip it, regardless of time pressure."
        ),
        "ESR": (
            "Electronic Service Report — the digital record of every job you complete, "
            "filed in the ESR Tool. Must be submitted the same day. Late ESRs delay "
            "customer invoicing and are tracked by your manager."
        ),
        "Work Order": (
            "A formal job instruction issued from SAP Service Cloud. Contains the job "
            "scope, customer details, and time allocation. You must have a Work Order "
            "before starting any job — no exceptions."
        ),
        "SLA": (
            "Service Level Agreement — the contracted response and fix time promised to "
            "a customer. Breaching an SLA can result in financial penalties for the company."
        ),
        "Escalation": (
            "The process of notifying your tech lead or manager when a job exceeds your "
            "skill level, exceeds the SLA, or requires additional resources. "
            "Escalate early — do not wait until the job is overdue."
        ),
        "Warranty Claim": (
            "A request to replace a faulty part at no cost under the manufacturer's "
            "warranty. Requires a completed ESR and photo evidence of the defect. "
            "Raise via the ESR Tool and flag to your tech lead."
        ),
        "Timesheet": (
            "A daily log of hours worked against each Work Order, submitted via MOM. "
            "Must be completed before 6pm. Used for payroll and customer billing."
        ),
        "De-brief": (
            "A short end-of-day call or message to your manager summarising completed "
            "jobs, outstanding issues, and next-day priorities. Builds visibility and "
            "helps your manager plan resource allocation."
        ),
        "PPE": (
            "Personal Protective Equipment — safety gear required on site, including "
            "hard hat, safety boots, hi-vis vest, and gloves. Always check the site "
            "safety requirements before arriving."
        ),
        "RAMS": (
            "Risk Assessment and Method Statement — a document outlining the hazards "
            "of a job and the steps taken to mitigate them. Required before starting "
            "any non-routine or high-risk task."
        ),
    },

}