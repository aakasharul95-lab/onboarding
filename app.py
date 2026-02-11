import streamlit as st
import pandas as pd
import random
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="AMT Onboarding Hub", layout="wide", page_icon="🚀")

# --- 1. DATA & CONTENT ---

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
        "SharePoint: Global Engineering",
        "Box (Cloud Storage)",
        "Udemy Business (Learning Portal)",
        "Internal Wiki (Confluence)"
    ],
    "SPE": [
        "SAP GUI: ERP System (Production)",
        "GLOPPS (Global Logistics & Parts)",
        "KOLA (Parts Documentation DB)",
        "RUMBA (Legacy Parts Lookup)",
        "Autodesk Vault (CAD Data Management)",
        "Creo MCAD (View & Edit License)",
        "Agile PLM (Product Lifecycle Mgmt)",
        "PowerBI Desktop (Inventory Analytics)",
        "JIRA (Engineering Ticket Tracking)",
        "Tableau (Supply Chain Dashboards)",
        "Teamcenter (PLM Viewer)",
        "Matlab (Simulation License)"
    ],
    "SE": [
        "SAP Service Cloud (C4C)",
        "MOM (Mobile Order Management App)",
        "LOTO Safety Portal (Lock Out Tag Out)",
        "ESR Tool (Electronic Service Report)",
        "Hydraulic Schematics Viewer (HSV)",
        "Salesforce CRM (Customer History)",
        "ServiceMax (Field Dispatch)",
        "Fleet Management System (Vehicle Logs)",
        "PLC Diagnostic Tool (Remote Connect)",
        "Electrical Diagrams Database (EDD)",
        "Field Safety App (Mobile)",
        "VPN Token (Hardware)"
    ]
}

# EXTRACTED FROM: AMT Program Links
IMPORTANT_LINKS = {
    "FAROS (Access Portal)": "https://faros.internal.example.com", 
    "Workday (HR)": "https://www.myworkday.com",
    "Concur (Expenses)": "https://www.concursolutions.com",
    "C-Time (Timesheets)": "https://ctime.internal.example.com",
    "E-Learning Portal": "https://learning.internal.example.com"
}

# KEY CONTACTS (New Feature)
KEY_CONTACTS = {
    "IT Helpdesk": "Ext. 4040 (help@amt.com)",
    "HR Onboarding": "Ext. 2000 (hr@amt.com)",
    "Safety Officer": "Ext. 9110 (safety@amt.com)",
    "Facilities": "Ext. 1234 (fixit@amt.com)"
}

# ACRONYM DICTIONARY
ACRONYMS = {
    "GLOPPS": "Global Logistics & Parts Planning System",
    "KOLA": "Key On-Line Access (Parts Documentation DB)",
    "LOTO": "Lock Out Tag Out (Safety Procedure)",
    "MOM": "Mobile Order Management",
    "SAP": "Systems, Applications, and Products (ERP Software)",
    "SPE": "Spare Parts Engineer",
    "SE": "Service Engineer",
    "FAROS": "Federated Access Request & Onboarding System",
    "ESR": "Electronic Service Report",
    "HSV": "Hydraulic Schematics Viewer",
    "PLM": "Product Lifecycle Management",
    "PPE": "Personal Protective Equipment",
    "SOP": "Standard Operating Procedure",
    "VPN": "Virtual Private Network"
}

# MAIN DATA FUNCTION
def get_checklist_data(role):
    tasks = [
        # DAY 1 - BASICS
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Safety Shoes & PPE", "Mentor": "Office Admin", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Laptop, Mobile & Headset", "Mentor": "IT Support", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "IT Setup", "Task": "Initial Windows Login & Password Change", "Mentor": "IT Support", "Type": "Action"},
        {"Phase": "Day 1", "Category": "IT Setup", "Task": "Connect to Office Wi-Fi / VPN", "Mentor": "Buddy: Sarah J.", "Type": "Action"},
        {"Phase": "Day 1", "Category": "Orientation", "Task": "Office Tour (Fire Exits, Pantry, First Aid)", "Mentor": "Buddy: Sarah J.", "Type": "Meeting"},
        
        # WEEK 1 - GENERAL
        {"Phase": "Week 1", "Category": "HR & Admin", "Task": "Complete 'Code of Conduct' Training", "Mentor": "HR Dept", "Type": "Training"},
        {"Phase": "Week 1", "Category": "HR & Admin", "Task": "Submit Bank Details in Workday", "Mentor": "HR Dept", "Type": "Admin"},
        {"Phase": "Week 1", "Category": "Introduction", "Task": "Meet with Line Manager (Expectations)", "Mentor": "Manager: Mike R.", "Type": "Meeting"},
        {"Phase": "Week 1", "Category": "Introduction", "Task": "Team Introduction Presentation", "Mentor": "Manager: Mike R.", "Type": "Meeting"},
    ]

    if role == "SE (Service Engineer)":
        tasks.extend([
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: SAP Service Module", "Mentor": "Tech Lead: Alex", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: MOM (Mobile Order Mgmt)", "Mentor": "Tech Lead: Alex", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "LOTO (Lock Out Tag Out) Certification", "Mentor": "Safety Officer", "Type": "Training"},
            {"Phase": "Week 1", "Category": "Field Prep", "Task": "Ride-along Preparation", "Mentor": "Senior SE: John D.", "Type": "Meeting"},
        ])

    elif role == "SPE (Spare Parts Engineer)":
        tasks.extend([
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: SAP GUI (ERP)", "Mentor": "Logistics Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: GLOPPS & KOLA Access", "Mentor": "Logistics Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: Autodesk Vault & Creo", "Mentor": "Design Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "Reman Number Creation Process (SOP)", "Mentor": "Senior SPE: Emily", "Type": "Training"},
            {"Phase": "Week 1", "Category": "Training", "Task": "Warehouse Inventory Cycle Count Intro", "Mentor": "Warehouse Mgr", "Type": "Training"},
        ])
        
    return tasks

