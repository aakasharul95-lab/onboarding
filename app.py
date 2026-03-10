import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Tuple, Dict
from datetime import date, datetime, timedelta
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="SPAE Onboarding Hub", layout="wide", page_icon="⚙️", initial_sidebar_state="expanded")

try:
    import graphviz
    has_graphviz = True
except ModuleNotFoundError:
    has_graphviz = False

# --- 1. CONSTANTS & HELPER DATA ---
ROLE_KEY_MAP: Dict[str, str] = {
    "SPE (Spare Parts Engineer)": "SPE",
    "SE (Service Engineer)": "SE",
}
PHASE_PRIORITY: List[str] = ["Day 1", "Week 1", "Month 1", "Month 2", "Month 3"]

FAROS_CATALOG: Dict[str, List[str]] = {
    "Common": ["Microsoft 365 (Outlook, Teams, Excel)", "Cisco AnyConnect VPN (Remote Access)", "Workday (HR & Payroll)", "Concur (Travel & Expenses)", "ServiceNow (IT Helpdesk)", "Slack (Internal Comm Channels)", "LastPass Enterprise (Password Manager)", "Zoom (Video Conferencing)", "SharePoint: Global Engineering"],
    "SPE": ["SAP GUI: ERP System (Production)", "GLOPPS (Global Logistics & Parts)", "KOLA (Parts Documentation DB)", "RUMBA (Legacy Parts Lookup)", "Autodesk Vault (CAD Data Management)", "Creo MCAD (View & Edit License)", "Agile PLM: Product Lifecycle Mgmt", "PowerBI Desktop (Inventory Analytics)"],
    "SE": ["SAP Service Cloud (C4C)", "MOM (Mobile Order Management App)", "LOTO Safety Portal (Lock Out Tag Out)", "ESR Tool (Electronic Service Report)", "Hydraulic Schematics Viewer (HSV)", "Salesforce CRM (Customer History)", "ServiceMax (Field Dispatch)", "Fleet Management System (Vehicle Logs)"]
}

NAVIGATOR_COURSES: Dict[str, List[str]] = {
    "Mandatory": ["Global Data Privacy & GDPR (30 mins)", "Cybersecurity Awareness: Phishing (15 mins)", "Code of Conduct: Anti-Bribery (45 mins)", "Diversity & Inclusion Basics (20 mins)", "Health & Safety: Office Ergonomics (15 mins)"],
    "SPE": ["SAP ERP: Supply Chain Basics (60 mins)", "Logistics 101: Incoterms (30 mins)", "Agile PLM: Document Control (45 mins)"],
    "SE": ["Field Safety: Electrical Hazards (60 mins)", "Defensive Driving Certification (External)", "Customer Service: Handling Conflict (30 mins)"]
}

TOOLKIT: Dict[str, List[str]] = {
    "Common": ["Tidinfo – Technical information portal", "SCORE – Service & Customer Operations Reporting Engine"],
    "SPE": ["Parts Costing Calculator", "BOM Comparison Utility"],
    "SE": ["Service Checklists Mobile Pack", "Field Report Template Pack"]
}

IMPORTANT_LINKS: Dict[str, str] = {
    "FAROS (Access Portal)": "https://faros.internal.example.com",
    "Navigator (Learning)": "https://navigator.internal.example.com",
    "Workday (HR)": "https://www.myworkday.com",
    "Concur (Expenses)": "https://www.concursolutions.com"
}

ACRONYMS: Dict[str, str] = {
    "AI": "Aakash Intelligence", "KOLA": "Key On-Line Access (Parts DB)", "LOTO": "Lock Out Tag Out",
    "MOM": "Mobile Order Management", "SAP": "Systems, Applications, and Products",
    "SPE": "Spare Parts Engineer", "SE": "Service Engineer",
    "BOM": "Bill of Materials", "PLM": "Product Lifecycle Management",
    "ERP": "Enterprise Resource Planning", "CRM": "Customer Relationship Management",
    "PPE": "Personal Protective Equipment", "SOP": "Standard Operating Procedure",
    "ESR": "Electronic Service Report", "HSV": "Hydraulic Schematics Viewer",
    "VPN": "Virtual Private Network", "PO": "Purchase Order",
    "Tobias": "Totally Outclassed By Intelligent Aakash Significantly",
    "Aakash": "An Absolute Knight Amongst Silly Humans"
}

KEY_CONTACTS: Dict[str, str] = {
    "IT Helpdesk": "Ext. 4040", "HR Onboarding": "Ext. 2000", "Safety Officer": "Ext. 9110"
}

THEME_IMAGES = {
    "SPE": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=600&q=80",
    "SE": "https://images.unsplash.com/photo-1581092335397-9583eb92d232?auto=format&fit=crop&w=600&q=80"
}

# --- GLOSSARY ---
GLOSSARY: Dict[str, Dict[str, str]] = {
    "SPE": {
        "Reman": "Remanufactured part — a used component restored to original spec. Often cheaper than new.",
        "BOM": "Bill of Materials — a structured list of all components needed to build a product.",
        "Supersession": "When a part number is replaced by a newer one. Always check KOLA for current part numbers.",
        "Incoterms": "International commercial terms defining who pays for shipping, insurance, and import duties.",
        "MOQ": "Minimum Order Quantity — the smallest amount a supplier will sell in a single order.",
        "Lead Time": "The time between placing an order and receiving the parts. Critical for planning.",
        "Dead Stock": "Inventory that hasn't moved in 12+ months. SPEs review this quarterly.",
        "Cross-Reference": "Matching a competitor's part number to our equivalent in KOLA or GLOPPS.",
    },
    "SE": {
        "LOTO": "Lock Out Tag Out — mandatory safety procedure before working on any energised equipment.",
        "ESR": "Electronic Service Report — the digital record of every job you complete. Must be filed same day.",
        "Work Order": "A formal job instruction from SAP Service Cloud. Never work without one.",
        "SLA": "Service Level Agreement — the contracted response/fix time promised to a customer.",
        "Escalation": "When a job exceeds your skill level or time — immediately notify your tech lead.",
        "Warranty Claim": "A request to replace a part under manufacturer warranty. Requires ESR + photo evidence.",
        "Timesheet": "Daily log of hours per work order submitted via MOM. Must be done before 6pm.",
        "De-brief": "End-of-day call with your manager to review completed and outstanding jobs.",
    }
}

