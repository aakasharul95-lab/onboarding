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

# Phase priority for ordering tasks
PHASE_PRIORITY: List[str] = ["Day 1", "Week 1", "Month 1", "Month 2"]

# EXTRACTED FROM: AMT Faros Request Catalogue
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
        "Agile PLM (Product Lifecycle Mgmt)",
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

# NAVIGATOR TRAINING COURSES
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

# TOOLKIT (Tidinfo, SCORE, etc.)
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

# UPDATED ACRONYMS WITH TOBIAS & AAKASH
ACRONYMS: Dict[str, str] = {
    "AI": "Aakash Intelligence",
    "KOLA": "Key On-Line Access (Parts DB)",
    "LOTO": "Lock Out Tag Out",
    "MOM": "Mobile Order Management",
    "SAP": "Systems, Applications, and Products",
    "SPE": "Spare Parts Engineer",
    "SE": "Service Engineer",
    "Tobias": "Totally Outclassed By Intelligent Aakash Significantly",
    "Aakash": "An Absolute Knight Amongst Silly Humans"
}

KEY_CONTACTS: Dict[str, str] = {
    "IT Helpdesk": "Ext. 4040",
    "HR Onboarding": "Ext. 2000",
    "Safety Officer": "Ext. 9110"
}

# --- 2. HELPER FUNCTIONS ---

def get_role_key(full_role: str) -> str:
    """Map the UI role label to a short role key, defaulting to SPE."""
    return ROLE_KEY_MAP.get(full_role, "SPE")


def phase_rank(phase: str) -> int:
    """Return numeric ordering for phases based on PHASE_PRIORITY."""
    return PHASE_PRIORITY.index(phase) if phase in PHASE_PRIORITY else len(PHASE_PRIORITY)


def get_checklist_data(full_role: str) -> List[Dict]:
    """Return base checklist + role-specific items."""
    role_key = get_role_key(full_role)

    tasks: List[Dict] = [
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


def reset_user() -> None:
    """Reset curriculum and Navigator status when user role changes."""
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]
    init_navigator_status()


def toggle_status(index: int) -> None:
    """Toggle checklist status for a given index."""
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']


def get_tech_stack_graph(role_key: str):
    if not has_graphviz:
        return None

    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    graph.attr('node', shape='box', style='filled', fontname='Helvetica')

    if role_key == "SE":
        # Service Engineer Workflow
        graph.node('C', 'Customer Site', fillcolor='#e1f5fe')
        graph.node('SF', 'Salesforce (CRM)', shape='ellipse', fillcolor='#fff9c4')
        graph.node('SAP', 'SAP Service Module', shape='ellipse', fillcolor='#fff9c4')
        graph.node('MOM', 'MOM App (Mobile)', fillcolor='#c8e6c9')
        graph.node('KOLA', 'KOLA (Parts DB)', shape='cylinder', fillcolor='#f0f4c3')

        graph.edge('C', 'SF', label='Ticket Created')
        graph.edge('SF', 'SAP', label='Job Dispatch')
        graph.edge('SAP', 'MOM', label='Work Order Sync')
        graph.edge('MOM', 'KOLA', label='Lookup Parts')
        graph.edge('MOM', 'SAP', label='Submit Timesheet')

    else:
        # Spare Parts Engineer Workflow
        graph.node('V', 'Vendor / Supplier', fillcolor='#e1f5fe')
        graph.node('SAP', 'SAP GUI (ERP)', shape='ellipse', fillcolor='#fff9c4')
        graph.node('PLM', 'Agile PLM', shape='ellipse', fillcolor='#e1bee7')
        graph.node('CAD', 'Creo / Vault', fillcolor='#c8e6c9')
        graph.node('GLOPPS', 'GLOPPS (Logistics)', shape='cylinder', fillcolor='#f0f4c3')

        graph.edge('V', 'SAP', label='Invoices')
        graph.edge('SAP', 'GLOPPS', label='Inventory Check')
        graph.edge('PLM', 'SAP', label='Part Number Gen')
        graph.edge('CAD', 'PLM', label='Drawings Upload')

    return graph


# --- NAVIGATOR STATUS HELPERS ---

def navigator_course_key(section: str, course: str) -> str:
    """Unique key for each Navigator course."""
    return f"{section}::{course}"


