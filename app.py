import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="AMT Onboarding Hub", layout="wide")

# --- 1. DATA & CONTENT ---

# EXTRACTED FROM: AMT Faros Request Catalogue
FAROS_CATALOG = {
    "Common": [
        "Microsoft 365 (Outlook, Teams, Excel)",
        "VPN Access (Cisco AnyConnect)",
        "Workday Access",
        "Concur (Travel & Expenses)"
    ],
    "SPE": [
        "SAP GUI (ERP System)",
        "GLOPPS (Global Logistics)",
        "KOLA (Parts Documentation)",
        "RUMBA",
        "Autodesk Vault (CAD Data Management)",
        "Creo MCAD (View Only)"
    ],
    "SE": [
        "SAP GUI (Service Module)",
        "MOM (Mobile Order Management)",
        "LOTO Safety Portal",
        "Electronic Service Report (ESR) Tool",
        "Hydraulic Schematics Viewer"
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

# MAIN DATA FUNCTION: Returns tasks based on role
def get_checklist_data(role):
    # Base list for everyone (Day 1 Basics)
    tasks = [
        # DAY 1 - BASICS
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Safety Shoes & PPE", "Mentor": "Office Admin", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "Logistics", "Task": "Collect Laptop, Mobile & Headset", "Mentor": "IT Support", "Type": "Pickup"},
        {"Phase": "Day 1", "Category": "IT Setup", "Task": "Initial Windows Login & Password Change", "Mentor": "IT Support", "Type": "Action"},
        {"Phase": "Day 1", "Category": "IT Setup", "Task": "Connect to Office Wi-Fi / VPN", "Mentor": "Buddy: Sarah J.", "Type": "Action"},
        {"Phase": "Day 1", "Category": "Orientation", "Task": "Office Tour (Fire Exits, Pantry, First Aid)", "Mentor": "Buddy: Sarah J.", "Type": "Meeting"},
        
        # DAY 2-5 - INDUCTION
        {"Phase": "Week 1", "Category": "HR & Admin", "Task": "Complete 'Code of Conduct' Training", "Mentor": "HR Dept", "Type": "Training"},
        {"Phase": "Week 1", "Category": "HR & Admin", "Task": "Submit Bank Details in Workday", "Mentor": "HR Dept", "Type": "Admin"},
        {"Phase": "Week 1", "Category": "Introduction", "Task": "Meet with Line Manager (Expectations)", "Mentor": "Manager: Mike R.", "Type": "Meeting"},
        {"Phase": "Week 1", "Category": "Introduction", "Task": "Team Introduction Presentation", "Mentor": "Manager: Mike R.", "Type": "Meeting"},
    ]

    # SPECIFIC TASKS FOR SE (Service Engineer)
    if role == "SE (Service Engineer)":
        tasks.extend([
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: SAP Service Module", "Mentor": "Tech Lead: Alex", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: MOM (Mobile Order Mgmt)", "Mentor": "Tech Lead: Alex", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "LOTO (Lock Out Tag Out) Certification", "Mentor": "Safety Officer", "Type": "Training"},
            {"Phase": "Week 1", "Category": "Field Prep", "Task": "Ride-along Preparation", "Mentor": "Senior SE: John D.", "Type": "Meeting"},
        ])

    # SPECIFIC TASKS FOR SPE (Spare Parts Engineer)
    elif role == "SPE (Spare Parts Engineer)":
        tasks.extend([
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: SAP GUI (ERP)", "Mentor": "Logistics Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: GLOPPS & KOLA Access", "Mentor": "Logistics Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "FAROS Access", "Task": "Request: Autodesk Vault & Creo", "Mentor": "Design Lead", "Type": "IT Ticket"},
            {"Phase": "Week 1", "Category": "Training", "Task": "Reman Number Creation Process (SOP)", "Mentor": "Senior SPE: Emily", "Type": "Training"},
            {"Phase": "Week 1", "Category": "Training", "Task": "Warehouse Inventory Cycle Count Intro", "Mentor": "Warehouse Mgr", "Type": "Training"},
        ])
        
    return tasks

# --- STATE MANAGEMENT ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "SPE (Spare Parts Engineer)" # Default

# Load curriculum into session state
if 'curriculum' not in st.session_state:
    raw_data = get_checklist_data(st.session_state['user_role'])
    # Add 'Status' key to track completion
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]

def reset_user():
    """Resets the checklist when the user switches roles"""
    raw_data = get_checklist_data(st.session_state['user_role'])
    st.session_state['curriculum'] = [{**t, "Status": False} for t in raw_data]

def toggle_status(index):
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

# --- SIDEBAR ---
st.sidebar.title("🚀 AMT Onboarding")

# Role Switcher
selected_role = st.sidebar.selectbox(
    "Select Role:",
    ["SPE (Spare Parts Engineer)", "SE (Service Engineer)"],
    index=0
)

# Reset if role changes
if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

# Navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "FAROS Requests", "Checklist", "Mentor Guide"])
st.sidebar.markdown("---")

# Links Section
st.sidebar.subheader("🔗 Quick Links")
for name, url in IMPORTANT_LINKS.items():
    st.sidebar.markdown(f"[{name}]({url})")

