import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="AMT Onboarding Hub", layout="wide", page_icon="🚀")

# --- 0. LIBRARY CHECK (CRASH GUARD) ---
try:
    import graphviz
    has_graphviz = True
except ModuleNotFoundError:
    has_graphviz = False

# --- 1. DATA & CONTENT ---

# TECH STACK VISUALIZATION DATA
def get_tech_stack_graph(role):
    if not has_graphviz:
        return None
        
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR') 
    graph.attr('node', shape='box', style='filled', fontname='Helvetica')
    
    if "Service" in role:
        # Service Engineer Workflow
        graph.node('C', 'Customer Site', fillcolor='#e1f5fe')
        graph.node('SF', 'Salesforce (CRM)', shape='ellipse', fillcolor='#fff9c4')
        graph.node('SAP', 'SAP Service Module', shape='ellipse', fillcolor='#fff9c4')
        graph.node('MOM', 'MOM App (Mobile)', fillcolor='#c8e6c9')
        graph.node('KOLA', 'KOLA (Parts DB)', shape='cylinder', fillcolor='#f0f4c3')
        
        # Connections
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
        
        # Connections
        graph.edge('V', 'SAP', label='Invoices')
        graph.edge('SAP', 'GLOPPS', label='Inventory Check')
        graph.edge('PLM', 'SAP', label='Part Number Gen')
        graph.edge('CAD', 'PLM', label='Drawings Upload')
        
    return graph

