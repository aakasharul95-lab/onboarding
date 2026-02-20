import streamlit as st
import pandas as pd
from typing import List, Tuple, Dict

# --- CONFIGURATION ---
st.set_page_config(page_title="AMT Onboarding Hub", layout="wide", page_icon="🚀")

# --- 0. LIBRARY CHECK (CRASH GUARD) ---
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

PHASE_PRIORITY: List[str] = ["Day 1", "Week 1", "Month 1", "Month 2"]

FAROS_CATALOG: Dict[str, List[str]] = {
    "Common": [
        "Microsoft 365 (Outlook, Teams, Excel)",
        "Cisco AnyConnect VPN (Remote Access)",
        "Workday (HR & Payroll)",
        "Concur (Travel & Expenses)",
        "ServiceNow (IT Helpdesk)",
        "Slack (Internal Comm Channels)",
        "LastPass Enterprise (Password Manager)",
        "Zoom (Video Conferencing)",
        "SharePoint: Global Engineering"
    ],
    "SPE": [
        "SAP GUI: ERP System (Production)",
        "GLOPPS (Global Logistics & Parts)",
        "KOLA (Parts Documentation DB)",
        "RUMBA (Legacy Parts Lookup)",
        "Autodesk Vault (CAD Data Management)",
        "Creo MCAD (View & Edit License)",
        "Agile PLM: Product Lifecycle Mgmt",
        "PowerBI Desktop (Inventory Analytics)"
    ],
    "SE": [
        "SAP Service Cloud (C4C)",
        "MOM (Mobile Order Management App)",
        "LOTO Safety Portal (Lock Out Tag Out)",
        "ESR Tool (Electronic Service Report)",
        "Hydraulic Schematics Viewer (HSV)",
        "Salesforce CRM (Customer History)",
        "ServiceMax (Field Dispatch)",
        "Fleet Management System (Vehicle Logs)"
    ]
}

NAVIGATOR_COURSES: Dict[str, List[str]] = {
    "Mandatory": [
        "Global Data Privacy & GDPR (30 mins)",
        "Cybersecurity Awareness: Phishing (15 mins)",
        "Code of Conduct: Anti-Bribery (45 mins)",
        "Diversity & Inclusion Basics (20 mins)",
        "Health & Safety: Office Ergonomics (15 mins)"
    ],
    "SPE": [
        "SAP ERP: Supply Chain Basics (60 mins)",
        "Logistics 101: Incoterms (30 mins)",
        "Agile PLM: Document Control (45 mins)"
    ],
    "SE": [
        "Field Safety: Electrical Hazards (60 mins)",
        "Defensive Driving Certification (External)",
        "Customer Service: Handling Conflict (30 mins)"
    ]
}

TOOLKIT: Dict[str, List[str]] = {
    "Common": [
        "Tidinfo – Technical information portal",
        "SCORE – Service & Customer Operations Reporting Engine"
    ],
    "SPE": [
        "Parts Costing Calculator",
        "BOM Comparison Utility"
    ],
    "SE": [
        "Service Checklists Mobile Pack",
        "Field Report Template Pack"
    ]
}

IMPORTANT_LINKS: Dict[str, str] = {
    "FAROS (Access Portal)": "https://faros.internal.example.com",
    "Navigator (Learning)": "https://navigator.internal.example.com",
    "Workday (HR)": "https://www.myworkday.com",
    "Concur (Expenses)": "https://www.concursolutions.com"
}

ACRONYMS: Dict[str, str] = {
    "AI": "Aakash Intelligence",
    "KOLA": "Key On-Line Access (Parts DB)",
    "LOTO": "Lock Out Tag Out",
    "MOM": "Mobile Order Management",
    "SAP": "Systems, Applications, and Products",
    "SPE": "Spare Parts Engineer",
    "SE": "Service Engineer",
}

KEY_CONTACTS: Dict[str, str] = {
    "IT Helpdesk": "Ext. 4040",
    "HR Onboarding": "Ext. 2000",
    "Safety Officer": "Ext. 9110"
}

# --- 2. HELPER FUNCTIONS & STYLE ---

def inject_global_css():
    st.markdown(
        """
        <style>
        [data-testid="stMetricLabel"] > div { font-size: 0.85rem; }
        .hero-card, .soft-card {
            padding: 1.0rem 1.3rem;
            border-radius: 0.9rem;
            border: 1px solid rgba(148, 163, 184, 0.45);
            background-color: rgba(148, 163, 184, 0.05);
        }
        .pill {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            border: 1px solid rgba(129, 140, 248, 0.7);
            background-color: rgba(79, 70, 229, 0.06);
            color: rgba(129, 140, 248, 0.95);
            margin-right: 0.35rem;
        }
        .muted { opacity: 0.85; font-size: 0.9rem; }
        .sm-label { font-size: 0.8rem; opacity: 0.7; }
        .checklist-row {
            padding: 0.15rem 0.3rem;
            border-radius: 0.4rem;
            transition: background-color 120ms ease;
        }
        .checklist-row:hover { background-color: rgba(148, 163, 184, 0.12); }
        </style>
        """,
        unsafe_allow_html=True
    )

def get_role_key(full_role: str) -> str:
    return ROLE_KEY_MAP.get(full_role, "SPE")

def phase_rank(phase: str) -> int:
    return PHASE_PRIORITY.index(phase) if phase in PHASE_PRIORITY else len(PHASE_PRIORITY)