# --- PAGE 1: DASHBOARD ---
if page == "Dashboard":
    st.title(f"Welcome, {selected_role.split('(')[0]}! 👋")
    
    # Progress Calculation
    df = pd.DataFrame(st.session_state['curriculum'])
    if not df.empty:
        total = len(df)
        completed = len(df[df['Status'] == True])
        progress = int((completed / total) * 100)
    else:
        progress = 0

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Progress", f"{progress}%")
    with col2:
        # Count FAROS (IT Ticket) tasks specifically
        faros_tasks = df[df['Category'] == 'FAROS Access']
        if not faros_tasks.empty:
            faros_done = len(faros_tasks[faros_tasks['Status'] == True])
            st.metric("Access Requests", f"{faros_done} / {len(faros_tasks)}")
        else:
            st.metric("Access Requests", "N/A")
    with col3:
        remaining = len(df[df['Status'] == False])
        st.metric("Pending Tasks", remaining)

    st.progress(progress / 100)
    
    st.subheader("📅 Today's Focus")
    # Filter for Day 1 tasks if incomplete, otherwise show Week 1
    day1_tasks = df[(df['Phase'] == 'Day 1') & (df['Status'] == False)]
    
    if not day1_tasks.empty:
        st.info("⚠️ You still have 'Day 1' tasks to complete!")
        # Show specific columns
        st.dataframe(day1_tasks[['Category', 'Task', 'Mentor']], hide_index=True, use_container_width=True)
    else:
        st.success("Day 1 tasks complete! Moving on to Week 1 goals.")
        week1_tasks = df[(df['Phase'] == 'Week 1') & (df['Status'] == False)]
        if not week1_tasks.empty:
            st.dataframe(week1_tasks[['Category', 'Task', 'Mentor']], hide_index=True, use_container_width=True)

# --- PAGE 2: FAROS REQUESTS ---
elif page == "FAROS Requests":
    st.title("🔐 FAROS Access Catalogue")
    st.markdown("Use the **FAROS Portal** link in the sidebar to request these specific tools.")
    
    # Determine which list to show based on role
    role_key = "SE" if "Service" in st.session_state['user_role'] else "SPE"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Core Access (Everyone)")
        for item in FAROS_CATALOG["Common"]:
            st.markdown(f"- {item}")
            
    with col2:
        st.subheader(f"🛠 {role_key} Specific Tools")
        for item in FAROS_CATALOG[role_key]:
            st.markdown(f"- **{item}**")

    st.info("ℹ️ **Tip:** When requesting SAP access in FAROS, make sure to select the correct 'Profile' for your region.")

# --- PAGE 3: CHECKLIST ---
elif page == "Checklist":
    st.title("✅ Onboarding Checklist")
    
    df = pd.DataFrame(st.session_state['curriculum'])
    
    # Group by Phase (Day 1 vs Week 1)
    phases = ["Day 1", "Week 1"]
    
    for phase in phases:
        with st.expander(f"🗓 {phase} Tasks", expanded=True):
            phase_tasks = df[df['Phase'] == phase]
            
            # Create headers for the list to simulate a table with controls
            h1, h2, h3 = st.columns([0.05, 0.6, 0.35])
            h2.caption("TASK")
            h3.caption("MENTOR / POC") # Point of Contact
            
            for index, row in phase_tasks.iterrows():
                # Find original index to sync state because filtering changes indices
                original_index = -1
                for i, item in enumerate(st.session_state['curriculum']):
                    if item['Task'] == row['Task']:
                        original_index = i
                        break
                
                c1, c2, c3 = st.columns([0.05, 0.6, 0.35])
                
                # Column 1: Checkbox
                with c1:
                    st.checkbox(
                        "Done", 
                        value=row['Status'], 
                        key=f"chk_{original_index}",
                        on_change=toggle_status,
                        args=(original_index,),
                        label_visibility="collapsed"
                    )
                
                # Column 2: Task Name
                with c2:
                    if row['Status']:
                        st.markdown(f"~~{row['Task']}~~") # Strikethrough if done
                    else:
                        st.write(f"**{row['Task']}**")

                # Column 3: Mentor Name (The new feature)
                with c3:
                    st.info(f"👤 {row['Mentor']}", icon="ℹ️")

# --- PAGE 4: MENTOR GUIDE ---
elif page == "Mentor Guide":
    st.title("📘 Mentor's Handbook")
    st.warning("🔒 This section is intended for Mentors & Managers to review.")

    st.subheader("💡 Best Practices for Onboarding")
    st.markdown("""
    * **Day 1 is about comfort:** Ensure the new hire has their hardware and coffee access before diving into technical topics.
    * **Shadowing:** For the first 3 field visits, the new hire should only observe. Do not assign them active tasks yet.
    * **SOP Review:** When teaching *Reman Process*, please use the updated PDF (v2.4) located in SharePoint.
    """)

    st.markdown("---")

    st.subheader("📝 Feedback Criteria")
    st.write("When evaluating the new hire during Week 1, please look for:")
    
    # Using columns for better layout
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Technical Skills**")
        st.checkbox("Understands basic SAP navigation")
        st.checkbox("Can identify key safety hazards (LOTO)")
        st.checkbox("Knows how to look up part numbers in KOLA")
        
    with col2:
        st.info("**Soft Skills**")
        st.checkbox("Asks questions when unsure")
        st.checkbox("Punctual for morning meetings")
        st.checkbox("Shows initiative in reviewing documentation")
        
    st.markdown("---")
    st.caption("Need to report an issue? Contact the Onboarding Lead at hr-onboarding@example.com")