# --- FAQs ---
FAQS: Dict[str, List[Dict[str, str]]] = {
    "Common": [
        {"q": "I haven't received my laptop yet — what do I do?", "a": "Contact IT Helpdesk (Ext. 4040) immediately. Escalate to your manager if unresolved after 24 hours. Do not use a personal device for work systems."},
        {"q": "My FAROS access request has been pending for 3+ days.", "a": "Raise a ServiceNow ticket under 'Access Management'. Include your employee ID, system name, and manager approval email. Your manager can also expedite by calling Ext. 4040."},
        {"q": "I missed a Navigator training deadline.", "a": "Log in to Navigator and self-enroll again. Notify HR Onboarding (Ext. 2000) so they can update your compliance record. Most modules reset monthly."},
        {"q": "Where do I submit expenses from my first week?", "a": "Use Concur (link in sidebar). All receipts must be uploaded within 30 days. Ask your buddy to walk you through the first submission — it has some quirks."},
        {"q": "I don't know who to ask for help day-to-day.", "a": "Your buddy is your first point of call for anything informal. For IT issues: ServiceNow. For HR: Workday or Ext. 2000. For process questions: your manager or the team Slack channel."},
    ],
    "SPE": [
        {"q": "A part number in KOLA doesn't match what's on the physical part.", "a": "Check for a supersession chain in KOLA first. If unresolved, raise it with your Senior SPE — do not create a new part number without approval."},
        {"q": "I need to order a part urgently but GLOPPS shows 0 stock.", "a": "Check RUMBA for legacy stock first. If nothing, escalate to your Logistics Lead for an emergency PO. Document everything in SAP."},
        {"q": "I don't understand the Reman vs New pricing decision.", "a": "As a rule: Reman is preferred for cost and sustainability unless the customer contract specifies new parts. Ask your Senior SPE for the Reman Decision Matrix SOP on SharePoint."},
    ],
    "SE": [
        {"q": "A customer is asking me to work without a formal Work Order.", "a": "Never proceed without a Work Order in SAP Service Cloud. Politely explain this is a compliance requirement. Call your tech lead if the customer pushes back."},
        {"q": "I completed a job but can't submit my ESR — the system is down.", "a": "Complete a paper ESR form (in your vehicle kit) and photograph it. Submit digitally as soon as the system is back. Notify your manager same day."},
        {"q": "I'm not sure if I need to apply LOTO for a specific job.", "a": "If in doubt, always apply LOTO. Check the LOTO Safety Portal for the equipment-specific procedure. Never skip it based on time pressure."},
    ]
}

# --- BADGES ---
ALL_BADGES = [
    {"id": "first_step",    "name": "First Step",         "icon": "👟", "desc": "Complete your very first task",             "condition": lambda c, n, xp: c >= 1},
    {"id": "week1_done",    "name": "Week 1 Warrior",      "icon": "⚔️", "desc": "Complete all Day 1 & Week 1 tasks",         "condition": lambda c, n, xp: n >= 1},
    {"id": "half_way",      "name": "Halfway There",       "icon": "🌗", "desc": "Reach 50% overall progress",               "condition": lambda c, n, xp: xp >= 0.5},
    {"id": "quiz_ace",      "name": "Quiz Ace",            "icon": "🧠", "desc": "Score 100% on a knowledge quiz",           "condition": lambda c, n, xp: st.session_state.get('perfect_quiz', False)},
    {"id": "learning_done", "name": "Scholar",             "icon": "🎓", "desc": "Complete all Navigator training modules",  "condition": lambda c, n, xp: n >= 1.0},
    {"id": "champion",      "name": "SPAE Champion",       "icon": "🏆", "desc": "Reach 100% overall completion",            "condition": lambda c, n, xp: xp >= 1.0},
    {"id": "speed_runner",  "name": "Speed Runner",        "icon": "⚡", "desc": "Complete 5 tasks in a single session",     "condition": lambda c, n, xp: st.session_state.get('session_completions', 0) >= 5},
]

# --- QUIZZES ---
QUIZZES: Dict[str, List[Dict]] = {
    "SPE": [
        {"q": "What does BOM stand for?",                          "options": ["Bill of Materials", "Batch Order Management", "Base Order Module", "Budget of Materials"],        "answer": 0, "explanation": "BOM = Bill of Materials. It lists every component needed to build a product."},
        {"q": "Where do you look up a part number supersession?",   "options": ["SAP GUI", "KOLA", "GLOPPS", "Agile PLM"],                                                         "answer": 1, "explanation": "KOLA (Key On-Line Access) is the parts documentation database where you check supersession chains."},
        {"q": "What does 'Reman' mean in parts context?",           "options": ["A brand-new part", "A remanufactured part restored to original spec", "A rejected part", "A part on back-order"], "answer": 1, "explanation": "Reman = Remanufactured. It's a used part restored to OEM specification — often preferred for cost & sustainability."},
        {"q": "Which system is used to check global logistics/inventory?", "options": ["RUMBA", "KOLA", "GLOPPS", "Agile PLM"],                                                    "answer": 2, "explanation": "GLOPPS = Global Logistics & Parts System. RUMBA is legacy and used as a fallback."},
        {"q": "Who approves a new part number creation?",           "options": ["Any SPE can do it", "Only a Senior SPE after review", "IT Helpdesk", "FAROS Admin"],               "answer": 1, "explanation": "New part numbers must be approved by a Senior SPE. Never create one without sign-off."},
    ],
    "SE": [
        {"q": "What does LOTO stand for?",                          "options": ["Lock On Tag Off", "Lock Out Tag Out", "Log Off Turn Over", "Lift Out Test On"],                   "answer": 1, "explanation": "LOTO = Lock Out Tag Out. A mandatory safety procedure before working on any energised equipment."},
        {"q": "What do you do if a customer asks you to work without a Work Order?", "options": ["Proceed if the job is small", "Politely refuse and notify your tech lead", "Create the Work Order yourself later", "Ask the customer to email you instead"], "answer": 1, "explanation": "Never work without a Work Order in SAP Service Cloud. Compliance is non-negotiable."},
        {"q": "What is an ESR?",                                    "options": ["Emergency Safety Report", "Electronic Service Report", "External System Request", "Employee Status Review"], "answer": 1, "explanation": "ESR = Electronic Service Report. Must be filed the same day as the job."},
        {"q": "When should you apply LOTO if unsure?",              "options": ["Only for large machines", "Only if your manager says so", "Always apply it if in doubt", "Only for electrical work"], "answer": 2, "explanation": "If in doubt, always apply LOTO. Never skip it due to time pressure."},
        {"q": "What is the timesheet deadline each day?",           "options": ["End of week", "Next morning", "6pm same day", "Whenever you remember"],                           "answer": 2, "explanation": "Timesheets must be submitted via MOM before 6pm each working day."},
    ]
}