def init_navigator_status() -> None:
    """
    Ensure st.session_state['navigator_status'] exists and has
    entries for all courses (default False) for the current role.
    """
    role_key = get_role_key(st.session_state['user_role'])

    if 'navigator_status' not in st.session_state:
        st.session_state['navigator_status'] = {}

    status = st.session_state['navigator_status']

    # Mandatory
    for c in NAVIGATOR_COURSES["Mandatory"]:
        key = navigator_course_key("Mandatory", c)
        status.setdefault(key, False)

    # Role-specific
    for c in NAVIGATOR_COURSES[role_key]:
        key = navigator_course_key(role_key, c)
        status.setdefault(key, False)

    st.session_state['navigator_status'] = status


def set_navigator_course(section: str, course: str, value: bool) -> None:
    """Set completion status for a Navigator course."""
    key = navigator_course_key(section, course)
    st.session_state['navigator_status'][key] = value


def get_navigator_progress() -> Tuple[int, int]:
    """
    Compute number completed / total for current role + mandatory.
    Returns (completed, total).
    """
    role_key = get_role_key(st.session_state['user_role'])
    status = st.session_state.get('navigator_status', {})

    all_courses = (
        [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] +
        [(role_key, c) for c in NAVIGATOR_COURSES[role_key]]
    )

    total = len(all_courses)
    completed = 0
    for section, course in all_courses:
        key = navigator_course_key(section, course)
        if status.get(key, False):
            completed += 1
    return completed, total


def get_overall_progress() -> Tuple[float, float, float]:
    """
    Combine checklist and Navigator progress into one overall %.
    Returns (checklist_progress, navigator_progress, overall_progress).
    """
    # Checklist progress
    df = pd.DataFrame(st.session_state['curriculum'])
    if not df.empty:
        checklist_total = len(df)
        checklist_done = df['Status'].sum()
        checklist_progress = checklist_done / checklist_total
    else:
        checklist_progress = 0.0

    # Navigator progress
    nav_done, nav_total = get_navigator_progress()
    navigator_progress = (nav_done / nav_total) if nav_total > 0 else 0.0

    # Weights (adjust as you like)
    w_checklist = 0.5
    w_navigator = 0.5

    overall = (w_checklist * checklist_progress) + (w_navigator * navigator_progress)
    return checklist_progress, navigator_progress, overall


def get_incomplete_navigator_courses_for_focus(max_items: int) -> List[Tuple[str, str]]:
    """
    Return a list of (section, course) for incomplete Navigator courses,
    limited to max_items.
    Priority: Mandatory first, then role-specific.
    """
    role_key = get_role_key(st.session_state['user_role'])
    status = st.session_state.get('navigator_status', {})

    ordered = (
        [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] +
        [(role_key, c) for c in NAVIGATOR_COURSES[role_key]]
    )

    incomplete: List[Tuple[str, str]] = []
    for section, course in ordered:
        key = navigator_course_key(section, course)
        if not status.get(key, False):
            incomplete.append((section, course))
        if len(incomplete) >= max_items:
            break

    return incomplete


def render_two_column_list(items: List[str], icon_left: str = "✅", icon_right: str = None, bold: bool = False) -> None:
    """
    Render items across two columns, with optional icons and bold text.
    """
    if icon_right is None:
        icon_right = icon_left

    c1, c2 = st.columns(2)
    half = (len(items) + 1) // 2

    for item in items[:half]:
        text = f"{icon_left} **{item}**" if bold else f"{icon_left} {item}"
        c1.markdown(text)

    for item in items[half:]:
        text = f"{icon_right} **{item}**" if bold else f"{icon_right} {item}"
        c2.markdown(text)


# --- 3. STATE INITIALIZATION ---

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "SPE (Spare Parts Engineer)"

if 'curriculum' not in st.session_state:
    raw_data_init = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data_init]

# Initialize navigator status once user_role exists
init_navigator_status()

# --- 4. SIDEBAR ---

st.sidebar.title("🚀 AMT Onboarding")

selected_role = st.sidebar.selectbox(
    "Select Role:",
    list(ROLE_KEY_MAP.keys()),
    index=list(ROLE_KEY_MAP.keys()).index(st.session_state['user_role'])
)

if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

page = st.sidebar.radio("Navigate", ["Dashboard", "Requests & Learning", "Checklist", "Mentor Guide", "Good to Know"])

st.sidebar.markdown("---")
with st.sidebar.expander("🆘 Who do I call?"):
    for dept, contact in KEY_CONTACTS.items():
        st.write(f"**{dept}:** `{contact}`")