def get_checklist_data(full_role: str) -> List[Dict]:
    role_key = get_role_key(full_role)
    tasks = [
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Safety Shoes & PPE", "Mentor": "Office Admin", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Laptop, Mobile & Headset", "Mentor": "IT Support", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "IT Setup", "Task": "Initial Windows Login", "Mentor": "IT Support", "Type": "Action"},
        {"Phase": "Day 1", "Category": "Orientation", "Task": "Office Tour (Fire Exits)", "Mentor": "Buddy: Sarah J.", "Type": "Meeting"},
        {"Phase": "Week 1", "Category": "HR", "Task": "Submit Bank Details", "Mentor": "HR Dept", "Type": "Admin"},
        {"Phase": "Week 1", "Category": "Intro", "Task": "Team Intro Presentation", "Mentor": "Manager: Mike R.", "Type": "Meeting"},
    ]
    if role_key == "SE":
        tasks.extend([
            {"Phase": "Week 1", "Category": "Access", "Task": "Request: SAP Service Module", "Mentor": "Tech Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "LOTO Certification", "Mentor": "Safety Officer", "Type": "Training"},
        ])
    elif role_key == "SPE":
        tasks.extend([
            {"Phase": "Week 1", "Category": "Access", "Task": "Request: GLOPPS Access", "Mentor": "Logistics Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "Reman Process SOP", "Mentor": "Senior SPE", "Type": "Training"},
        ])
    return tasks

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

# --- CALLBACK FUNCTIONS ---

def reset_user() -> None:
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]
    st.session_state['navigator_status'] = {}
    init_navigator_status()

def toggle_status(index: int) -> None:
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

def update_navigator_callback(section: str, course: str):
    """Updates the session state immediately when checkbox is toggled."""
    key = navigator_course_key(section, course)
    # The checkbox widget automatically updates session_state[widget_key].
    # We sync our dictionary here.
    widget_key = f"nav_cb_{key}"
    st.session_state['navigator_status'][key] = st.session_state[widget_key]

# --- PROGRESS LOGIC ---

def get_navigator_progress() -> Tuple[int, int]:
    role_key = get_role_key(st.session_state['user_role'])
    status = st.session_state.get('navigator_status', {})
    all_courses = (
        [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] +
        [(role_key, c) for c in NAVIGATOR_COURSES[role_key]]
    )
    total = len(all_courses)
    completed = sum(1 for s, c in all_courses if status.get(navigator_course_key(s, c), False))
    return completed, total

def get_overall_progress() -> Tuple[float, float, float]:
    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_progress = df['Status'].sum() / len(df) if not df.empty else 0.0
    nav_done, nav_total = get_navigator_progress()
    navigator_progress = (nav_done / nav_total) if nav_total > 0 else 0.0
    overall = (0.5 * checklist_progress) + (0.5 * navigator_progress)
    return checklist_progress, navigator_progress, overall

def extract_role_label(full_label: str) -> str:
    return full_label.split("(", 1)[0].strip() if "(" in full_label else full_label.strip()

# --- 3. STATE INITIALIZATION ---

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "SPE (Spare Parts Engineer)"
if 'curriculum' not in st.session_state:
    raw_data_init = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data_init]

init_navigator_status()
inject_global_css()

# --- 4. SIDEBAR ---

st.sidebar.title("🚀 AMT Onboarding Hub")
selected_role = st.sidebar.selectbox("Your role", list(ROLE_KEY_MAP.keys()), 
                                    index=list(ROLE_KEY_MAP.keys()).index(st.session_state['user_role']))

if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

page = st.sidebar.radio("Navigate", ["Dashboard", "Requests & Learning", "Checklist", "Mentor Guide", "Good to Know"])

# --- 5. PAGES ---
role_key = get_role_key(st.session_state['user_role'])

if page == "Dashboard":
    role_label = extract_role_label(selected_role)
    st.title(f"Welcome, {role_label} 👋")
    
    checklist_p, navigator_p, overall_p = get_overall_progress()
    nav_done, nav_total = get_navigator_progress()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Progress", f"{int(overall_p * 100)}%")
    col2.metric("Checklist", f"{int(checklist_p * 100)}%")
    col3.metric("Navigator", f"{nav_done} / {nav_total}")
    st.progress(overall_p)

elif page == "Requests & Learning":
    st.title("📚 Requests & Learning")
    tab1, tab2, tab3 = st.tabs(["🔐 Access Requests", "🎓 Navigator Courses", "🧰 Toolkit"])

    with tab2:
        # Re-calculating here ensures the metric is fresh
        completed_nav, total_nav = get_navigator_progress()
        st.metric("Navigator Progress", f"{completed_nav} / {total_nav} courses")
        
        st.info("Log in to Navigator to complete these modules.")

        st.subheader("🚨 Mandatory (Due in Week 1)")
        for course in NAVIGATOR_COURSES["Mandatory"]:
            key = navigator_course_key("Mandatory", course)
            st.checkbox(
                label=course,
                value=st.session_state['navigator_status'].get(key, False),
                key=f"nav_cb_{key}", # Unique key for the widget
                on_change=update_navigator_callback,
                args=("Mandatory", course)
            )

        st.markdown("---")

        st.subheader(f"🧠 {role_key} Role-specific Training")
        for course in NAVIGATOR_COURSES[role_key]:
            key = navigator_course_key(role_key, course)
            st.checkbox(
                label=course,
                value=st.session_state['navigator_status'].get(key, False),
                key=f"nav_cb_{key}",
                on_change=update_navigator_callback,
                args=(role_key, course)
            )

elif page == "Checklist":
    st.title("✅ Onboarding Checklist")
    df = pd.DataFrame(st.session_state['curriculum'])
    for i, row in df.iterrows():
        c1, c2 = st.columns([0.1, 0.9])
        c1.checkbox("Done", value=row['Status'], key=f"chk_{i}", on_change=toggle_status, args=(i,), label_visibility="collapsed")
        st.write(f"**{row['Task']}** - {row['Phase']}")

else:
    st.info("Select a page from the sidebar to continue.")