# EXTRACTED FROM: AMT Faros Request Catalogue
FAROS_CATALOG = {
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

# NEW: NAVIGATOR TRAINING COURSES
NAVIGATOR_COURSES = {
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

IMPORTANT_LINKS = {
    "FAROS (Access Portal)": "https://faros.internal.example.com", 
    "Navigator (Learning)": "https://navigator.internal.example.com",
    "Workday (HR)": "https://www.myworkday.com",
    "Concur (Expenses)": "https://www.concursolutions.com"
}

# ACRONYMS
ACRONYMS = {
    "AI": "Aakash Intelligence",
    "TOBIAS": "Totally Outclassed By Intelligent Aakash Significantly",
    "AAKASH": "An Absolute Knight Amongst Silly Humans",
    "MOM": "Mobile Order Management",
    "SAP": "Systems, Applications, and Products",
    "SPE": "Spare Parts Engineer",
    "SE": "Service Engineer",
    "FAROS": "Federated Access Request System",
    "VPN": "Virtual Private Network"
}

# CONTACTS
KEY_CONTACTS = {
    "IT Helpdesk": "Ext. 4040",
    "HR Onboarding": "Ext. 2000",
    "Safety Officer": "Ext. 9110"
}

def get_checklist_data(role):
    tasks = [
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Safety Shoes & PPE", "Mentor": "Office Admin", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Laptop, Mobile & Headset", "Mentor": "IT Support", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "IT Setup", "Task": "Initial Windows Login", "Mentor": "IT Support", "Type": "Action"},
        {"Phase": "Day 1", "Category": "Orientation", "Task": "Office Tour (Fire Exits)", "Mentor": "Buddy: Sarah J.", "Type": "Meeting"},
        
        {"Phase": "Week 1", "Category": "HR", "Task": "Submit Bank Details", "Mentor": "HR Dept", "Type": "Admin"},
        {"Phase": "Week 1", "Category": "Intro", "Task": "Team Intro Presentation", "Mentor": "Manager: Mike R.", "Type": "Meeting"},
    ]

    if role == "SE (Service Engineer)":
        tasks.extend([
            {"Phase": "Week 1", "Category": "Access", "Task": "Request: SAP Service Module", "Mentor": "Tech Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "LOTO Certification", "Mentor": "Safety Officer", "Type": "Training"},
        ])
    elif role == "SPE (Spare Parts Engineer)":
        tasks.extend([
            {"Phase": "Week 1", "Category": "Access", "Task": "Request: GLOPPS Access", "Mentor": "Logistics Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "Reman Process SOP", "Mentor": "Senior SPE", "Type": "Training"},
        ])
    return tasks

# --- STATE ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "SPE (Spare Parts Engineer)"

if 'curriculum' not in st.session_state:
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]

def reset_user():
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]

def toggle_status(index):
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

# --- SIDEBAR ---
st.sidebar.title("🚀 AMT Onboarding")
selected_role = st.sidebar.selectbox("Select Role:", ["SPE (Spare Parts Engineer)", "SE (Service Engineer)"])

if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

# Updated Navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "Requests & Learning", "Checklist", "Mentor Guide", "Good to Know"])

# CONTACT WIDGET
st.sidebar.markdown("---")
with st.sidebar.expander("🆘 Who do I call?"):
    for dept, contact in KEY_CONTACTS.items():
        st.markdown(f"**{dept}:**\n`{contact}`")

# ACRONYM WIDGET
st.sidebar.markdown("---")
with st.sidebar.expander("🧠 Acronym Buster"):
    search_term = st.text_input("Look up a term:", placeholder="e.g. MOM")
    if search_term:
        found = False
        for key, value in ACRONYMS.items():
            if search_term.upper() in key:
                st.info(f"**{key}**: {value}")
                found = True
        if not found:
            st.error("Unknown term.")

st.sidebar.markdown("---")
st.sidebar.subheader("🔗 Quick Links")
for name, url in IMPORTANT_LINKS.items():
    st.sidebar.markdown(f"[{name}]({url})")

# --- PAGE 1: DASHBOARD ---
if page == "Dashboard":
    st.title(f"Welcome, {selected_role.split('(')[0]}! 👋")
    
    df = pd.DataFrame(st.session_state['curriculum'])
    if not df.empty:
        total = len(df)
        completed = len(df[df['Status'] == True])
        progress = int((completed / total) * 100)
    else:
        progress = 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Progress", f"{progress}%")
    with col2:
        faros_tasks = df[df['Category'] == 'Access']
        if not faros_tasks.empty:
            faros_done = len(faros_tasks[faros_tasks['Status'] == True])
            st.metric("Access Requests", f"{faros_done} / {len(faros_tasks)}")
    with col3:
        remaining = len(df[df['Status'] == False])
        st.metric("Pending Tasks", remaining)

    st.progress(progress / 100)
    
    # Celebration
    if progress == 100:
        st.balloons()
        st.success("🎉 You have completed all onboarding tasks!")
    
    st.subheader("📅 Today's Focus")
    day1_tasks = df[(df['Phase'] == 'Day 1') & (df['Status'] == False)]
    
    if not day1_tasks.empty:
        st.info("⚠️ You still have 'Day 1' tasks to complete!")
        st.dataframe(day1_tasks[['Category', 'Task', 'Mentor']], hide_index=True, use_container_width=True)
    else:
        if progress < 100:
            st.success("Day 1 tasks complete! Moving on to Week 1 goals.")
            week1_tasks = df[(df['Phase'] == 'Week 1') & (df['Status'] == False)]
            if not week1_tasks.empty:
                st.dataframe(week1_tasks[['Category', 'Task', 'Mentor']], hide_index=True, use_container_width=True)

# --- PAGE 2: REQUESTS & LEARNING (Combined) ---
elif page == "Requests & Learning":
    st.title("📚 Requests & Learning")
    st.markdown("Here you can find your IT Access Requests and your Mandatory Training.")
    
    role_key = "SE" if "Service" in st.session_state['user_role'] else "SPE"
    
    # Create two tabs
    tab1, tab2 = st.tabs(["🔐 FAROS Access Requests", "🎓 Navigator Courses"])
    
    # --- TAB 1: FAROS ACCESS ---
    with tab1:
        st.info("Use the **FAROS Portal** link in the sidebar to request these tools.")
        
        st.subheader("🏢 Standard Access (Required for All)")
        with st.expander("View Core Systems List", expanded=True):
            c1, c2 = st.columns(2)
            items = FAROS_CATALOG["Common"]
            half = (len(items) + 1) // 2
            with c1:
                for item in items[:half]:
                    st.markdown(f"✅ {item}")
            with c2:
                for item in items[half:]:
                    st.markdown(f"✅ {item}")

        st.subheader(f"🛠 {role_key} Specialized Tools")
        with st.expander(f"View {role_key} Toolset", expanded=True):
            c1, c2 = st.columns(2)
            items = FAROS_CATALOG[role_key]
            half = (len(items) + 1) // 2
            with c1:
                for item in items[:half]:
                    st.markdown(f"🔹 **{item}**")
            with c2:
                for item in items[half:]:
                    st.markdown(f"🔹 **{item}**")

    # --- TAB 2: NAVIGATOR COURSES ---
    with tab2:
        st.info("Log in to **Navigator** (link in sidebar) to complete these modules.")
        
        st.subheader("🚨 Mandatory Compliance (Due Week 1)")
        for item in NAVIGATOR_COURSES["Mandatory"]:
            st.warning(f"⚠️ {item}")
            
        st.markdown("---")
        
        st.subheader(f"🧠 {role_key} Role-Specific Training")
        for item in NAVIGATOR_COURSES[role_key]:
            st.success(f"🎓 {item}")

# --- PAGE 3: CHECKLIST ---
elif page == "Checklist":
    st.title("✅ Onboarding Checklist")
    df = pd.DataFrame(st.session_state['curriculum'])
    phases = ["Day 1", "Week 1"]
    
    for phase in phases:
        with st.expander(f"🗓 {phase} Tasks", expanded=True):
            phase_tasks = df[df['Phase'] == phase]
            h1, h2, h3 = st.columns([0.05, 0.6, 0.35])
            h2.caption("TASK")
            h3.caption("MENTOR / POC")
            
            for index, row in phase_tasks.iterrows():
                original_index = -1
                for i, item in enumerate(st.session_state['curriculum']):
                    if item['Task'] == row['Task']:
                        original_index = i
                        break
                
                c1, c2, c3 = st.columns([0.05, 0.6, 0.35])
                with c1:
                    st.checkbox("Done", value=row['Status'], key=f"chk_{original_index}", on_change=toggle_status, args=(original_index,), label_visibility="collapsed")
                with c2:
                    if row['Status']:
                        st.markdown(f"~~{row['Task']}~~")
                    else:
                        st.write(f"**{row['Task']}**")
                with c3:
                    st.info(f"👤 {row['Mentor']}", icon="ℹ️")

# --- PAGE 4: MENTOR GUIDE ---
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

# --- PAGE 5: GOOD TO KNOW ---
elif page == "Good to Know":
    st.title("🧩 Good to Know")
    st.markdown("Context and Reference material for your role.")
    
    st.subheader("System Architecture")
    st.markdown("Understanding how our tools connect helps you understand the workflow.")
    
    if has_graphviz:
        role = st.session_state['user_role']
        st.write(f"**Workflow for: {role}**")
        
        # Render the graphviz chart
        graph = get_tech_stack_graph(role)
        st.graphviz_chart(graph)
        st.info("💡 **Tip:** Click the 'View Fullscreen' arrow on the chart to see details clearly.")
    else:
        st.warning("⚠️ Graphviz is not installed. The system map cannot be displayed.")
        st.code("pip install graphviz", language="bash")








