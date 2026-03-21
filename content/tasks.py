"""
tasks.py — Onboarding Checklist Tasks
======================================
Add, remove, or edit tasks here. The main app will pick up changes automatically.

Each task is a dict with these keys:
  Phase     : "Day 1" | "Week 1" | "Month 1" | "Month 2" | "Month 3"
  Category  : free-text label shown on the card (e.g. "IT Setup", "HR")
  Task      : the task name displayed to the user
  Mentor    : who owns/guides this task — use "Buddy" or "Manager" to get
              auto-substitution with the user's actual buddy/manager name
  Type      : "Action" | "Meeting" | "Training" | "Pickup" | "Admin"
              | "IT Ticket" | "Shadowing" | "Recurring" | "Milestone"
  Tip       : a short insider tip shown below the task (keep under 120 chars)
  Role      : "Common" | "SPE" | "SE"  — controls who sees the task

PHASE ORDER: Day 1 → Week 1 → Month 1 → Month 2 → Month 3
"""

from typing import List, Dict


# ---------------------------------------------------------------------------
# COMMON TASKS  (shown to both SPE and SE)
# ---------------------------------------------------------------------------
COMMON_TASKS: List[Dict] = [

    # ── Day 1 ───────────────────────────────────────────────────────────────
    {
        "Phase": "Day 1", "Category": "Logistics", "Role": "Common",
        "Task": "Collect Safety Shoes & PPE",
        "Mentor": "Office Admin", "Type": "Pickup",
        "Tip": "Check sizing beforehand — exchanges take 2 days.",
    },
    {
        "Phase": "Day 1", "Category": "Logistics", "Role": "Common",
        "Task": "Collect Laptop, Mobile & Headset",
        "Mentor": "IT Support", "Type": "Pickup",
        "Tip": "Confirm all accessories are in the box before signing.",
    },
    {
        "Phase": "Day 1", "Category": "IT Setup", "Role": "Common",
        "Task": "Initial Windows Login & MFA Setup",
        "Mentor": "IT Support", "Type": "Action",
        "Tip": "Use the Microsoft Authenticator app for MFA — not SMS.",
    },
    {
        "Phase": "Day 1", "Category": "Orientation", "Role": "Common",
        "Task": "Office Tour (Fire Exits & Muster Points)",
        "Mentor": "Buddy", "Type": "Meeting",
        "Tip": "Ask your buddy which muster point is active — they change seasonally.",
    },
    {
        "Phase": "Day 1", "Category": "HR", "Role": "Common",
        "Task": "Sign & Return Employment Contract",
        "Mentor": "HR Dept", "Type": "Admin",
        "Tip": "Keep a signed copy for yourself — HR can take 2 weeks to return one.",
    },

    # ── Week 1 ──────────────────────────────────────────────────────────────
    {
        "Phase": "Week 1", "Category": "HR", "Role": "Common",
        "Task": "Submit Bank Details via Workday",
        "Mentor": "HR Dept", "Type": "Admin",
        "Tip": "Must be done by Wednesday to be on the current payroll cycle.",
    },
    {
        "Phase": "Week 1", "Category": "Intro", "Role": "Common",
        "Task": "Team Intro Presentation",
        "Mentor": "Manager", "Type": "Meeting",
        "Tip": "Keep it to 5 mins max. Colleagues appreciate brevity.",
    },
    {
        "Phase": "Week 1", "Category": "IT Setup", "Role": "Common",
        "Task": "Set Up VPN & Test Remote Access",
        "Mentor": "IT Support", "Type": "Action",
        "Tip": "Test from home before you need it urgently.",
    },
    {
        "Phase": "Week 1", "Category": "Social", "Role": "Common",
        "Task": "Coffee Chat with Buddy",
        "Mentor": "Buddy", "Type": "Meeting",
        "Tip": "Ask them: 'What do you wish you knew in your first week?'",
    },

    # ── Month 1 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 1", "Category": "Process", "Role": "Common",
        "Task": "Complete First Solo Task (supervised)",
        "Mentor": "Manager", "Type": "Action",
        "Tip": "Ask for feedback immediately after — first impressions set the tone.",
    },
    {
        "Phase": "Month 1", "Category": "HR", "Role": "Common",
        "Task": "30-Day Check-in with Manager",
        "Mentor": "Manager", "Type": "Meeting",
        "Tip": "Prepare 3 things going well and 1 area where you need more support.",
    },
    {
        "Phase": "Month 1", "Category": "Learning", "Role": "Common",
        "Task": "Complete All Mandatory Navigator Courses",
        "Mentor": "HR Dept", "Type": "Training",
        "Tip": "Block 2 hours on a quiet afternoon — squeezing them in doesn't work.",
    },
    {
        "Phase": "Month 1", "Category": "Social", "Role": "Common",
        "Task": "Attend Team Weekly Stand-up x4",
        "Mentor": "Manager", "Type": "Recurring",
        "Tip": "Speak up at least once per stand-up — visibility matters early on.",
    },

    # ── Month 2 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 2", "Category": "Review", "Role": "Common",
        "Task": "60-Day Performance Conversation",
        "Mentor": "Manager", "Type": "Meeting",
        "Tip": "Bring a self-assessment. Managers appreciate ownership of development.",
    },
    {
        "Phase": "Month 2", "Category": "Process", "Role": "Common",
        "Task": "Handle First Task Independently",
        "Mentor": "Manager", "Type": "Milestone",
        "Tip": "You've got this. Ask questions early rather than late.",
    },
    {
        "Phase": "Month 2", "Category": "Network", "Role": "Common",
        "Task": "Intro Call with Colleague from Another Site",
        "Mentor": "Manager", "Type": "Meeting",
        "Tip": "Cross-site relationships are how you solve problems fast.",
    },

    # ── Month 3 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 3", "Category": "Review", "Role": "Common",
        "Task": "90-Day Review & Goal Setting",
        "Mentor": "Manager", "Type": "Meeting",
        "Tip": "Set 3–5 SMART goals for the next quarter.",
    },
    {
        "Phase": "Month 3", "Category": "Contribute", "Role": "Common",
        "Task": "Propose One Process Improvement Idea",
        "Mentor": "Manager", "Type": "Milestone",
        "Tip": "Doesn't need to be big — even a template or checklist improvement counts.",
    },
    {
        "Phase": "Month 3", "Category": "Network", "Role": "Common",
        "Task": "Onboard or Buddy a Newer Colleague",
        "Mentor": "HR Dept", "Type": "Milestone",
        "Tip": "Teaching what you've learned is the best way to solidify it.",
    },
]