st.sidebar.markdown("---")
# CASE-INSENSITIVE ACRONYM BUSTER
with st.sidebar.expander("🧠 Acronym Buster"):
    search_term = st.text_input("Look up a term:", placeholder="e.g. MOM, Tobias, Aakash")
    if search_term:
        query = search_term.strip().lower()
        found = False

        for key, value in ACRONYMS.items():
            if key.lower() == query:
                st.info(f"**{key}**: {value}")
                found = True
                break

        if not found:
            st.error("Unknown term.")

st.sidebar.markdown("---")
st.sidebar.subheader("🔗 Quick Links")
for name, url in IMPORTANT_LINKS.items():
    st.sidebar.markdown(f"[{name}]({url})")

# --- 5. PAGES ---

role_key = get_role_key(st.session_state['user_role'])

# PAGE: DASHBOARD
if page == "Dashboard":
    st.title(f"Welcome, {selected_role.split('(')[0].strip()}! 👋")

    df = pd.DataFrame(st.session_state['curriculum'])

    # Combined progress
    checklist_p, navigator_p, overall_p = get_overall_progress()
    overall_percent = int(overall_p * 100)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Onboarding Progress", f"{overall_percent}%")

    with col2:
        # Checklist-specific info
        if not df.empty:
            faros_tasks = df[df['Category'] == 'Access']
            if not faros_tasks.empty:
                faros_done = faros_tasks['Status'].sum()
                st.metric("Access Requests (Checklist)", f"{faros_done} / {len(faros_tasks)}")
            else:
                st.metric("Access Requests (Checklist)", "0 / 0")
        else:
            st.metric("Access Requests (Checklist)", "0 / 0")

    with col3:
        # Navigator-specific metric
        nav_done, nav_total = get_navigator_progress()
        st.metric("Navigator Courses", f"{nav_done} / {nav_total}")

    # Progress bar reflects overall progress
    st.progress(overall_p)

    # Sub progress
    st.caption(
        f"Checklist completion: {int(checklist_p * 100)}%  •  "
        f"Navigator completion: {int(navigator_p * 100)}%"
    )

    # Celebration if overall is 100%
    if overall_percent == 100:
        st.balloons()
        st.success("🎉 You have completed all onboarding tasks (checklist + Navigator)!")

    # --- Today's Focus (Checklist + Navigator) ---
    st.subheader("📅 Today's Focus")

    if not df.empty:
        remaining_tasks = df[df['Status'] == False].copy()
        remaining_tasks["PhaseOrder"] = remaining_tasks["Phase"].apply(phase_rank)

        remaining_tasks = remaining_tasks.sort_values(
            by=["PhaseOrder", "Phase", "Category", "Task"]
        )

        N = 5
        focus_tasks = remaining_tasks.head(N)
        num_checklist_focus = len(focus_tasks)

        if num_checklist_focus > 0:
            st.markdown("**Checklist – next tasks (by phase priority)**")
            st.dataframe(
                focus_tasks[["Phase", "Category", "Task", "Mentor"]],
                hide_index=True,
                use_container_width=True
            )

        # Fill remaining slots with Navigator courses if any
        remaining_slots = max(0, N - num_checklist_focus)
        nav_focus: List[Tuple[str, str]] = []
        if remaining_slots > 0:
            nav_focus = get_incomplete_navigator_courses_for_focus(remaining_slots)

        if nav_focus:
            st.markdown("---")
            st.markdown("**Navigator – suggested courses to complete next**")
            nav_df = pd.DataFrame(
                [
                    {"Section": section, "Course": course}
                    for section, course in nav_focus
                ]
            )
            st.dataframe(nav_df, hide_index=True, use_container_width=True)

        if num_checklist_focus == 0 and not nav_focus:
            st.success("✅ All checklist tasks and Navigator courses for your role are complete!")
    else:
        st.info("No checklist tasks defined yet.")

