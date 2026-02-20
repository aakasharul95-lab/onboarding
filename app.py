import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Tuple, Dict

# --- CONFIGURATION ---
st.set_page_config(page_title="AMT Onboarding Hub", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

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
    "Tobias": "Totally Outclassed By Intelligent Aakash Significantly", "Aakash": "An Absolute Knight Amongst Silly Humans"
}

KEY_CONTACTS: Dict[str, str] = {
    "IT Helpdesk": "Ext. 4040", "HR Onboarding": "Ext. 2000", "Safety Officer": "Ext. 9110"
}

# --- 2. HELPER FUNCTIONS & ADVANCED UI STYLING ---

def inject_global_css():
    st.markdown(
        """
        <style>
        /* Top Gradient Accent - Stays vibrant in both modes */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #4f46e5, #0ea5e9, #10b981);
            z-index: 99999;
        }
        
        /* Metric Typography - Uses native text variables */
        [data-testid="stMetricValue"] { font-weight: 800; font-size: 2.2rem; color: var(--text-color); }
        [data-testid="stMetricLabel"] > div { font-size: 0.95rem; font-weight: 600; opacity: 0.8; }

        /* Premium Hero Card - Adapts seamlessly to Light/Dark */
        .hero-card {
            padding: 2.0rem;
            border-radius: 1rem;
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 15px -5px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .hero-card h1 { 
            margin-bottom: 0.2rem; 
            font-size: 2.5rem; 
            color: var(--text-color); 
        }

        /* Animated Pills - Uses native primary color */
        .pill {
            display: inline-flex; align-items: center; justify-content: center;
            padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700;
            border: 1px solid var(--primary-color); 
            background-color: transparent; 
            color: var(--primary-color);
        }

        .muted { opacity: 0.85; font-size: 1.0rem; line-height: 1.6; }
        
        /* Interactive Task Row - Auto-adjusts background */
        .checklist-row {
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            border-left: 3px solid transparent;
            background-color: var(--secondary-background-color);
            margin-bottom: 0.5rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .checklist-row:hover {
            border-left: 3px solid var(--primary-color);
            transform: translateX(4px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Adaptive Mentor Badge */
        .mentor-badge {
            background-color: rgba(128, 128, 128, 0.15);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            color: var(--text-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def create_donut_chart(progress: float):
    """Creates a sleek, animated donut chart that looks good in light and dark mode."""
    progress_pct = round(progress * 100)
    source = pd.DataFrame({
        "Category": ["Completed", "Remaining"],
        "Value": [progress_pct, 100 - progress_pct]
    })
    
    # Using rgba with transparency for the "Remaining" track makes it look native in any theme
    chart = alt.Chart(source).mark_arc(innerRadius=60, cornerRadius=15).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Category", type="nominal",
                        scale=alt.Scale(domain=["Completed", "Remaining"], range=["#3b82f6", "rgba(128, 128, 128, 0.15)"]),
                        legend=None),
        tooltip=['Category', 'Value']
    ).properties(width=220, height=220)
    return chart

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

# --- INSTANT SYNC & GAMIFICATION CALLBACKS ---
def toggle_status(index: int) -> None:
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']
    if st.session_state['curriculum'][index]['Status']:
        task_name = st.session_state['curriculum'][index]['Task']
        st.toast(f"Boom! '{task_name}' is done. Great job! 🎉", icon="🔥")

def nav_click_callback(section: str, course: str) -> None:
    key = navigator_course_key(section, course)
    is_done = st.session_state[f"nav_{key}"]
    st.session_state['navigator_status'][key] = is_done
    if is_done:
        st.toast(f"Knowledge leveled up! Completed '{course}'. 🧠", icon="🚀")

def get_tech_stack_graph(role_key: str):
    if not has_graphviz: return None
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR', bgcolor='transparent')
    graph.attr('node', shape='box', style='filled', fontname='Helvetica, sans-serif', rx='5', ry='5')
    if role_key == "SE":
        graph.node('C', 'Customer Site', fillcolor='#bae6fd', color='#0284c7')
        graph.node('SF', 'Salesforce (CRM)', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('SAP', 'SAP Service Module', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('MOM', 'MOM App (Mobile)', fillcolor='#bbf7d0', color='#16a34a')
        graph.node('KOLA', 'KOLA (Parts DB)', shape='cylinder', fillcolor='#e9d5ff', color='#9333ea')
        graph.edge('C', 'SF', label='Ticket Created')
        graph.edge('SF', 'SAP', label='Job Dispatch')
        graph.edge('SAP', 'MOM', label='Work Order Sync')
        graph.edge('MOM', 'KOLA', label='Lookup Parts')
        graph.edge('MOM', 'SAP', label='Submit Timesheet')
    else:
        graph.node('V', 'Vendor / Supplier', fillcolor='#bae6fd', color='#0284c7')
        graph.node('SAP', 'SAP GUI (ERP)', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('PLM', 'Agile PLM', shape='ellipse', fillcolor='#e9d5ff', color='#9333ea')
        graph.node('CAD', 'Creo / Vault', fillcolor='#bbf7d0', color='#16a34a')
        graph.node('GLOPPS', 'GLOPPS (Logistics)', shape='cylinder', fillcolor='#fecdd3', color='#e11d48')
        graph.edge('V', 'SAP', label='Invoices')
        graph.edge('SAP', 'GLOPPS', label='Inventory Check')
        graph.edge('PLM', 'SAP', label='Part Number Gen')
        graph.edge('CAD', 'PLM', label='Drawings Upload')
    return graph

def navigator_course_key(section: str, course: str) -> str: return f"{section}::{course}"

def init_navigator_status() -> None:
    role_key = get_role_key(st.session_state['user_role'])
    if 'navigator_status' not in st.session_state: st.session_state['navigator_status'] = {}
    status = st.session_state['navigator_status']
    for c in NAVIGATOR_COURSES["Mandatory"]: status.setdefault(navigator_course_key("Mandatory", c), False)
    for c in NAVIGATOR_COURSES[role_key]: status.setdefault(navigator_course_key(role_key, c), False)
    st.session_state['navigator_status'] = status

def get_navigator_progress() -> Tuple[int, int]:
    role_key = get_role_key(st.session_state['user_role'])
    status = st.session_state.get('navigator_status', {})
    all_courses = [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] + [(role_key, c) for c in NAVIGATOR_COURSES[role_key]]
    return sum(1 for section, course in all_courses if status.get(navigator_course_key(section, course), False)), len(all_courses)

def get_overall_progress() -> Tuple[float, float, float]:
    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_p = df['Status'].sum() / len(df) if not df.empty else 0.0
    nav_done, nav_total = get_navigator_progress()
    navigator_p = (nav_done / nav_total) if nav_total > 0 else 0.0
    return checklist_p, navigator_p, (0.5 * checklist_p) + (0.5 * navigator_p)

# --- 3. STATE INITIALIZATION ---
if 'user_role' not in st.session_state: st.session_state['user_role'] = "SPE (Spare Parts Engineer)"
if 'curriculum' not in st.session_state:
    st.session_state['curriculum'] = [{**t, "Status": False} for t in get_checklist_data(st.session_state['user_role'])]
init_navigator_status()
inject_global_css()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3214/3214011.png", width=60) # Sleek icon
    st.title("AMT Hub")
    
    selected_role = st.selectbox("Current Role", list(ROLE_KEY_MAP.keys()), index=list(ROLE_KEY_MAP.keys()).index(st.session_state['user_role']))
    if selected_role != st.session_state['user_role']:
        st.session_state['user_role'] = selected_role
        reset_user()
        st.rerun()

    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Requests & Learning", "Checklist", "Mentor Guide", "Good to Know"], label_visibility="collapsed")
    st.markdown("---")

    # Modern Popovers instead of Expanders
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
    for name, url in IMPORTANT_LINKS.items():
        st.markdown(f"🔗 [{name}]({url})")

# --- 5. PAGES ---
role_key = get_role_key(st.session_state['user_role'])
role_label = st.session_state['user_role'].split("(")[0].strip()

# PAGE: DASHBOARD
if page == "Dashboard":
    st.markdown(
        f"""
        <div class="hero-card">
            <span class="pill">⚡ AMT Onboarding</span>
            <h1>Welcome to the team, {role_label} 👋</h1>
            <p class="muted">Your personalized command center for mastering the {role_key} role. Track your gear, request access, and complete your training all in one place.</p>
        </div>
        """, unsafe_allow_html=True
    )

    checklist_p, navigator_p, overall_p = get_overall_progress()
    overall_percent = int(overall_p * 100)
    nav_done, nav_total = get_navigator_progress()
    df = pd.DataFrame(st.session_state['curriculum'])

    # KPI Layout
    kpi1, kpi2, kpi3, chart_col = st.columns([1, 1, 1, 1.2])
    
    with kpi1:
        with st.container(border=True):
            st.metric("Total Progress", f"{overall_percent}%", delta="On Track", delta_color="normal")
    with kpi2:
        with st.container(border=True):
            st.metric("Checklist Tasks", f"{int(checklist_p * 100)}%")
    with kpi3:
        with st.container(border=True):
            st.metric("Learning Modules", f"{nav_done} / {nav_total}")
    with chart_col:
        st.altair_chart(create_donut_chart(overall_p), use_container_width=True)

    if overall_percent == 100:
        st.balloons()
        st.success("🎉 Incredible work! You have completed all onboarding requirements.")

    st.markdown("### 🎯 Action Center")
    colA, colB = st.columns(2)
    
    with colA:
        with st.container(border=True):
            st.subheader("Next Checklist Tasks")
            if not df.empty:
                pending = df[df['Status'] == False].sort_values(by="Phase").head(4)
                if not pending.empty:
                    st.dataframe(pending[["Phase", "Task", "Mentor"]], hide_index=True, use_container_width=True)
                else:
                    st.success("All checklist tasks complete! ✅")
            
    with colB:
        with st.container(border=True):
            st.subheader("Upcoming Training")
            nav_focus = [c for c in [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]] + [(role_key, c) for c in NAVIGATOR_COURSES[role_key]] if not st.session_state['navigator_status'].get(navigator_course_key(c[0], c[1]), False)][:4]
            if nav_focus:
                st.dataframe(pd.DataFrame([{"Category": s, "Course": c} for s, c in nav_focus]), hide_index=True, use_container_width=True)
            else:
                st.success("You are entirely caught up on training! ✅")

# PAGE: REQUESTS & LEARNING
elif page == "Requests & Learning":
    st.markdown("## 📚 Requests & Learning")
    st.markdown("Manage your system access and required certifications.")

    tab1, tab2, tab3 = st.tabs(["🔐 FAROS Access", "🎓 Navigator Hub", "🧰 Toolkit"])

    with tab1:
        st.info("💡 Pro Tip: Use the **FAROS Portal** link in the sidebar to log these requests.")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("🏢 Core Systems")
                for item in FAROS_CATALOG["Common"]: st.markdown(f"✅ {item}")
        with col2:
            with st.container(border=True):
                st.subheader(f"🛠 {role_key} Systems")
                for item in FAROS_CATALOG[role_key]: st.markdown(f"🔹 **{item}**")

    with tab2:
        completed_nav, total_nav = get_navigator_progress()
        st.progress(completed_nav / total_nav if total_nav > 0 else 0, text=f"Course Completion: {completed_nav}/{total_nav}")
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🚨 Mandatory Training")
                for course in NAVIGATOR_COURSES["Mandatory"]:
                    key = navigator_course_key("Mandatory", course)
                    st.checkbox(course, value=st.session_state['navigator_status'].get(key, False), key=f"nav_{key}", on_change=nav_click_callback, args=("Mandatory", course))
        with c2:
            with st.container(border=True):
                st.subheader(f"🧠 {role_key} Specific")
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
    df = pd.DataFrame(st.session_state['curriculum'])
    df['idx'] = df.index

    # Advanced Search Filter
    search_query = st.text_input("🔍 Filter tasks by keyword...", "").lower()

    if not df.empty:
        unique_phases = df['Phase'].unique().tolist()
        for phase in unique_phases:
            phase_tasks = df[df['Phase'] == phase]
            
            # Apply search filter
            if search_query:
                phase_tasks = phase_tasks[phase_tasks['Task'].str.lower().str.contains(search_query) | phase_tasks['Category'].str.lower().str.contains(search_query)]
                if phase_tasks.empty: continue # Skip rendering phase if no matches
            
            done = int(phase_tasks['Status'].sum())
            total = len(phase_tasks)
            
            with st.container(border=True):
                st.markdown(f"### 🗓 {phase} ({done}/{total})")
                for _, row in phase_tasks.iterrows():
                    idx = int(row['idx'])
                    st.markdown('<div class="checklist-row">', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([0.05, 0.65, 0.30])
                    with c1:
                        st.checkbox("Done", value=row['Status'], key=f"chk_{idx}", on_change=toggle_status, args=(idx,), label_visibility="collapsed")
                    with c2:
                        task_text = f"~~**{row['Task']}**~~" if row['Status'] else f"**{row['Task']}**"
                        st.markdown(task_text)
                        st.caption(f"Category: {row['Category']}")
                    with c3:
                        st.markdown(f"<div style='text-align:right;'><span class='mentor-badge'>👤 {row['Mentor']}</span></div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# PAGE: MENTOR GUIDE
elif page == "Mentor Guide":
    st.markdown("## 📘 Mentor’s Playbook")
    st.warning("🔒 **Restricted:** This section is intended for Mentors & Managers to ensure a high-quality onboarding experience.")
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("💡 Best Practices")
            st.markdown("- **Comfort First:** Ensure hardware and badges are sorted before deep technical topics.\n- **Shadowing:** Hires should mostly observe during their first 3 field visits.\n- **SOP:** Always use the latest SharePoint SOP.")
    with c2:
        with st.container(border=True):
            st.subheader("👀 Red Flags to Watch For")
            st.markdown("- Signs of overload during Week 1 stand-ups.\n- Lingering system access blockers preventing productivity.\n- Misunderstanding of basic workshop safety.")

# PAGE: GOOD TO KNOW
elif page == "Good to Know":
    st.markdown("## 🧩 System Architecture")
    st.markdown("Understanding how data flows between our internal tools is key to mastering your workflow.")
    
    with st.container(border=True):
        if has_graphviz:
            st.markdown(f"**Data Flow Map: {st.session_state['user_role']}**")
            st.graphviz_chart(get_tech_stack_graph(role_key))
        else:
            st.error("Graphviz required for visualization.")