# ---------------------------------------------------------------------------
# SPE-SPECIFIC TASKS  (Spare Parts Engineer only)
# ---------------------------------------------------------------------------
SPE_TASKS: List[Dict] = [

    # ── Week 1 ──────────────────────────────────────────────────────────────
    {
        "Phase": "Week 1", "Category": "Access", "Role": "SPE",
        "Task": "Request: GLOPPS & KOLA via FAROS",
        "Mentor": "Logistics Lead", "Type": "IT Ticket",
        "Tip": "Request both in the same ticket — they share the same approver.",
    },
    {
        "Phase": "Week 1", "Category": "Training", "Role": "SPE",
        "Task": "Read Reman Process SOP on SharePoint",
        "Mentor": "Senior SPE", "Type": "Training",
        "Tip": "Ask your Senior SPE which sections are actually tested day-to-day.",
    },
    {
        "Phase": "Week 1", "Category": "Training", "Role": "SPE",
        "Task": "Shadow a Senior SPE on a Parts Order",
        "Mentor": "Senior SPE", "Type": "Shadowing",
        "Tip": "Watch how they handle supersession checks in KOLA — not obvious from docs.",
    },

    # ── Month 1 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 1", "Category": "Process", "Role": "SPE",
        "Task": "Create Your First Part Number in SAP",
        "Mentor": "Senior SPE", "Type": "Action",
        "Tip": "Get it reviewed before submitting — errors require a full reversal process.",
    },
    {
        "Phase": "Month 1", "Category": "Learning", "Role": "SPE",
        "Task": "Complete SAP ERP: Supply Chain Navigator Course",
        "Mentor": "Training Portal", "Type": "Training",
        "Tip": "The MRP module is the most useful for day-to-day work.",
    },

    # ── Month 2 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 2", "Category": "Process", "Role": "SPE",
        "Task": "Conduct First Dead Stock Review",
        "Mentor": "Logistics Lead", "Type": "Action",
        "Tip": "Use the PowerBI dashboard — your Logistics Lead can share the template.",
    },

]


