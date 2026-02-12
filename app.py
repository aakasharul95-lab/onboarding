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
    "Tobias": "Totally Outclassed By Intelligent Aakash Significantly",
    "Aakash": "An Absolute Knight Amongst Silly Humans"
}

KEY_CONTACTS: Dict[str, str] = {
    "IT Helpdesk": "Ext. 4040",
    "HR Onboarding": "Ext. 2000",
    "Safety Officer": "Ext. 9110"
}

# --- 2. HELPER FUNCTIONS & STYLE ---


def inject_global_css():
    """
    Add theme-friendly styling: no hardcoded background colors,
    only borders, radii, slight opacity, so it works in light & dark.
    """
    st.markdown(
        """
        <style>
        /* Slightly smaller metric labels */
        [data-testid="stMetricLabel"] > div {
            font-size: 0.85rem;
        }

        /* Common card styling with theme-friendly colors */
        .hero-card, .soft-card {
            padding: 1.0rem 1.3rem;
            border-radius: 0.9rem;
            border: 1px solid rgba(148, 163, 184, 0.45);
            background-color: rgba(148, 163, 184, 0.05);
        }

        .hero-card h2 {
            margin-bottom: 0.35rem;
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

        .muted {
            opacity: 0.85;
            font-size: 0.9rem;
        }

        .sm-label {
            font-size: 0.8rem;
            opacity: 0.7;
        }

        /* Checklist row hover effect */
        .checklist-row:hover {
            background-color: rgba(148, 163, 184, 0.10);
            border-radius: 0.4rem;
        }
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
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]
    init_navigator_status()


def toggle_status(index: int) -> None:
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']


def get_tech_stack_graph(role_key: str):
    if not has_graphviz:
        return None

    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    graph.attr('node', shape='box', style='filled', fontname='Helvetica')

    if role_key == "SE":
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


def navigator_course_key(section: str, course: str) -> str:
    return f"{section}::{course}"


def init_navigator_status() -> None:
    role_key = get_role_key(st.session_state['user_role'])

    if 'navigator_status' not in st.session_state:
        st.session_state['navigator_status'] = {}

    status = st.session_state['navigator_status']

    for c in NAVIGATOR_COURSES["Mandatory"]:
        key = navigator_course_key("Mandatory", c)
        status.setdefault(key, False)

    for c in NAVIGATOR_COURSES[role_key]:
        key = navigator_course_key(role_key, c)
        status.setdefault(key, False)

    st.session_state['navigator_status'] = status


def set_navigator_course(section: str, course: str, value: bool) -> None:
    key = navigator_course_key(section, course)
    st.session_state['navigator_status'][key] = value


def get_navigator_progress() -> Tuple[int, int]:
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
    df = pd.DataFrame(st.session_state['curriculum'])
    if not df.empty:
        checklist_total = len(df)
        checklist_done = df['Status'].sum()
        checklist_progress = checklist_done / checklist_total
    else:
        checklist_progress = 0.0

    nav_done, nav_total = get_navigator_progress()
    navigator_progress = (nav_done / nav_total) if nav_total > 0 else 0.0

    w_checklist = 0.5
    w_navigator = 0.5

    overall = (w_checklist * checklist_progress) + (w_navigator * navigator_progress)
    return checklist_progress, navigator_progress, overall


def get_incomplete_navigator_courses_for_focus(max_items: int) -> List[Tuple[str, str]]:
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


def render_progress_pill(overall_percent: int) -> None:
    if overall_percent < 30:
        label = "Getting started"
    elif overall_percent < 70:
        label = "Making progress"
    elif overall_percent < 100:
        label = "Almost there"
    else:
        label = "All done"

    st.markdown(
        f"""
        <span class="pill">
            {label} • {overall_percent}%
        </span>
        """,
        unsafe_allow_html=True
    )


def render_dynamic_tip(checklist_p: float, navigator_p: float) -> None:
    if checklist_p < 0.3:
        st.info("Start with your **Day 1 logistics and IT setup** so you're fully equipped before diving into training.")
    elif navigator_p < 0.3:
        st.info("Great — you've covered initial logistics. Next, focus on **mandatory Navigator modules** (due in Week 1).")
    elif checklist_p < 1.0:
        st.info("You're doing well. Complete the remaining checklist items to unlock full access to tools and processes.")
    else:
        st.success("Your checklist is complete — keep an eye on upcoming **training modules** and field activities.")


def extract_role_label(full_label: str) -> str:
    if "(" in full_label:
        return full_label.split("(", 1)[0].strip()
    return full_label.strip()


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

selected_role = st.sidebar.selectbox(
    "Your role",
    list(ROLE_KEY_MAP.keys()),
    index=list(ROLE_KEY_MAP.keys()).index(st.session_state['user_role'])
)

if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

# Navigation directly below role selector
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Requests & Learning", "Checklist", "Mentor Guide", "Good to Know"],
    index=0
)

st.sidebar.markdown("---")

with st.sidebar.expander("🆘 Who do I call?", expanded=False):
    for dept, contact in KEY_CONTACTS.items():
        st.write(f"**{dept}:** `{contact}`")

st.sidebar.markdown("---")

# Enhanced Acronym Buster – supports partial matches
with st.sidebar.expander("🧠 Acronym Buster", expanded=False):
    search_term = st.text_input("Look up a term:", placeholder="Type acronym or part of a word...")
    if search_term:
        query = search_term.strip().lower()
        exact = {k: v for k, v in ACRONYMS.items() if k.lower() == query}
        partial = {k: v for k, v in ACRONYMS.items() if query in k.lower()}

        if exact:
            for k, v in exact.items():
                st.info(f"**{k}**: {v}")
        elif partial:
            st.write("Did you mean:")
            for k, v in partial.items():
                st.markdown(f"- **{k}** – {v}")
        else:
            st.error("No matching acronyms found.")

st.sidebar.markdown("---")

st.sidebar.subheader("🔗 Quick Links")
for name, url in IMPORTANT_LINKS.items():
    st.sidebar.markdown(f"- [{name}]({url})")

# --- 5. PAGES ---

role_key = get_role_key(st.session_state['user_role'])

# PAGE: DASHBOARD
if page == "Dashboard":
    role_label = extract_role_label(selected_role)

    # HERO
    st.markdown(
        f"""
        <div class="hero-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.75rem;">
                <div style="flex:1;">
                    <h2>Welcome, {role_label} 👋</h2>
                    <p class="muted">
                        This hub keeps track of your equipment, access requests, and training — everything you need to feel at home in AMT.
                    </p>
                </div>
                <div style="text-align:right;">
                    <span class="sm-label">Role</span><br/>
                    <span style="font-size:0.9rem;font-weight:600;">{selected_role}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")

    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_p, navigator_p, overall_p = get_overall_progress()
    overall_percent = int(overall_p * 100)

    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
    with col1:
        st.markdown("**Overall Onboarding Status**")
        render_progress_pill(overall_percent)

    with col2:
        st.metric("Checklist completion", f"{int(checklist_p * 100)}%")

    with col3:
        nav_done, nav_total = get_navigator_progress()
        st.metric("Navigator courses", f"{nav_done} / {nav_total}")

    with col4:
        if not df.empty:
            faros_tasks = df[df['Category'] == 'Access']
            if not faros_tasks.empty:
                faros_done = faros_tasks['Status'].sum()
                st.metric("Access requests done", f"{faros_done} / {len(faros_tasks)}")
            else:
                st.metric("Access requests done", "0 / 0")
        else:
            st.metric("Access requests done", "0 / 0")

    st.progress(overall_p)
    render_dynamic_tip(checklist_p, navigator_p)

    if overall_percent == 100:
        st.balloons()
        st.success("🎉 You have completed all onboarding tasks (checklist + Navigator)!")

    st.markdown("---")
    st.subheader("📅 Today’s Focus")

    if not df.empty:
        remaining_tasks = df[df['Status'] == False].copy()
        remaining_tasks["PhaseOrder"] = remaining_tasks["Phase"].apply(phase_rank)

        remaining_tasks = remaining_tasks.sort_values(
            by=["PhaseOrder", "Phase", "Category", "Task"]
        )

        N = 5
        focus_tasks = remaining_tasks.head(N)
        num_checklist_focus = len(focus_tasks)

        c_left, c_right = st.columns([1.4, 1])

        with c_left:
            if num_checklist_focus > 0:
                st.markdown("**Next checklist actions**")
                st.dataframe(
                    focus_tasks[["Phase", "Category", "Task", "Mentor"]],
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.success("No pending checklist tasks. 🎯")

        with c_right:
            remaining_slots = max(0, N - num_checklist_focus)
            nav_focus: List[Tuple[str, str]] = []
            if remaining_slots > 0:
                nav_focus = get_incomplete_navigator_courses_for_focus(remaining_slots)

            st.markdown("**Training suggestions**")
            if nav_focus:
                nav_df = pd.DataFrame(
                    [
                        {"Section": section, "Course": course}
                        for section, course in nav_focus
                    ]
                )
                st.dataframe(nav_df, hide_index=True, use_container_width=True)
            else:
                st.success("You’re on track with Navigator training. ✅")

        if num_checklist_focus == 0 and not nav_focus:
            st.success("✅ All checklist tasks and Navigator courses for your role are complete!")

        st.markdown("---")
        st.markdown("**Need a copy for your manager or HR?**")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download checklist as CSV",
            csv,
            "amt_onboarding_checklist.csv",
            "text/csv"
        )
    else:
        st.info("No checklist tasks defined yet.")

# PAGE: REQUESTS & LEARNING
elif page == "Requests & Learning":
    st.title("📚 Requests & Learning")
    st.markdown("See which tools you’ll use, and which trainings you should complete in Navigator.")

    tab1, tab2, tab3 = st.tabs(["🔐 FAROS Access Requests", "🎓 Navigator Courses", "🧰 Toolkit"])

    with tab1:
        st.info("Use the **FAROS Portal** (link in the sidebar) to request or check access status.")

        st.subheader("🏢 Standard Access (for everyone)")
        with st.expander("View core systems", expanded=True):
            render_two_column_list(FAROS_CATALOG["Common"], icon_left="✅")

        st.subheader(f"🛠 {role_key} Role-specific Access")
        with st.expander(f"View {role_key} toolset", expanded=True):
            render_two_column_list(FAROS_CATALOG[role_key], icon_left="🔹", bold=True)

    with tab2:
        st.info("Log in to **Navigator** (sidebar link) to complete these modules and mark them here as done.")

        completed_nav, total_nav = get_navigator_progress()
        st.metric("Navigator Progress", f"{completed_nav} / {total_nav} courses")

        st.subheader("🚨 Mandatory (Due in Week 1)")
        for course in NAVIGATOR_COURSES["Mandatory"]:
            key = navigator_course_key("Mandatory", course)
            checked = st.checkbox(
                label=course,
                value=st.session_state['navigator_status'].get(key, False),
                key=f"nav_{key}"
            )
            set_navigator_course("Mandatory", course, checked)

        st.markdown("---")

        st.subheader(f"🧠 {role_key} Role-specific Training")
        for course in NAVIGATOR_COURSES[role_key]:
            key = navigator_course_key(role_key, course)
            checked = st.checkbox(
                label=course,
                value=st.session_state['navigator_status'].get(key, False),
                key=f"nav_{key}"
            )
            set_navigator_course(role_key, course, checked)

    with tab3:
        st.title("🧰 Role Toolkit")

        st.subheader("🔗 Common tools")
        for item in TOOLKIT["Common"]:
            st.markdown(f"- {item}")

        st.markdown("---")

        st.subheader(f"🧩 {role_key} role-specific toolkit")
        for item in TOOLKIT[role_key]:
            st.markdown(f"- {item}")

        st.info("If you can’t access a tool, raise a request via FAROS or contact the IT Helpdesk.")

# PAGE: CHECKLIST
elif page == "Checklist":
    st.title("✅ Onboarding Checklist")

    df = pd.DataFrame(st.session_state['curriculum'])
    df['idx'] = df.index

    if df.empty:
        st.info("No checklist items defined yet.")
    else:
        st.markdown("### Phase overview")
        phase_cols = st.columns(min(len(df['Phase'].unique()), 4))
        unique_phases = df['Phase'].unique().tolist()

        for col, phase in zip(phase_cols, unique_phases):
            phase_tasks = df[df['Phase'] == phase]
            done = int(phase_tasks['Status'].sum())
            total = len(phase_tasks)
            pct = int((done / total) * 100) if total else 0
            with col:
                st.markdown(f"**{phase}**")
                st.progress(pct / 100)
                st.caption(f"{done}/{total} tasks done")

        st.markdown("---")

        for phase in unique_phases:
            with st.expander(f"🗓 {phase} tasks", expanded=True):
                phase_tasks = df[df['Phase'] == phase]
                h1, h2, h3 = st.columns([0.05, 0.6, 0.35])
                h2.caption("Task")
                h3.caption("Mentor / POC")

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
                        label = f"**{row['Task']}**"
                        if row['Status']:
                            st.markdown(f"~~{label}~~")
                        else:
                            st.markdown(label)
                    with c3:
                        st.info(f"👤 {row['Mentor']}", icon="ℹ️")

# PAGE: MENTOR GUIDE
elif page == "Mentor Guide":
    st.title("📘 Mentor’s Handbook")
    st.warning("🔒 This section is intended for Mentors & Managers.")

    st.markdown(
        "The goal of this guide is to make sure new colleagues feel supported, safe, and productive in their first weeks."
    )

    colA, colB = st.columns(2)
    with colA:
        st.subheader("💡 Best practices")
        st.markdown(
            """
            - **Day 1 is about comfort**: Ensure hardware, access badges, and coffee are sorted before deep technical topics.  
            - **Shadowing**: For the first 3 field visits, new hires should mostly observe and ask questions.  
            - **SOP Review**: For *Reman Process*, always use the latest SOP (v2.4) from SharePoint.
            """
        )

    with colB:
        st.subheader("👀 What to watch for")
        st.markdown(
            """
            - Signs of overload or confusion during Week 1 stand-ups.  
            - Access blockers (e.g., SAP, GLOPPS) preventing them from completing tasks.  
            - Safety concerns when on-site or in the workshop.
            """
        )

    st.markdown("---")
    st.caption("Need to report an issue or escalate a concern? Email: hr-onboarding@example.com")

# PAGE: GOOD TO KNOW
elif page == "Good to Know":
    st.title("🧩 Good to Know")
    st.markdown("Context, architecture and background material for your role.")

    st.subheader("System architecture")
    st.markdown(
        "Seeing how tools connect makes it easier to understand where your work fits in the bigger AMT picture."
    )

    if has_graphviz:
        st.markdown(f"**Workflow map for:** {st.session_state['user_role']}")
        graph = get_tech_stack_graph(role_key)

        try:
            st.graphviz_chart(graph)
            st.info("Tip: Use the fullscreen button on the chart to inspect all nodes comfortably.")
        except Exception:
            st.warning("Graphviz is installed, but rendering failed. Check if the system-level Graphviz is installed.")
    else:
        st.warning("Graphviz is not installed. The system map cannot be displayed.")
        with st.expander("How to install Graphviz"):
            st.code("pip install graphviz\n# plus OS-level graphviz package, e.g.\n# sudo apt-get install graphviz", language="bash")







