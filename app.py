import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Team Onboarding Hub", layout="wide")

# --- 1. DEFINE ROLES & CURRICULUMS ---
# separate lists for each role
COMMON_TASKS = [
    {"Category": "Admin", "Task": "Collect Safety Gear (PPE)", "Type": "Checklist"},
    {"Category": "Admin", "Task": "Setup Company Email & Slack", "Type": "Checklist"},
    {"Category": "HR", "Task": "Submit Bank Details", "Type": "Checklist"},
]

SPARE_PARTS_TASKS = [
    {"Category": "Parts Knowledge", "Task": "Intro to ERP System (SAP/Oracle)", "Type": "Module"},
    {"Category": "Parts Knowledge", "Task": "Understanding BOM (Bill of Materials)", "Type": "Module"},
    {"Category": "Warehouse", "Task": "Inventory Cycle Counting", "Type": "Module"},
    {"Category": "Logistics", "Task": "Handling Returns (RMA Process)", "Type": "Module"},
]

SERVICE_ENG_TASKS = [
    {"Category": "Safety", "Task": "LOTO (Lock Out Tag Out) Certification", "Type": "Module"},
    {"Category": "Field Skills", "Task": "Field Service Report Writing", "Type": "Module"},
    {"Category": "Technical", "Task": "Reading Hydraulic Schematics", "Type": "Module"},
    {"Category": "Customer Service", "Task": "Handling Difficult Customers", "Type": "Module"},
]

# --- STATE MANAGEMENT ---
# Initialize session state for the user if it doesn't exist
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "Service Engineer" # Default

# Helper to generate the curriculum based on role
def get_curriculum(role):
    tasks = []
    # Everyone gets common tasks
    for t in COMMON_TASKS:
        tasks.append({**t, "Status": False, "Role": "All"})
    
    # Add specific tasks
    if role == "Service Engineer":
        for t in SERVICE_ENG_TASKS:
            tasks.append({**t, "Status": False, "Role": "Service"})
    elif role == "Spare Parts Engineer":
        for t in SPARE_PARTS_TASKS:
            tasks.append({**t, "Status": False, "Role": "Parts"})
            
    return tasks

# Initialize curriculum if new user or reset
if 'curriculum' not in st.session_state:
    st.session_state['curriculum'] = get_curriculum(st.session_state['user_role'])

# --- HELPER FUNCTIONS ---
def get_progress():
    df = pd.DataFrame(st.session_state['curriculum'])
    if df.empty: return 0
    total = len(df)
    completed = len(df[df['Status'] == True])
    return int((completed / total) * 100)

def toggle_status(index):
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

def reset_user():
    st.session_state['curriculum'] = get_curriculum(st.session_state['user_role'])

# --- SIDEBAR: ROLE SWITCHER (LOGIN SIMULATION) ---
st.sidebar.title("🔧 Onboarding Hub")

# This selectbox acts as your "Login" for now
selected_role = st.sidebar.selectbox(
    "Select User Role:",
    ["Service Engineer", "Spare Parts Engineer"],
    index=0 if st.session_state['user_role'] == "Service Engineer" else 1
)

# If role changes, reset the dashboard
if selected_role != st.session_state['user_role']:
    st.session_state['user_role'] = selected_role
    reset_user()
    st.rerun()

page = st.sidebar.radio("Navigate", ["My Dashboard", "Learning Modules", "Admin View"])
st.sidebar.markdown("---")
st.sidebar.info(f"Viewing as: **{selected_role}**")

# --- PAGE 1: DASHBOARD ---
if page == "My Dashboard":
    st.title(f"Welcome, {selected_role}! 👋")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    progress = get_progress()
    
    with col1:
        st.metric("Onboarding Progress", f"{progress}%")
    with col2:
        # Custom message based on role
        if selected_role == "Service Engineer":
            st.metric("Field Visits", "0 / 5")
        else:
            st.metric("Parts ID'd", "0 / 50")
    with col3:
        remaining = len([x for x in st.session_state['curriculum'] if not x['Status']])
        st.metric("Tasks Remaining", remaining)

    st.progress(progress / 100)
    
    # Conditional Content based on Role
    if selected_role == "Service Engineer":
        st.info("💡 **Tip:** Don't forget to schedule your ride-along with a senior engineer this week.")
    else:
        st.info("💡 **Tip:** The ERP system will be down for maintenance on Friday night.")

    st.subheader("Your To-Do List")
    df = pd.DataFrame(st.session_state['curriculum'])
    
    # Show active tasks
    pending_tasks = df[df['Status'] == False]
    if not pending_tasks.empty:
        st.dataframe(
            pending_tasks[['Category', 'Task', 'Type']], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("All caught up!")

# --- PAGE 2: LEARNING MODULES ---
elif page == "Learning Modules":
    st.title("📚 Your Curriculum")
    
    # Group tasks by Category for cleaner view
    df = pd.DataFrame(st.session_state['curriculum'])
    categories = df['Category'].unique()
    
    for cat in categories:
        with st.expander(f"📂 {cat}", expanded=True):
            # Get tasks in this category
            cat_tasks = df[df['Category'] == cat]
            
            for index, row in cat_tasks.iterrows():
                # We need the original index from the session state list to toggle correctly
                # We find the index by matching the Task name (simple method for this demo)
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
                    st.write(f"**{row['Task']}** ({row['Type']})")

# --- PAGE 3: ADMIN VIEW ---
elif page == "Admin View":
    st.title("Manager Overview 🔒")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Service Engineers", "12")
    with col2:
        st.metric("Total Parts Engineers", "8")
        
    st.subheader("Team Progress Snapshot")
    
    # Mock Data separated by role
    mock_team = pd.DataFrame({
        "Name": ["Alex (Service)", "Sam (Parts)", "Mike (Service)", "Jenny (Parts)"],
        "Role": ["Service Engineer", "Spare Parts Engineer", "Service Engineer", "Spare Parts Engineer"],
        "Progress": [15, 85, 45, 10]
    })
    
    fig = px.bar(
        mock_team, 
        x="Name", 
        y="Progress", 
        color="Role", 
        title="Completion by Engineer",
        color_discrete_map={"Service Engineer": "#EF553B", "Spare Parts Engineer": "#636EFA"}
    )
    st.plotly_chart(fig, use_container_width=True)