# PAGE: REQUESTS & LEARNING
elif page == "Requests & Learning":
    st.title("📚 Requests & Learning")
    st.markdown("Here you can find your IT Access Requests, Mandatory Training, and Toolkit.")

    # 3 tabs: FAROS, Navigator, Toolkit
    tab1, tab2, tab3 = st.tabs(["🔐 FAROS Access Requests", "🎓 Navigator Courses", "🧰 Toolkit"])

    # --- TAB 1: FAROS ACCESS ---
    with tab1:
        st.info("Use the **FAROS Portal** link in the sidebar to request these tools.")

        st.subheader("🏢 Standard Access (Required for All)")
        with st.expander("View Core Systems List", expanded=True):
            render_two_column_list(FAROS_CATALOG["Common"], icon_left="✅")

        st.subheader(f"🛠 {role_key} Specialized Tools")
        with st.expander(f"View {role_key} Toolset", expanded=True):
            render_two_column_list(FAROS_CATALOG[role_key], icon_left="🔹", bold=True)

    # --- TAB 2: NAVIGATOR COURSES (with checkboxes) ---
    with tab2:
        st.info("Log in to **Navigator** (link in sidebar) to complete these modules.")

        completed_nav, total_nav = get_navigator_progress()
        st.metric("Navigator Progress", f"{completed_nav} / {total_nav} courses")

        st.subheader("🚨 Mandatory Compliance (Due Week 1)")
        for course in NAVIGATOR_COURSES["Mandatory"]:
            key = navigator_course_key("Mandatory", course)
            checked = st.checkbox(
                label=course,
                value=st.session_state['navigator_status'].get(key, False),
                key=f"nav_{key}"
            )
            set_navigator_course("Mandatory", course, checked)

        st.markdown("---")

        st.subheader(f"🧠 {role_key} Role-Specific Training")
        for course in NAVIGATOR_COURSES[role_key]:
            key = navigator_course_key(role_key, course)
            checked = st.checkbox(
                label=course,
                value=st.session_state['navigator_status'].get(key, False),
                key=f"nav_{key}"
            )
            set_navigator_course(role_key, course, checked)

    # --- TAB 3: TOOLKIT ---
    with tab3:
        st.title("🧰 Role Toolkit")

        st.subheader("🔗 Common Tools")
        for item in TOOLKIT["Common"]:
            st.markdown(f"- {item}")

        st.markdown("---")

        st.subheader(f"🧩 {role_key} Role-Specific Toolkit")
        for item in TOOLKIT[role_key]:
            st.markdown(f"- {item}")

        st.info("If you can't access a tool, raise a request via FAROS or contact the IT Helpdesk.")

# PAGE: CHECKLIST
elif page == "Checklist":
    st.title("✅ Onboarding Checklist")
    df = pd.DataFrame(st.session_state['curriculum'])
    df['idx'] = df.index

    phases = df['Phase'].unique().tolist()
    for phase in phases:
        with st.expander(f"🗓 {phase} Tasks", expanded=True):
            phase_tasks = df[df['Phase'] == phase]
            h1, h2, h3 = st.columns([0.05, 0.6, 0.35])
            h2.caption("TASK")
            h3.caption("MENTOR / POC")

            for _, row in phase_tasks.iterrows():
                idx = int(row['idx'])
                c1, c2, c3 = st.columns([0.05, 0.6, 0.35])
                with c1:
                    st.checkbox(
                        "Done",
                        value=row['Status'],
                        key=f"chk_{idx}",
                        on_change=toggle_status,
                        args=(idx,),
                        label_visibility="collapsed"
                    )
                with c2:
                    if row['Status']:
                        st.markdown(f"~~{row['Task']}~~")
                    else:
                        st.write(f"**{row['Task']}**")
                with c3:
                    st.info(f"👤 {row['Mentor']}", icon="ℹ️")

# PAGE: MENTOR GUIDE
elif page == "Mentor Guide":
    st.title("📘 Mentor's Handbook")
    st.warning("🔒 This section is intended for Mentors & Managers to review.")

    st.subheader("💡 Best Practices")
    st.markdown("""
    * **Day 1 is about comfort:** Ensure the new hire has their hardware and coffee access before diving into technical topics.
    * **Shadowing:** For the first 3 field visits, the new hire should only observe. Do not assign them active tasks yet.
    * **SOP Review:** When teaching *Reman Process*, please use the updated PDF (v2.4) located in SharePoint.
    """)
    st.caption("Need to report an issue? Contact the Onboarding Lead at hr-onboarding@example.com")

# PAGE: GOOD TO KNOW
elif page == "Good to Know":
    st.title("🧩 Good to Know")
    st.markdown("Context and Reference material for your role.")

    st.subheader("System Architecture")
    st.markdown("Understanding how our tools connect helps you understand the workflow.")

    if has_graphviz:
        st.write(f"**Workflow for: {st.session_state['user_role']}**")

        graph = get_tech_stack_graph(role_key)
        st.graphviz_chart(graph)
        st.info("💡 **Tip:** Click the 'View Fullscreen' arrow on the chart to see details clearly.")
    else:
        st.warning("⚠️ Graphviz is not installed. The system map cannot be displayed.")
        with st.expander("How to install Graphviz"):
            st.code("pip install graphviz\n# plus OS-level graphviz package if needed", language="bash")







