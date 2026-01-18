import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Team Onboarding Hub", layout="wide")

# --- 1. DEFINE ROLES & CURRICULUMS ---

# Common Tasks (Now Empty/Generic - HR tasks removed)
COMMON_TASKS = []

# --- CUSTOMIZED SPARE PARTS CURRICULUM ---
SPARE_PARTS_TASKS = [
    # 1. Equipment Collection & Intro
    {"Category": "Equipment & Gear", "Task": "Collect Laptop & Peripherals (Mouse/Keyboard)", "Type": "Pickup"},
    {"Category": "Equipment & Gear", "Task": "Collect Mobile Phone & Headset", "Type": "Pickup"},
    {"Category": "Equipment & Gear", "Task": "Safety Shoes Fitting & Collection", "Type": "Pickup"},
    {"Category": "Orientation", "Task": "Office Tour (Fire Exits, Pantry, Printers)", "Type": "Meeting"},
    {"Category": "Orientation", "Task": "Team Introduction Meeting", "Type": "Meeting"},
    
    # 2. Software Access (IT Requests)
    {"Category": "Software Access", "Task": "Request Access: GLOPPS", "Type": "IT Ticket"},
    {"Category": "Software Access", "Task": "Request Access: KOLA", "Type": "IT Ticket"},
    {"Category": "Software Access", "Task": "Request Access: RUMBA", "Type": "IT Ticket"},
    {"Category": "Software Access", "Task": "Get 'WD Numbers' Excel File Access", "Type": "File Access"},
    {"Category": "Software Access", "Task": "Install & License: Creo MCAD", "Type": "IT Ticket"},

    # 3. Training (Online Courses)
    {"Category": "Training Modules", "Task": "GLOPPS Basics (Online Course)", "Type": "Training"},
    {"Category": "Training Modules", "Task": "KOLA Navigation & Search (Online Course)", "Type": "Training"},
    {"Category": "Training Modules", "Task": "RUMBA Workflow Training (Online Course)", "Type": "Training"},
    {"Category": "Training Modules", "Task": "Creo MCAD Fundamentals (Online Course)", "Type": "Training"},
    
    # 4. Specific Processes
    {"Category": "Process Knowledge", "Task": "Learn: Reman Number Creation", "Type": "SOP Study"},
]

# Service Engineer Tasks
SERVICE_ENG_TASKS = [
    {"Category": "Safety", "Task": "LOTO (Lock Out Tag Out) Certification", "Type": "Module"},
    {"Category": "Field Skills", "Task": "Field Service Report Writing", "Type": "Module"},
    {"Category": "Technical", "Task": "Reading Hydraulic Schematics", "Type": "Module"},
]

# --- SHAREPOINT LINKS (HR Link Removed) ---
IMPORTANT_LINKS = {
    "SharePoint Home": "https://yourcompany.sharepoint.com/sites/home",
    "Engineering Specs": "https://yourcompany.sharepoint.com/sites/engineering",
    "IT Support Ticket": "https://yourcompany.service-now.com"
}

# --- STATE MANAGEMENT ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "Spare Parts Engineer" 

def get_curriculum(role):
    tasks = []
    # Add Common Tasks (If any)
    for t in COMMON_TASKS:
        tasks.append({**t, "Status": False, "Role": "All"})
    
    # Add Role Specific Tasks
    if role == "Service Engineer":
        for t in SERVICE_ENG_TASKS:
            tasks.append({**t, "Status": False, "Role": "Service"})
    elif role == "Spare Parts Engineer":
        for t in SPARE_PARTS_TASKS:
            tasks.append({**t, "Status": False, "Role": "Parts"})
            
    return tasks

# Initialize curriculum
if 'curriculum' not in st.session_state:
    st.session_state['curriculum'] = get_curriculum(st.session_state['user_role'])

def toggle_status(index):
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

def reset_user():
    st.session_state['curriculum'] = get_curriculum(st.session_state['user_role'])

# --- SIDEBAR ---
st.sidebar.title("🚀 Onboarding Hub")

# Role Switcher
selected_role = st.sidebar.selectbox(
    "Select User Role:",
    ["Spare Parts Engineer", "Service Engineer"],
    index=0
)