# --- EXTENDED CHECKLIST ---
def get_checklist_data(full_role: str) -> List[Dict]:
    role_key = get_role_key(full_role)
    tasks: List[Dict] = [
        # Day 1
        {"Phase": "Day 1",   "Category": "Logistics",    "Task": "Collect Safety Shoes & PPE",           "Mentor": "Office Admin",   "Type": "Pickup",    "Tip": "Check sizing beforehand — exchanges take 2 days."},
        {"Phase": "Day 1",   "Category": "Logistics",    "Task": "Collect Laptop, Mobile & Headset",     "Mentor": "IT Support",     "Type": "Pickup",    "Tip": "Confirm all accessories are in the box before signing."},
        {"Phase": "Day 1",   "Category": "IT Setup",     "Task": "Initial Windows Login & MFA Setup",    "Mentor": "IT Support",     "Type": "Action",    "Tip": "Use the Microsoft Authenticator app for MFA — not SMS."},
        {"Phase": "Day 1",   "Category": "Orientation",  "Task": "Office Tour (Fire Exits & Muster)",    "Mentor": "Buddy",          "Type": "Meeting",   "Tip": "Ask your buddy which muster point is active — they change seasonally."},
        {"Phase": "Day 1",   "Category": "HR",           "Task": "Sign & Return Employment Contract",    "Mentor": "HR Dept",        "Type": "Admin",     "Tip": "Keep a signed copy for yourself — HR can take 2 weeks to return one."},
        # Week 1
        {"Phase": "Week 1",  "Category": "HR",           "Task": "Submit Bank Details via Workday",      "Mentor": "HR Dept",        "Type": "Admin",     "Tip": "Must be done by Wednesday to be on the current payroll cycle."},
        {"Phase": "Week 1",  "Category": "Intro",        "Task": "Team Intro Presentation",              "Mentor": "Manager",        "Type": "Meeting",   "Tip": "Keep it to 5 mins max. Colleagues appreciate brevity."},
        {"Phase": "Week 1",  "Category": "IT Setup",     "Task": "Set Up VPN & Test Remote Access",      "Mentor": "IT Support",     "Type": "Action",    "Tip": "Test from home before you need it urgently."},
        {"Phase": "Week 1",  "Category": "Social",       "Task": "Coffee Chat with Buddy",               "Mentor": "Buddy",          "Type": "Meeting",   "Tip": "Ask them: 'What do you wish you knew in your first week?'"},
    ]
    # Role-specific Week 1
    if role_key == "SE":
        tasks.extend([
            {"Phase": "Week 1",  "Category": "Access",      "Task": "Request: SAP Service Module via FAROS",   "Mentor": "Tech Lead",        "Type": "IT Ticket", "Tip": "Attach your manager's approval email to the FAROS request — it halves processing time."},
            {"Phase": "Week 1",  "Category": "Training",    "Task": "LOTO Certification (Safety Portal)",      "Mentor": "Safety Officer",   "Type": "Training",  "Tip": "This blocks field access until complete — prioritise it above everything else."},
            {"Phase": "Week 1",  "Category": "Training",    "Task": "Shadow a Senior SE on a Live Job",        "Mentor": "Tech Lead",        "Type": "Shadowing", "Tip": "Take notes on the ESR process — the first one you file solo is always the trickiest."},
        ])
    elif role_key == "SPE":
        tasks.extend([
            {"Phase": "Week 1",  "Category": "Access",      "Task": "Request: GLOPPS & KOLA via FAROS",        "Mentor": "Logistics Lead",   "Type": "IT Ticket", "Tip": "Request both in the same ticket — they share the same approver."},
            {"Phase": "Week 1",  "Category": "Training",    "Task": "Read Reman Process SOP on SharePoint",    "Mentor": "Senior SPE",       "Type": "Training",  "Tip": "The SOP is long — ask your Senior SPE which sections are actually tested day-to-day."},
            {"Phase": "Week 1",  "Category": "Training",    "Task": "Shadow a Senior SPE on a Parts Order",    "Mentor": "Senior SPE",       "Type": "Shadowing", "Tip": "Watch how they handle supersession checks in KOLA — it's not obvious from the docs."},
        ])
    # Month 1
    tasks.extend([
        {"Phase": "Month 1", "Category": "Process",     "Task": "Complete First Solo Task (supervised)",     "Mentor": "Manager",        "Type": "Action",    "Tip": "Ask for feedback immediately after — first impressions set the tone."},
        {"Phase": "Month 1", "Category": "HR",          "Task": "30-Day Check-in with Manager",              "Mentor": "Manager",        "Type": "Meeting",   "Tip": "Prepare 3 things going well and 1 area where you need more support."},
        {"Phase": "Month 1", "Category": "Learning",    "Task": "Complete All Mandatory Navigator Courses",  "Mentor": "HR Dept",        "Type": "Training",  "Tip": "Block 2 hours on a quiet afternoon — trying to squeeze them into spare minutes doesn't work."},
        {"Phase": "Month 1", "Category": "Social",      "Task": "Attend Team Weekly Stand-up x4",            "Mentor": "Manager",        "Type": "Recurring", "Tip": "Speak up at least once per stand-up — visibility matters early on."},
    ])
    if role_key == "SE":
        tasks.extend([
            {"Phase": "Month 1", "Category": "Field",      "Task": "Complete 3 Jobs with ESR Filed Same Day",  "Mentor": "Tech Lead",        "Type": "Action",    "Tip": "ESRs filed late create customer billing delays — your manager watches this metric."},
            {"Phase": "Month 1", "Category": "Training",   "Task": "Defensive Driving Certification",          "Mentor": "Safety Officer",   "Type": "Training",  "Tip": "Book early — slots fill up 3 weeks in advance."},
        ])
    elif role_key == "SPE":
        tasks.extend([
            {"Phase": "Month 1", "Category": "Process",    "Task": "Create Your First Part Number in SAP",     "Mentor": "Senior SPE",       "Type": "Action",    "Tip": "Get it reviewed before submitting — errors require a full reversal process."},
            {"Phase": "Month 1", "Category": "Learning",   "Task": "Complete SAP ERP: Supply Chain Navigator", "Mentor": "Training Portal",  "Type": "Training",  "Tip": "The module on MRP is the most useful for day-to-day work."},
        ])
    # Month 2
    tasks.extend([
        {"Phase": "Month 2", "Category": "Review",      "Task": "60-Day Performance Conversation",           "Mentor": "Manager",        "Type": "Meeting",   "Tip": "Bring a self-assessment. Managers appreciate when new hires take ownership of their development."},
        {"Phase": "Month 2", "Category": "Process",     "Task": "Handle First Task Independently",           "Mentor": "Manager",        "Type": "Milestone", "Tip": "You've got this. Trust the process and ask questions early rather than late."},
        {"Phase": "Month 2", "Category": "Network",     "Task": "Intro Call with Colleague from Another Site","Mentor": "Manager",        "Type": "Meeting",   "Tip": "Cross-site relationships are how you solve problems fast when your local team is stuck."},
    ])
    if role_key == "SE":
        tasks.extend([
            {"Phase": "Month 2", "Category": "Field",      "Task": "Complete 10 Cumulative Solo Jobs",          "Mentor": "Tech Lead",        "Type": "Milestone", "Tip": "Track your jobs in a personal log — useful for your 90-day review."},
        ])
    elif role_key == "SPE":
        tasks.extend([
            {"Phase": "Month 2", "Category": "Process",    "Task": "Conduct First Dead Stock Review",           "Mentor": "Logistics Lead",   "Type": "Action",    "Tip": "Use the PowerBI dashboard — your Logistics Lead can share the template report."},
        ])
    # Month 3
    tasks.extend([
        {"Phase": "Month 3", "Category": "Review",      "Task": "90-Day Review & Goal Setting",              "Mentor": "Manager",        "Type": "Meeting",   "Tip": "Set 3–5 SMART goals for the next quarter. Ask your manager what success looks like at 6 months."},
        {"Phase": "Month 3", "Category": "Contribute",  "Task": "Propose One Process Improvement Idea",     "Mentor": "Manager",        "Type": "Milestone", "Tip": "Doesn't need to be big — even a template or checklist improvement counts."},
        {"Phase": "Month 3", "Category": "Network",     "Task": "Onboard or Buddy a Newer Colleague",       "Mentor": "HR Dept",        "Type": "Milestone", "Tip": "Teaching what you've learned is the best way to solidify it."},
    ])
    return tasks

