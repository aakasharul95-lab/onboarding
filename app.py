import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Service & Parts Onboarding", layout="wide")

# --- MOCK DATA & STATE MANAGEMENT ---
# In a real app, this would come from a SQL Database or Google Sheet
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {
        'New Hire': 'Alex (Service Eng)',
        'Role': 'Service Engineer',
        'Start Date': '2023-10-01'
    }

# Initialize the checklist/curriculum if not present
if 'curriculum' not in st.session_state:
    st.session_state['curriculum'] = [
        # Administrative
        {"id": 1, "Category": "Admin", "Task": "Collect Safety Gear (PPE)", "Status": False, "Type": "Checklist"},
        {"id": 2, "Category": "Admin", "Task": "Setup Company Email & Slack", "Status": True, "Type": "Checklist"},
        # Technical - Spare Parts
        {"id": 3, "Category": "Spare Parts", "Task": "Intro to ERP System (SAP/Oracle)", "Status": False, "Type": "Module"},
        {"id": 4, "Category": "Spare Parts", "Task": "Understanding BOM (Bill of Materials)", "Status": False, "Type": "Module"},
        # Technical - Service
        {"id": 5, "Category": "Service", "Task": "LOTO (Lock Out Tag Out) Certification", "Status": False, "Type": "Module"},
        {"id": 6, "Category": "Service", "Task": "Field Service Report Writing", "Status": False, "Type": "Module"},
    ]

# --- HELPER FUNCTIONS ---
def get_progress():
    df = pd.DataFrame(st.session_state['curriculum'])
    total = len(df)
    completed = len(df[df['Status'] == True])
    return int((completed / total) * 100)

def toggle_status(index):
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔧 Onboarding Hub")
page = st.sidebar.radio("Navigate", ["Dashboard", "Learning Modules", "Admin View"])
st.sidebar.markdown("---")
st.sidebar.info(f"Logged in as: **{st.session_state['user_data']['New Hire']}**")

# --- PAGE 1: DASHBOARD ---
if page == "Dashboard":
    st.title(f"Welcome, {st.session_state['user_data']['New Hire']}! 👋")
    
    # Metrics Row
    col1, col2, col3 = st.columns(3)
    progress = get_progress()
    
    with col1:
        st.metric("Overall Progress", f"{progress}%")
    with col2:
        st.metric("Days on Team", "14 Days")
    with col3:
        remaining = len([x for x in st.session_state['curriculum'] if not x['Status']])
        st.metric("Tasks Remaining", remaining)

    # Progress Bar
    st.progress(progress / 100)
    
    # Motivation Logic
    if progress == 100:
        st.success("🎉 Amazing! You have completed all onboarding tasks!")
    elif progress > 50:
        st.info("🚀 You are more than halfway there! Keep going.")
    
    st.subheader("Your Upcoming Tasks")
    df = pd.DataFrame(st.session_state['curriculum'])
    pending_tasks = df[df['Status'] == False]
    
    if not pending_tasks.empty:
        st.dataframe(pending_tasks[['Category', 'Task', 'Type']], use_container_width=True)
    else:
        st.write("No pending tasks. Great job!")

# --- PAGE 2: LEARNING MODULES ---
elif page == "Learning Modules":
    st.title("📚 Learning & Checklist")
    
    tabs = st.tabs(["Admin & Gear", "Technical Skills", "Service Protocols"])
    
    # Helper to render tasks by category
    def render_tasks(category_filter):
        for i, item in enumerate(st.session_state['curriculum']):
            # Filter logic
            is_category = item['Category'] in category_filter
            
            if is_category:
                col_a, col_b = st.columns([0.1, 0.9])
                with col_a:
                    # Checkbox to toggle state
                    checked = st.checkbox(
                        "Done", 
                        value=item['Status'], 
                        key=f"task_{i}",
                        on_change=toggle_status,
                        args=(i,)
                    )
                with col_b:
                    st.markdown(f"**{item['Task']}**")
                    if item['Type'] == "Module":
                        with st.expander("📖 View Material / Instructions"):
                            st.write("Here you would embed a PDF, a Video, or text instructions.")
                            st.info(f"Goal: Learn about {item['Task']}")
                            # Example of embedding a video (placeholder)
                            # st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    with tabs[0]:
        st.header("Administrative & Safety Gear")
        render_tasks(["Admin"])
        
    with tabs[1]:
        st.header("Spare Parts & Technical")
        render_tasks(["Spare Parts"])
        
    with tabs[2]:
        st.header("Service Engineering")
        render_tasks(["Service"])

# --- PAGE 3: ADMIN VIEW ---
elif page == "Admin View":
    st.title("Manager Overview 🔒")
    st.warning("This view is for Managers/Mentors.")
    
    # Charts
    st.subheader("Team Progress")
    
    # Mock data for the whole team
    team_data = pd.DataFrame({
        "Engineer": ["Alex", "Sarah", "Mike", "David"],
        "Progress": [get_progress(), 85, 40, 10],
        "Role": ["Service", "Parts", "Service", "Parts"]
    })
    
    fig = px.bar(team_data, x="Engineer", y="Progress", color="Role", title="Onboarding Completion %", range_y=[0,100])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Action Items")
    st.write("These engineers have been stuck on the same module for > 3 days:")
    st.error("⚠️ Mike: LOTO Certification")