# ---------------------------------------------------------------------------
# SE-SPECIFIC TASKS  (Service Engineer only)
# ---------------------------------------------------------------------------
SE_TASKS: List[Dict] = [

    # ── Week 1 ──────────────────────────────────────────────────────────────
    {
        "Phase": "Week 1", "Category": "Access", "Role": "SE",
        "Task": "Request: SAP Service Module via FAROS",
        "Mentor": "Tech Lead", "Type": "IT Ticket",
        "Tip": "Attach your manager's approval email — it halves processing time.",
    },
    {
        "Phase": "Week 1", "Category": "Training", "Role": "SE",
        "Task": "LOTO Certification (Safety Portal)",
        "Mentor": "Safety Officer", "Type": "Training",
        "Tip": "This blocks field access until complete — prioritise above everything else.",
    },
    {
        "Phase": "Week 1", "Category": "Training", "Role": "SE",
        "Task": "Shadow a Senior SE on a Live Job",
        "Mentor": "Tech Lead", "Type": "Shadowing",
        "Tip": "Take notes on the ESR process — the first one you file solo is the trickiest.",
    },

    # ── Month 1 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 1", "Category": "Field", "Role": "SE",
        "Task": "Complete 3 Jobs with ESR Filed Same Day",
        "Mentor": "Tech Lead", "Type": "Action",
        "Tip": "ESRs filed late create customer billing delays — your manager watches this.",
    },
    {
        "Phase": "Month 1", "Category": "Training", "Role": "SE",
        "Task": "Defensive Driving Certification",
        "Mentor": "Safety Officer", "Type": "Training",
        "Tip": "Book early — slots fill up 3 weeks in advance.",
    },

    # ── Month 2 ─────────────────────────────────────────────────────────────
    {
        "Phase": "Month 2", "Category": "Field", "Role": "SE",
        "Task": "Complete 10 Cumulative Solo Jobs",
        "Mentor": "Tech Lead", "Type": "Milestone",
        "Tip": "Track your jobs in a personal log — useful for your 90-day review.",
    },

]


# ---------------------------------------------------------------------------
# PUBLIC FUNCTION — called by the main app
# ---------------------------------------------------------------------------
PHASE_ORDER = ["Day 1", "Week 1", "Month 1", "Month 2", "Month 3"]

def get_checklist_data(full_role: str) -> List[Dict]:
    """
    Returns the full ordered task list for a given role.
    Tasks are sorted by PHASE_ORDER so the checklist always renders correctly.
    """
    from content.courses import ROLE_KEY_MAP  # avoid circular at module level
    role_key = ROLE_KEY_MAP.get(full_role, "SPE")

    role_tasks = SPE_TASKS if role_key == "SPE" else SE_TASKS
    all_tasks  = COMMON_TASKS + role_tasks

    # Sort by phase order so mixed sources always appear in the right order
    return sorted(all_tasks, key=lambda t: PHASE_ORDER.index(t["Phase"]))