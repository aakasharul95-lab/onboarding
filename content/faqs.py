"""
faqs.py — Frequently Asked Questions
======================================
Real questions from new hires. Add new ones as they come up in onboarding sessions.

Structure:
  FAQS["Common"]  → shown to all roles
  FAQS["SPE"]     → shown only to Spare Parts Engineers
  FAQS["SE"]      → shown only to Service Engineers

Each FAQ is a dict:
  "q" : the question (as a new hire would ask it)
  "a" : the answer (practical, direct — no corporate fluff)

TIPS:
  - Write answers in second-person ("you", "your") — feels more personal
  - Include who to contact or what system to use where relevant
  - If a question keeps coming up in onboarding, it belongs here
"""

from typing import Dict, List

FAQS: Dict[str, List[Dict[str, str]]] = {

    # ── Common (all roles) ────────────────────────────────────────────────────
    "Common": [
        {
            "q": "I haven't received my laptop yet — what do I do?",
            "a": (
                "Contact IT Helpdesk (Ext. 4040) immediately. Escalate to your manager "
                "if unresolved after 24 hours. Do not use a personal device for any "
                "work systems — it's a data security violation."
            ),
        },
        {
            "q": "My FAROS access request has been pending for 3+ days.",
            "a": (
                "Raise a ServiceNow ticket under 'Access Management'. Include your "
                "employee ID, the system name, and forward your manager's approval email. "
                "Your manager can also expedite by calling IT Helpdesk (Ext. 4040) directly."
            ),
        },
        {
            "q": "I missed a Navigator training deadline.",
            "a": (
                "Log in to Navigator and self-enrol in the module again — most reset monthly. "
                "Notify HR Onboarding (Ext. 2000) so they can update your compliance record. "
                "Don't wait for them to chase you."
            ),
        },
        {
            "q": "Where do I submit expenses from my first week?",
            "a": (
                "Use Concur (link in the sidebar). All receipts must be uploaded within 30 days. "
                "Ask your buddy to walk you through the first submission — "
                "the cost centre coding has some quirks."
            ),
        },
        {
            "q": "I don't know who to ask for help day-to-day.",
            "a": (
                "Your buddy is your first port of call for anything informal. "
                "For IT issues: raise a ServiceNow ticket. "
                "For HR questions: Workday or Ext. 2000. "
                "For process questions: your manager or the team Slack channel."
            ),
        },
        {
            "q": "How do I book annual leave?",
            "a": (
                "All leave is booked through Workday. Submit your request at least 2 weeks "
                "in advance where possible. Your manager will approve or decline in Workday — "
                "don't assume it's approved until you see the confirmation."
            ),
        },
        {
            "q": "I'm struggling to settle in — is that normal?",
            "a": (
                "Completely normal. Most people feel overwhelmed in the first 4–6 weeks. "
                "Talk to your buddy — they've been through it. If it persists, speak to "
                "your manager at your next 1:1. The 30-day check-in is a good time to raise it."
            ),
        },
    ],

    # ── SPE-Specific ──────────────────────────────────────────────────────────
    "SPE": [
        {
            "q": "A part number in KOLA doesn't match what's on the physical part.",
            "a": (
                "Check for a supersession chain in KOLA first — the physical part may carry "
                "an old number that has since been replaced. If the chain is unclear or broken, "
                "raise it with your Senior SPE. Do not create a new part number without approval."
            ),
        },
        {
            "q": "I need to order a part urgently but GLOPPS shows 0 stock.",
            "a": (
                "Check RUMBA for legacy stock first — it sometimes shows inventory not visible "
                "in GLOPPS. If still nothing, escalate to your Logistics Lead for an emergency PO. "
                "Document every step in SAP so there's a paper trail."
            ),
        },
        {
            "q": "I don't understand when to choose Reman vs a new part.",
            "a": (
                "As a rule: Reman is preferred for cost and sustainability unless the customer "
                "contract explicitly requires new parts. Ask your Senior SPE for the "
                "Reman Decision Matrix SOP on SharePoint — it covers the edge cases."
            ),
        },
        {
            "q": "SAP won't let me save a new part number — it keeps throwing an error.",
            "a": (
                "The most common causes are a missing material group, an incomplete plant "
                "extension, or a mandatory field left blank. Ask your Senior SPE to review "
                "the entry with you before submitting — don't force it through."
            ),
        },
        {
            "q": "What's the difference between GLOPPS and RUMBA?",
            "a": (
                "GLOPPS is the current global logistics system — use it as your primary tool. "
                "RUMBA is the legacy system still used for older part records and "
                "historical stock that hasn't been migrated. Always check GLOPPS first, "
                "then RUMBA as a fallback."
            ),
        },
    ],

    # ── SE-Specific ───────────────────────────────────────────────────────────
    "SE": [
        {
            "q": "A customer is asking me to work without a formal Work Order.",
            "a": (
                "Never proceed without a Work Order in SAP Service Cloud. "
                "Politely explain that it is a compliance requirement — "
                "not a personal choice. Call your tech lead if the customer continues "
                "to push back. This protects both you and the company."
            ),
        },
        {
            "q": "I completed a job but can't submit my ESR — the system is down.",
            "a": (
                "Complete a paper ESR form (stored in your vehicle kit) and photograph it. "
                "Submit the digital version as soon as the system is restored. "
                "Notify your manager the same day so they're aware of the delay."
            ),
        },
        {
            "q": "I'm not sure if I need to apply LOTO for a specific job.",
            "a": (
                "If in any doubt, always apply LOTO. "
                "Check the LOTO Safety Portal for the equipment-specific isolation procedure. "
                "Time pressure is never a valid reason to skip it — "
                "speak to your tech lead if you need guidance."
            ),
        },
        {
            "q": "My vehicle broke down on the way to a customer site.",
            "a": (
                "Call Fleet Management immediately (number is on the dashboard card in your vehicle). "
                "Then notify your tech lead and the customer. Log it in the Fleet Management System "
                "when you're back online. Do not attempt roadside repairs yourself."
            ),
        },
        {
            "q": "A customer is being aggressive or abusive on site.",
            "a": (
                "You have the right to leave any unsafe situation. "
                "Calmly state that you will need to reschedule and remove yourself from the site. "
                "Call your tech lead immediately and document the incident in your ESR. "
                "Do not escalate the confrontation."
            ),
        },
    ],

}