if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

# Navigation
page = st.sidebar.radio("Navigate", ["My Dashboard", "Learning Modules", "Admin View"])
st.sidebar.markdown("---")

# --- LINKS SECTION ---
st.sidebar.subheader("🔗 Quick Links")
for name, url in IMPORTANT_LINKS.items():
    st.sidebar.markdown(f"[{name}]({url})")

# --- PAGE 1: DASHBOARD ---
if page == "My Dashboard":
    st.title(f"Welcome, {selected_role}! 👋")
    
    # Progress Calculation
    df = pd.DataFrame(st.session_state['curriculum'])
    if df.empty: 
        progress = 0
        total = 0
        completed = 0
    else:
        total = len(df)
        completed = len(df[df['Status'] == True])
        progress = int((completed / total) * 100)

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Progress", f"{progress}%")
    with col2:
        if selected_role == "Spare Parts Engineer":
            # Count specific software access tasks completed
            access_tasks = df[df['Category'] == 'Software Access']
            if not access_tasks.empty:
                access_done = len(access_tasks[access_tasks['Status'] == True])
                st.metric("Software Access", f"{access_done} / {len(access_tasks)}")
            else:
                 st.metric("Software Access", "0 / 0")
        else:
            st.metric("Field Visits", "0 / 5")
    with col3:
        remaining = len(df[df['Status'] == False])
        st.metric("To-Do Items", remaining)

    st.progress(progress / 100)
    
    # Priority Alert for Parts Engineers
    if selected_role == "Spare Parts Engineer":
        st.info("ℹ️ **Note:** 'WD Numbers' excel is located in the Engineering SharePoint. Check the sidebar for the link.")

    st.subheader("📌 Action Items")
    pending_tasks = df[df['Status'] == False]
    
    if not pending_tasks.empty:
        st.dataframe(
            pending_tasks[['Category', 'Task', 'Type']], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("You are all set! Great job.")

# --- PAGE 2: LEARNING MODULES ---
elif page == "Learning Modules":
    st.title("📚 Tasks & Training")
    
    df = pd.DataFrame(st.session_state['curriculum'])
    if not df.empty:
        categories = df['Category'].unique()
        
        # Custom order for Parts Engineers
        if selected_role == "Spare Parts Engineer":
            preferred_order = ["Equipment & Gear", "Orientation", "Software Access", "Training Modules", "Process Knowledge"]
            categories = [c for c in preferred_order if c in categories] + [c for c in categories if c not in preferred_order]

        for cat in categories:
            with st.expander(f"🔹 {cat}", expanded=True):
                cat_tasks = df[df['Category'] == cat]
                
                for index, row in cat_tasks.iterrows():
                    # Find original index
                    original_index = -1
                    for i, item in enumerate(st.session_state['curriculum']):
                        if item['Task'] == row['Task']:
                            original_index = i
                            break
                    
                    col_a, col_b = st.columns([0.05, 0.95])
                    with col_a:
                        st.checkbox(
                            "Done", 
                            value=row['Status'], 
                            key=f"task_{original_index}",
                            on_change=toggle_status,
                            args=(original_index,),
                            label_visibility="collapsed"
                        )
                    with col_b:
                        # Formatting based on type
                        if row['Type'] == "IT Ticket":
                            st.write(f"**{row['Task']}** 🎫 *(Requires IT Ticket)*")
                        elif row['Type'] == "Training":
                            st.write(f"**{row['Task']}** 🎓 *(Online Course)*")
                        else:
                            st.write(f"**{row['Task']}**")
    else:
        st.info("No tasks assigned yet.")

# --- PAGE 3: ADMIN VIEW ---
elif page == "Admin View":
    st.title("Manager Overview 🔒")
    st.write("Monitor team progress here.")
    
    # Mock Data
    data = {
        "Engineer": ["Alice (Parts)", "Bob (Parts)", "Charlie (Service)"],
        "GLOPPS Access": ["Granted", "Pending", "N/A"],
        "KOLA Training": ["Completed", "In Progress", "N/A"],
        "Onboarding %": [90, 45, 20]
    }
    st.table(data)