# --- HELPER FUNCTIONS ---
def generate_report(user_role, data):
    """Generates a text report for download"""
    buffer = io.StringIO()
    buffer.write(f"ONBOARDING REPORT: {user_role}\n")
    buffer.write("="*40 + "\n\n")
    
    completed = [t for t in data if t['Status']]
    pending = [t for t in data if not t['Status']]
    
    buffer.write(f"SUMMARY: {len(completed)} Completed | {len(pending)} Pending\n\n")
    
    buffer.write("[ COMPLETED TASKS ]\n")
    for t in completed:
        buffer.write(f"[x] {t['Task']} (Mentor: {t['Mentor']})\n")
        
    buffer.write("\n[ PENDING TASKS ]\n")
    for t in pending:
        buffer.write(f"[ ] {t['Task']} (Mentor: {t['Mentor']})\n")
        
    return buffer.getvalue()

# --- STATE MANAGEMENT ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "SPE (Spare Parts Engineer)"

if 'curriculum' not in st.session_state:
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]

# State for Flashcards
if 'flashcard_term' not in st.session_state:
    st.session_state['flashcard_term'] = random.choice(list(ACRONYMS.keys()))
if 'flashcard_reveal' not in st.session_state:
    st.session_state['flashcard_reveal'] = False

def reset_user():
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]

def toggle_status(index):
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

def new_flashcard():
    st.session_state['flashcard_term'] = random.choice(list(ACRONYMS.keys()))
    st.session_state['flashcard_reveal'] = False

def reveal_flashcard():
    st.session_state['flashcard_reveal'] = True

# --- SIDEBAR ---
st.sidebar.title("🚀 AMT Onboarding")

# Role Switcher
selected_role = st.sidebar.selectbox(
    "Select Role:",
    ["SPE (Spare Parts Engineer)", "SE (Service Engineer)"],
    index=0
)

if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

# Navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "FAROS Requests", "Checklist", "Training Dojo", "Mentor Guide"])

# CONTACT WIDGET (New Feature)
st.sidebar.markdown("---")
with st.sidebar.expander("🆘 Who do I call?"):
    for dept, contact in KEY_CONTACTS.items():
        st.markdown(f"**{dept}:**\n`{contact}`")

# Links Section
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

    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Progress", f"{progress}%")
    with col2:
        faros_tasks = df[df['Category'] == 'FAROS Access']
        if not faros_tasks.empty:
            faros_done = len(faros_tasks[faros_tasks['Status'] == True])
            st.metric("Access Requests", f"{faros_done} / {len(faros_tasks)}")
    with col3:
        remaining = len(df[df['Status'] == False])
        st.metric("Pending Tasks", remaining)

    st.progress(progress / 100)
    
    # Export Report Button (New Feature)
    st.download_button(
        label="📄 Download Progress Report",
        data=generate_report(selected_role, st.session_state['curriculum']),
        file_name="onboarding_report.txt",
        mime="text/plain"
    )

    st.markdown("---")
    
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

# --- PAGE 2: FAROS REQUESTS ---
elif page == "FAROS Requests":
    st.title("🔐 FAROS Access Catalogue")
    role_key = "SE" if "Service" in st.session_state['user_role'] else "SPE"
    
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
    st.info(f"These tools are specific to your role as **{st.session_state['user_role']}**.")
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

# --- PAGE 4: TRAINING DOJO (New Feature) ---
elif page == "Training Dojo":
    st.title("🥋 The Training Dojo")
    st.markdown("Master the company jargon before your first meeting.")
    
    st.subheader("⚡ Acronym Flashcards")
    
    # Card Container
    with st.container(border=True):
        st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>{st.session_state['flashcard_term']}</h1>", unsafe_allow_html=True)
        
        if st.session_state['flashcard_reveal']:
            definition = ACRONYMS[st.session_state['flashcard_term']]
            st.markdown(f"<h3 style='text-align: center; color: gray;'>{definition}</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: center; color: gray;'>???</h3>", unsafe_allow_html=True)
            
    # Controls
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.session_state['flashcard_reveal']:
            st.button("Next Card ➡️", on_click=new_flashcard, use_container_width=True)
        else:
            st.button("👀 Reveal Definition", on_click=reveal_flashcard, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📚 Full Dictionary")
    with st.expander("Browse all terms"):
        st.json(ACRONYMS)

# --- PAGE 5: MENTOR GUIDE ---
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