# --- 2. HELPER FUNCTIONS ---
def inject_global_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        html, body, p, div, h1, h2, h3, h4, h5, h6, li, span, label, a {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .material-symbols-rounded, .material-icons { font-family: 'Material Symbols Rounded' !important; }
        .stApp::before {
            content: "";
            position: fixed; top: 0; left: 0; right: 0;
            height: 5px;
            background: linear-gradient(90deg, #4f46e5, #0ea5e9, #10b981);
            z-index: 99999;
        }
        [data-testid="stMetricValue"] { font-weight: 800; font-size: 2.2rem; color: var(--text-color); }
        [data-testid="stMetricLabel"] > div { font-size: 0.95rem; font-weight: 600; opacity: 0.8; }
        .hero-card {
            padding: 2.0rem; border-radius: 1rem;
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.2);
            box-shadow: 0 8px 24px -5px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .hero-card h1 { margin-bottom: 0.2rem; font-size: 2.5rem; font-weight: 800; color: var(--text-color); letter-spacing: -0.5px; }
        .pill {
            display: inline-flex; align-items: center; justify-content: center;
            padding: 0.4rem 1rem; border-radius: 999px; font-size: 0.85rem; font-weight: 700;
            border: 1px solid var(--primary-color);
            background: linear-gradient(90deg, rgba(79,70,229,0.1), rgba(16,185,129,0.1));
            color: var(--primary-color);
        }
        .badge-card {
            padding: 1rem; border-radius: 0.75rem; text-align: center;
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.15);
            transition: transform 0.2s;
        }
        .badge-card:hover { transform: translateY(-3px); }
        .badge-locked { opacity: 0.35; filter: grayscale(1); }
        .badge-icon { font-size: 2.5rem; line-height: 1; }
        .badge-name { font-weight: 700; font-size: 0.85rem; margin-top: 4px; }
        .badge-desc { font-size: 0.75rem; opacity: 0.7; margin-top: 2px; }
        .checklist-row {
            padding: 0.5rem 1rem; border-radius: 0.5rem;
            border-left: 3px solid transparent;
            background-color: var(--secondary-background-color);
            margin-bottom: 0.5rem;
            transition: all 0.2s cubic-bezier(0.4,0,0.2,1);
        }
        .checklist-row:hover { border-left: 3px solid var(--primary-color); transform: translateX(4px); }
        .tip-box {
            font-size: 0.8rem; opacity: 0.75; margin-top: 2px;
            padding: 2px 8px; border-left: 2px solid #0ea5e9;
        }
        .mentor-badge {
            background-color: rgba(128,128,128,0.15); padding: 4px 8px;
            border-radius: 6px; font-size: 0.8rem; font-weight: 600; color: var(--text-color);
        }
        .days-counter {
            font-size: 3rem; font-weight: 800; color: var(--primary-color); line-height: 1;
        }
        .wizard-step {
            padding: 1.5rem; border-radius: 1rem;
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.2);
            margin-bottom: 1rem;
        }
        .muted { opacity: 0.85; font-size: 1.05rem; line-height: 1.6; }
        </style>
    """, unsafe_allow_html=True)

def get_role_key(full_role: str) -> str:
    return ROLE_KEY_MAP.get(full_role, "SPE")

def create_donut_chart(progress: float):
    progress_pct = round(progress * 100)
    source = pd.DataFrame({"Category": ["Completed", "Remaining"], "Value": [progress_pct, 100 - progress_pct]})
    return alt.Chart(source).mark_arc(innerRadius=60, cornerRadius=15).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Category", type="nominal",
                        scale=alt.Scale(domain=["Completed", "Remaining"], range=["#3b82f6", "rgba(128,128,128,0.15)"]),
                        legend=None),
        tooltip=['Category', 'Value']
    ).properties(width=220, height=220)

def navigator_course_key(section: str, course: str) -> str:
    return f"{section}::{course}"

def init_navigator_status() -> None:
    role_key = get_role_key(st.session_state['user_role'])
    if 'navigator_status' not in st.session_state:
        st.session_state['navigator_status'] = {}
    status = st.session_state['navigator_status']
    for c in NAVIGATOR_COURSES["Mandatory"]:
        status.setdefault(navigator_course_key("Mandatory", c), False)
    for c in NAVIGATOR_COURSES[role_key]:
        status.setdefault(navigator_course_key(role_key, c), False)

def get_navigator_progress() -> Tuple[int, int]:
    role_key = get_role_key(st.session_state['user_role'])
    status = st.session_state.get('navigator_status', {})
    all_courses = [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] + [(role_key, c) for c in NAVIGATOR_COURSES[role_key]]
    return sum(1 for s, c in all_courses if status.get(navigator_course_key(s, c), False)), len(all_courses)

def get_overall_progress() -> Tuple[float, float, float]:
    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_p = df['Status'].sum() / len(df) if not df.empty else 0.0
    nav_done, nav_total = get_navigator_progress()
    navigator_p = nav_done / nav_total if nav_total > 0 else 0.0
    return checklist_p, navigator_p, (0.5 * checklist_p) + (0.5 * navigator_p)

def get_xp_and_level() -> Tuple[int, int, str]:
    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_done = df['Status'].sum() if not df.empty else 0
    nav_done, nav_total = get_navigator_progress()
    xp = int((checklist_done * 20) + (nav_done * 50))
    max_xp = int((len(df) * 20) + (nav_total * 50)) if not df.empty else 100
    if xp == 0: level_name = "Welcome Aboard 👋"
    elif xp < max_xp * 0.3: level_name = "Rising Star ⭐"
    elif xp < max_xp * 0.6: level_name = "Momentum Builder 🚀"
    elif xp < max_xp * 0.85: level_name = "Process Pro 🧠"
    elif xp < max_xp: level_name = "Almost There 🔥"
    else: level_name = "SPAE Champion 🏆"
    return xp, max_xp, level_name

def get_earned_badges() -> List[str]:
    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_done = df['Status'].sum() / len(df) if not df.empty else 0
    nav_done, nav_total = get_navigator_progress()
    nav_p = nav_done / nav_total if nav_total > 0 else 0
    _, _, overall_p = get_overall_progress()
    week1_phases = df[df['Phase'].isin(['Day 1', 'Week 1'])]
    week1_done_ratio = week1_phases['Status'].sum() / len(week1_phases) if not week1_phases.empty else 0
    earned = []
    for badge in ALL_BADGES:
        if badge['id'] == 'first_step' and checklist_done >= 1 / len(df) if not df.empty else False:
            earned.append(badge['id'])
        elif badge['id'] == 'week1_done' and week1_done_ratio >= 1.0:
            earned.append(badge['id'])
        elif badge['id'] == 'half_way' and overall_p >= 0.5:
            earned.append(badge['id'])
        elif badge['id'] == 'quiz_ace' and st.session_state.get('perfect_quiz', False):
            earned.append(badge['id'])
        elif badge['id'] == 'learning_done' and nav_p >= 1.0:
            earned.append(badge['id'])
        elif badge['id'] == 'champion' and overall_p >= 1.0:
            earned.append(badge['id'])
        elif badge['id'] == 'speed_runner' and st.session_state.get('session_completions', 0) >= 5:
            earned.append(badge['id'])
    return earned

def reset_user() -> None:
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]
    st.session_state['navigator_status'] = {}
    init_navigator_status()
    st.session_state['quiz_state'] = {}
    st.session_state['session_completions'] = 0
    st.session_state['perfect_quiz'] = False

def toggle_status(index: int) -> None:
    was_done = st.session_state['curriculum'][index]['Status']
    st.session_state['curriculum'][index]['Status'] = not was_done
    if not was_done:
        task_name = st.session_state['curriculum'][index]['Task']
        st.toast(f"Done! '{task_name}' ✅ +20 XP!", icon="🔥")
        st.session_state['session_completions'] = st.session_state.get('session_completions', 0) + 1

def nav_click_callback(section: str, course: str) -> None:
    key = navigator_course_key(section, course)
    is_done = st.session_state[f"nav_{key}"]
    st.session_state['navigator_status'][key] = is_done
    if is_done:
        st.toast(f"Completed '{course}' +50 XP! 🧠", icon="🌟")

def get_tech_stack_graph(role_key: str):
    if not has_graphviz: return None
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR', bgcolor='transparent')
    graph.attr('node', shape='box', style='filled', fontname='Helvetica, sans-serif', rx='5', ry='5')
    graph.attr('edge', color='#cbd5e1', fontcolor='#cbd5e1', fontname='Helvetica, sans-serif', fontsize='10')
    if role_key == "SE":
        graph.node('C', 'Customer Site', fillcolor='#bae6fd', color='#0284c7')
        graph.node('SF', 'Salesforce (CRM)', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('SAP', 'SAP Service Module', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('MOM', 'MOM App (Mobile)', fillcolor='#bbf7d0', color='#16a34a')
        graph.node('KOLA', 'KOLA (Parts DB)', shape='cylinder', fillcolor='#e9d5ff', color='#9333ea')
        graph.edge('C', 'SF', label=' Ticket Created')
        graph.edge('SF', 'SAP', label=' Job Dispatch')
        graph.edge('SAP', 'MOM', label=' Work Order Sync')
        graph.edge('MOM', 'KOLA', label=' Lookup Parts')
        graph.edge('MOM', 'SAP', label=' Submit Timesheet')
    else:
        graph.node('V', 'Vendor / Supplier', fillcolor='#bae6fd', color='#0284c7')
        graph.node('SAP', 'SAP GUI (ERP)', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('PLM', 'Agile PLM', shape='ellipse', fillcolor='#e9d5ff', color='#9333ea')
        graph.node('CAD', 'Creo / Vault', fillcolor='#bbf7d0', color='#16a34a')
        graph.node('GLOPPS', 'GLOPPS (Logistics)', shape='cylinder', fillcolor='#fecdd3', color='#e11d48')
        graph.edge('V', 'SAP', label=' Invoices')
        graph.edge('SAP', 'GLOPPS', label=' Inventory Check')
        graph.edge('PLM', 'SAP', label=' Part Number Gen')
        graph.edge('CAD', 'PLM', label=' Drawings Upload')
    return graph

def days_since_start() -> int:
    start = st.session_state.get('start_date', date.today())
    return max(0, (date.today() - start).days)

def generate_certificate_html() -> str:
    name = st.session_state.get('user_name', 'Team Member')
    role = st.session_state.get('user_role', '')
    manager = st.session_state.get('manager_name', '')
    completion_date = date.today().strftime("%B %d, %Y")
    return f"""
    <!DOCTYPE html><html><head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');
        body {{ margin: 0; background: #f8f7f4; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .cert {{
            width: 780px; padding: 60px 70px;
            background: white;
            border: 12px solid transparent;
            border-image: linear-gradient(135deg, #4f46e5, #0ea5e9, #10b981) 1;
            text-align: center; font-family: 'Plus Jakarta Sans', sans-serif;
            box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        }}
        .logo {{ font-size: 3rem; margin-bottom: 8px; }}
        .subtitle {{ color: #6b7280; font-size: 0.9rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 32px; }}
        h1 {{ font-family: 'Playfair Display', serif; font-size: 2.6rem; color: #1f2937; margin: 0 0 8px 0; }}
        .presenter {{ color: #6b7280; font-size: 1rem; margin-bottom: 24px; }}
        .name {{ font-family: 'Playfair Display', serif; font-size: 3.2rem; color: #4f46e5; border-bottom: 2px solid #e5e7eb; padding-bottom: 12px; margin-bottom: 24px; }}
        .body-text {{ color: #374151; line-height: 1.7; font-size: 1rem; max-width: 560px; margin: 0 auto 32px; }}
        .role-badge {{ display: inline-block; background: linear-gradient(90deg, #4f46e5, #0ea5e9); color: white; padding: 8px 24px; border-radius: 999px; font-weight: 600; font-size: 0.95rem; margin-bottom: 32px; }}
        .footer {{ display: flex; justify-content: space-between; align-items: flex-end; margin-top: 40px; border-top: 1px solid #e5e7eb; padding-top: 24px; color: #9ca3af; font-size: 0.8rem; }}
        .sig {{ text-align: left; }}
        .sig-name {{ font-weight: 700; color: #374151; font-size: 0.95rem; }}
    </style></head><body>
    <div class="cert">
        <div class="logo">⚙️</div>
        <div class="subtitle">SPAE Onboarding Hub</div>
        <h1>Certificate of Completion</h1>
        <p class="presenter">This certifies that</p>
        <div class="name">{name}</div>
        <div class="role-badge">{role}</div>
        <p class="body-text">has successfully completed the SPAE onboarding programme, fulfilling all required training modules, system access tasks, and milestone activities.</p>
        <div class="footer">
            <div class="sig">
                <div class="sig-name">{manager if manager else 'Line Manager'}</div>
                <div>Line Manager</div>
            </div>
            <div style="text-align:center; font-size: 2rem;">🏆</div>
            <div style="text-align:right;">
                <div style="font-weight:700; color:#374151;">{completion_date}</div>
                <div>Date of Completion</div>
            </div>
        </div>
    </div></body></html>
    """

# --- 3. ONBOARDING WIZARD ---
def show_wizard():
    st.markdown("""
        <div style="max-width: 640px; margin: 40px auto 0 auto;">
            <div style="text-align:center; margin-bottom: 2rem;">
                <div style="font-size: 3rem;">⚙️</div>
                <h1 style="font-size: 2rem; font-weight: 800; margin: 8px 0 4px 0;">Welcome to SPAE Hub</h1>
                <p style="opacity: 0.7;">Let's personalise your onboarding experience. Takes 30 seconds.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        col = st.columns([1, 2, 1])[1]
        with col:
            with st.container(border=True):
                st.markdown("#### 👤 Your Details")
                name = st.text_input("Your First Name", placeholder="e.g. Jordan")
                role = st.selectbox("Your Role", list(ROLE_KEY_MAP.keys()))
                start = st.date_input("Your Start Date", value=date.today(), max_value=date.today() + timedelta(days=30))

                st.markdown("#### 🤝 Your Support Network")
                buddy = st.text_input("Buddy's Name", placeholder="e.g. Sarah J.")
                manager = st.text_input("Manager's Name", placeholder="e.g. Mike R.")

                st.markdown("")
                if st.button("🚀 Start My Onboarding", use_container_width=True, type="primary"):
                    if not name.strip():
                        st.error("Please enter your name to continue.")
                    else:
                        st.session_state['user_name'] = name.strip()
                        st.session_state['user_role'] = role
                        st.session_state['start_date'] = start
                        st.session_state['buddy_name'] = buddy.strip() if buddy.strip() else "Your Buddy"
                        st.session_state['manager_name'] = manager.strip() if manager.strip() else "Your Manager"
                        st.session_state['wizard_done'] = True
                        reset_user()
                        st.rerun()

# --- 4. STATE INITIALIZATION ---
if 'wizard_done' not in st.session_state:
    st.session_state['wizard_done'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "SPE (Spare Parts Engineer)"
if 'curriculum' not in st.session_state:
    st.session_state['curriculum'] = [{**t, "Status": False} for t in get_checklist_data(st.session_state['user_role'])]
if 'session_completions' not in st.session_state:
    st.session_state['session_completions'] = 0
if 'perfect_quiz' not in st.session_state:
    st.session_state['perfect_quiz'] = False
if 'quiz_state' not in st.session_state:
    st.session_state['quiz_state'] = {}
init_navigator_status()
inject_global_css()

# Show wizard if not done
if not st.session_state['wizard_done']:
    show_wizard()
    st.stop()

# --- 5. SIDEBAR ---
role_key = get_role_key(st.session_state['user_role'])
user_name = st.session_state.get('user_name', 'New Hire')
buddy_name = st.session_state.get('buddy_name', 'Your Buddy')
manager_name = st.session_state.get('manager_name', 'Your Manager')

with st.sidebar:
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:25px; margin-top:-10px;">
            <div style="background:linear-gradient(135deg,#4f46e5,#0ea5e9); padding:10px; border-radius:12px; color:white; font-size:22px; line-height:1;">⚙️</div>
            <h1 style="margin:0; padding:0; font-size:26px; font-weight:800; letter-spacing:-0.5px;">SPAE Hub</h1>
        </div>
        <div style="background:rgba(79,70,229,0.08); border-radius:0.75rem; padding:12px 14px; margin-bottom:16px; border:1px solid rgba(79,70,229,0.15);">
            <div style="font-weight:700; font-size:1rem;">👋 {user_name}</div>
            <div style="font-size:0.8rem; opacity:0.7; margin-top:2px;">{st.session_state['user_role'].split('(')[0].strip()}</div>
            <div style="font-size:0.78rem; opacity:0.6; margin-top:6px;">🤝 Buddy: <b>{buddy_name}</b></div>
            <div style="font-size:0.78rem; opacity:0.6; margin-top:2px;">👔 Manager: <b>{manager_name}</b></div>
        </div>
    """, unsafe_allow_html=True)

    days = days_since_start()
    st.markdown(f"""
        <div style="text-align:center; padding:8px; background:rgba(16,185,129,0.08); border-radius:0.5rem; margin-bottom:12px; border:1px solid rgba(16,185,129,0.2);">
            <div class="days-counter">{days}</div>
            <div style="font-size:0.8rem; opacity:0.7; font-weight:600;">day{"s" if days != 1 else ""} on the team</div>
        </div>
    """, unsafe_allow_html=True)

    selected_role = st.selectbox("Switch Role", list(ROLE_KEY_MAP.keys()), index=list(ROLE_KEY_MAP.keys()).index(st.session_state['user_role']))
    if selected_role != st.session_state['user_role']:
        st.session_state['user_role'] = selected_role
        reset_user()
        st.rerun()

    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Requests & Learning", "Checklist", "Knowledge Quiz", "Achievements", "Mentor Guide", "Good to Know"], label_visibility="collapsed")
    st.markdown("---")

    with st.popover("🆘 Directory & Help", use_container_width=True):
        st.markdown("**Emergency & Support Contacts**")
        for dept, contact in KEY_CONTACTS.items():
            st.info(f"**{dept}:** `{contact}`")

    with st.popover("🧠 Acronym Buster", use_container_width=True):
        st.markdown("**Search Internal Jargon**")
        search_term = st.text_input("Type here...", placeholder="e.g. KOLA")
        if search_term:
            query = search_term.strip().lower()
            results = {k: v for k, v in ACRONYMS.items() if query in k.lower()}
            if results:
                for k, v in results.items(): st.success(f"**{k}**: {v}")
            else:
                st.error("No matching acronyms found.")

    st.markdown("---")
    st.caption("Quick Links")
    for name_link, url in IMPORTANT_LINKS.items():
        st.markdown(f"🔗 [{name_link}]({url})")

    st.markdown("---")
    if st.button("🔄 Re-run Wizard", use_container_width=True):
        st.session_state['wizard_done'] = False
        st.rerun()

# --- 6. PAGES ---
role_key = get_role_key(st.session_state['user_role'])

# PAGE: DASHBOARD
if page == "Dashboard":
    xp, max_xp, level_name = get_xp_and_level()
    earned_badges = get_earned_badges()

    st.markdown(f"""
        <div class="hero-card">
            <span class="pill">{level_name} • {xp} / {max_xp} XP</span>
            <h1>Welcome, {user_name} 👋</h1>
            <p class="muted">Your personalised command centre for mastering the <strong>{role_key}</strong> role.
            You're on day <strong>{days_since_start()}</strong> of your journey — keep going!</p>
        </div>
    """, unsafe_allow_html=True)

    checklist_p, navigator_p, overall_p = get_overall_progress()
    overall_percent = int(overall_p * 100)
    nav_done, nav_total = get_navigator_progress()
    df = pd.DataFrame(st.session_state['curriculum'])

    kpi1, kpi2, kpi3, kpi4, chart_col = st.columns([1, 1, 1, 1, 1.2])
    with kpi1:
        with st.container(border=True):
            st.metric("Overall Progress", f"{overall_percent}%")
    with kpi2:
        with st.container(border=True):
            st.metric("Checklist", f"{int(checklist_p * 100)}%")
    with kpi3:
        with st.container(border=True):
            st.metric("Training", f"{nav_done}/{nav_total}")
    with kpi4:
        with st.container(border=True):
            st.metric("Badges Earned", f"{len(earned_badges)}/{len(ALL_BADGES)}")
    with chart_col:
        st.altair_chart(create_donut_chart(overall_p), use_container_width=True)

    if overall_percent == 100:
        st.balloons()
        st.success(f"🎉 Incredible, {user_name}! You are now a SPAE Champion. Download your certificate from the Achievements page.")

    col_action, col_badges = st.columns([3, 2])
    with col_action:
        st.markdown("### 🎯 Action Centre")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("Next Tasks")
                pending = df[df['Status'] == False].sort_values(by="Phase").head(4)
                if not pending.empty:
                    st.dataframe(pending[["Phase", "Task"]], hide_index=True, use_container_width=True)
                else:
                    st.success("All tasks complete! ✅")
        with c2:
            with st.container(border=True):
                st.subheader("Next Training")
                nav_focus = [(s, c) for s, c in [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] + [(role_key, c) for c in NAVIGATOR_COURSES[role_key]] if not st.session_state['navigator_status'].get(navigator_course_key(s, c), False)][:4]
                if nav_focus:
                    st.dataframe(pd.DataFrame([{"Type": s, "Course": c} for s, c in nav_focus]), hide_index=True, use_container_width=True)
                else:
                    st.success("All training complete! ✅")

    with col_badges:
        st.markdown("### 🏅 Recent Badges")
        badge_cols = st.columns(3)
        for i, badge in enumerate(ALL_BADGES[:6]):
            unlocked = badge['id'] in earned_badges
            with badge_cols[i % 3]:
                lock_class = "" if unlocked else "badge-locked"
                st.markdown(f"""
                    <div class="badge-card {lock_class}" title="{badge['desc']}">
                        <div class="badge-icon">{badge['icon']}</div>
                        <div class="badge-name">{badge['name']}</div>
                    </div>
                """, unsafe_allow_html=True)

# PAGE: REQUESTS & LEARNING
elif page == "Requests & Learning":
    st.markdown("## 📚 Requests & Learning")
    tab1, tab2, tab3 = st.tabs(["🔐 FAROS Access", "🎓 Navigator Hub", "🧰 Toolkit"])

    with tab1:
        st.info("💡 Use the **FAROS Portal** link in the sidebar. Attach your manager's approval email to every request.")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("🏢 Core Systems (All Roles)")
                for item in FAROS_CATALOG["Common"]: st.markdown(f"✅ {item}")
        with col2:
            with st.container(border=True):
                st.subheader(f"🛠 {role_key}-Specific Systems")
                img_col, text_col = st.columns([1.2, 3])
                with img_col:
                    st.image(THEME_IMAGES[role_key], use_container_width=True)
                with text_col:
                    for item in FAROS_CATALOG[role_key]: st.markdown(f"🔹 **{item}**")

    with tab2:
        completed_nav, total_nav = get_navigator_progress()
        st.progress(completed_nav / total_nav if total_nav > 0 else 0, text=f"Course Completion: {completed_nav}/{total_nav}")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🚨 Mandatory Training (50 XP ea)")
                for course in NAVIGATOR_COURSES["Mandatory"]:
                    key = navigator_course_key("Mandatory", course)
                    st.checkbox(course, value=st.session_state['navigator_status'].get(key, False), key=f"nav_{key}", on_change=nav_click_callback, args=("Mandatory", course))
        with c2:
            with st.container(border=True):
                st.subheader(f"🧠 {role_key} Specific (50 XP ea)")
                for course in NAVIGATOR_COURSES[role_key]:
                    key = navigator_course_key(role_key, course)
                    st.checkbox(course, value=st.session_state['navigator_status'].get(key, False), key=f"nav_{key}", on_change=nav_click_callback, args=(role_key, course))

    with tab3:
        with st.container(border=True):
            st.subheader("🔗 Essential Tools")
            for item in TOOLKIT["Common"] + TOOLKIT[role_key]: st.markdown(f"- {item}")

# PAGE: CHECKLIST
elif page == "Checklist":
    st.markdown("## ✅ Master Checklist")
    st.caption(f"Tasks personalised for **{user_name}** · Buddy: **{buddy_name}** · Manager: **{manager_name}**")
    df = pd.DataFrame(st.session_state['curriculum'])
    df['idx'] = df.index
    search_query = st.text_input("🔍 Filter tasks...", "").lower()

    phase_order = ["Day 1", "Week 1", "Month 1", "Month 2", "Month 3"]
    for phase in phase_order:
        phase_tasks = df[df['Phase'] == phase]
        if phase_tasks.empty: continue
        if search_query:
            phase_tasks = phase_tasks[phase_tasks['Task'].str.lower().str.contains(search_query) | phase_tasks['Category'].str.lower().str.contains(search_query)]
            if phase_tasks.empty: continue
        done = int(phase_tasks['Status'].sum())
        total = len(phase_tasks)
        with st.container(border=True):
            st.markdown(f"### 🗓 {phase} — {done}/{total} complete")
            st.progress(done / total)
            for _, row in phase_tasks.iterrows():
                idx = int(row['idx'])
                mentor_display = row['Mentor'].replace("Buddy", buddy_name).replace("Manager", manager_name)
                st.markdown('<div class="checklist-row">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1, 14, 4])
                with c1:
                    st.checkbox("Done", value=row['Status'], key=f"chk_{idx}", on_change=toggle_status, args=(idx,), label_visibility="collapsed")
                with c2:
                    task_text = f"~~**{row['Task']}**~~" if row['Status'] else f"**{row['Task']}**"
                    st.markdown(task_text)
                    if row.get('Tip'):
                        st.markdown(f"<div class='tip-box'>💡 {row['Tip']}</div>", unsafe_allow_html=True)
                    st.caption(f"Category: {row['Category']}")
                with c3:
                    st.markdown(f"<div style='text-align:right; margin-top:5px;'><span class='mentor-badge'>👤 {mentor_display}</span></div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# PAGE: KNOWLEDGE QUIZ
elif page == "Knowledge Quiz":
    st.markdown("## 🧠 Knowledge Quiz")
    st.markdown(f"Test what you've learned, {user_name}. Each quiz covers key concepts for the **{role_key}** role.")
    
    questions = QUIZZES.get(role_key, [])
    quiz_state = st.session_state.get('quiz_state', {})
    
    if not quiz_state:
        st.info("Answer all questions below, then submit to see your score.")
    
    with st.form("quiz_form"):
        answers = {}
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q['q']}**")
            answers[i] = st.radio("", q['options'], key=f"q_{i}", index=None, label_visibility="collapsed")
            st.markdown("")
        submitted = st.form_submit_button("📊 Submit Quiz", type="primary", use_container_width=True)

    if submitted:
        score = 0
        results = []
        all_answered = all(answers[i] is not None for i in range(len(questions)))
        if not all_answered:
            st.warning("Please answer all questions before submitting.")
        else:
            for i, q in enumerate(questions):
                selected = answers[i]
                correct = q['options'][q['answer']]
                is_correct = selected == correct
                if is_correct: score += 1
                results.append({"q": q['q'], "selected": selected, "correct": correct, "is_correct": is_correct, "explanation": q['explanation']})

            pct = int((score / len(questions)) * 100)
            if pct == 100:
                st.balloons()
                st.success(f"🎉 Perfect score! {score}/{len(questions)} — Badge unlocked: Quiz Ace 🧠")
                st.session_state['perfect_quiz'] = True
            elif pct >= 60:
                st.success(f"✅ Good work! {score}/{len(questions)} ({pct}%)")
            else:
                st.error(f"❌ {score}/{len(questions)} ({pct}%) — Review the explanations below and try again.")

            st.markdown("### Results")
            for r in results:
                if r['is_correct']:
                    st.success(f"✅ **{r['q']}**\n\n_{r['explanation']}_")
                else:
                    st.error(f"❌ **{r['q']}**\n\nYou answered: *{r['selected']}*\nCorrect: **{r['correct']}**\n\n_{r['explanation']}_")

# PAGE: ACHIEVEMENTS
elif page == "Achievements":
    st.markdown("## 🏅 Achievements")
    earned_badges = get_earned_badges()
    xp, max_xp, level_name = get_xp_and_level()
    _, _, overall_p = get_overall_progress()

    colA, colB = st.columns([2, 1])
    with colA:
        st.markdown(f"### {level_name}")
        st.progress(xp / max_xp if max_xp > 0 else 0, text=f"{xp} / {max_xp} XP — {len(earned_badges)}/{len(ALL_BADGES)} badges earned")

    with colB:
        with st.container(border=True):
            st.metric("Days on Team", days_since_start())

    st.markdown("### Your Badges")
    cols = st.columns(4)
    for i, badge in enumerate(ALL_BADGES):
        unlocked = badge['id'] in earned_badges
        lock_class = "" if unlocked else "badge-locked"
        status_text = "✅ Unlocked" if unlocked else f"🔒 {badge['desc']}"
        with cols[i % 4]:
            st.markdown(f"""
                <div class="badge-card {lock_class}">
                    <div class="badge-icon">{badge['icon']}</div>
                    <div class="badge-name">{badge['name']}</div>
                    <div class="badge-desc">{status_text}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎓 Completion Certificate")
    if overall_p >= 1.0:
        st.success("🏆 You've completed everything! Your certificate is ready.")
        cert_html = generate_certificate_html()
        st.download_button(
            label="⬇️ Download Certificate (HTML)",
            data=cert_html,
            file_name=f"SPAE_Certificate_{user_name.replace(' ','_')}.html",
            mime="text/html",
            use_container_width=True
        )
        st.components.v1.html(cert_html, height=520, scrolling=False)
    else:
        remaining = int((1.0 - overall_p) * 100)
        st.info(f"🔒 Complete 100% of your onboarding to unlock your certificate. You're {remaining}% away!")

# PAGE: MENTOR GUIDE
elif page == "Mentor Guide":
    st.markdown("## 📘 Mentor's Playbook")
    st.warning("🔒 **Restricted:** Intended for Mentors & Managers to ensure a high-quality onboarding experience.")

    tab_tips, tab_faq = st.tabs(["💡 Best Practices", "❓ New Hire FAQs"])

    with tab_tips:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("Week-by-Week Mentor Agenda")
                st.markdown("""
**Day 1:** Meet at reception. Walk them through the office personally. Sit with them during IT setup. Have lunch together.

**Week 1:** Daily 15-min check-in stand-up. Introduce to at least 5 colleagues. Shadow at least one real task together.

**Month 1:** Weekly 1:1s (30 mins). Review checklist completion together. Flag any system access blockers proactively.

**Month 2:** Shift to fortnightly 1:1s. Give structured feedback on first independent tasks. Discuss career goals.

**Month 3:** 90-day review prep. Encourage them to mentor someone newer. Celebrate the milestone.
                """)
        with c2:
            with st.container(border=True):
                st.subheader("👀 Red Flags to Watch For")
                st.markdown("""
- Signs of overload (missed stand-ups, short responses) during Week 1
- Lingering system access blockers beyond Day 5 — escalate to IT
- Misunderstanding of safety protocols (LOTO/PPE) — stop and re-train immediately
- Not asking questions — often means confusion, not confidence
- Submitting late ESRs or timesheets — habit-forming issue, address early
                """)

    with tab_faq:
        st.markdown("Common questions new hires bring to their mentors, and suggested answers.")
        all_faqs = FAQS["Common"] + FAQS.get(role_key, [])
        for faq in all_faqs:
            with st.expander(f"❓ {faq['q']}"):
                st.markdown(faq['a'])

# PAGE: GOOD TO KNOW
elif page == "Good to Know":
    tab_arch, tab_glossary, tab_faq = st.tabs(["🗺 System Architecture", "📖 Role Glossary", "❓ FAQ"])

    with tab_arch:
        st.markdown("## 🧩 System Architecture")
        st.markdown("Understanding how data flows between tools is key to mastering your workflow.")
        with st.container(border=True):
            if has_graphviz:
                st.markdown(f"**Data Flow: {st.session_state['user_role']}**")
                st.graphviz_chart(get_tech_stack_graph(role_key))
            else:
                st.error("Install graphviz to see the data flow diagram.")

    with tab_glossary:
        st.markdown("## 📖 Role Glossary")
        st.markdown(f"Key terms every **{role_key}** needs to know cold — beyond the acronym list.")
        search_gloss = st.text_input("🔍 Search terms...", "").lower()
        terms = GLOSSARY.get(role_key, {})
        for term, definition in terms.items():
            if search_gloss and search_gloss not in term.lower() and search_gloss not in definition.lower():
                continue
            with st.expander(f"**{term}**"):
                st.markdown(definition)

    with tab_faq:
        st.markdown("## ❓ Frequently Asked Questions")
        st.markdown("Real questions from new hires in your role.")
        all_faqs = FAQS["Common"] + FAQS.get(role_key, [])
        search_faq = st.text_input("🔍 Search FAQs...", "").lower()
        for faq in all_faqs:
            if search_faq and search_faq not in faq['q'].lower() and search_faq not in faq['a'].lower():
                continue
            with st.expander(f"❓ {faq['q']}"):
                st.markdown(faq['a'])
