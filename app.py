import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Tuple, Dict
import anthropic

# --- CONFIGURATION ---
st.set_page_config(page_title="SPAE Onboarding Hub", layout="wide", page_icon="⚙️", initial_sidebar_state="expanded")

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

THEME_IMAGES = {
    "SPE": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=600&q=80",
    "SE": "https://images.unsplash.com/photo-1581092335397-9583eb92d232?auto=format&fit=crop&w=600&q=80"
}

# --- AI CHATBOT SYSTEM PROMPT ---
def build_chatbot_system_prompt(role_key: str, role_label: str) -> str:
    faros_common = "\n".join(f"- {x}" for x in FAROS_CATALOG["Common"])
    faros_role = "\n".join(f"- {x}" for x in FAROS_CATALOG[role_key])
    nav_mandatory = "\n".join(f"- {x}" for x in NAVIGATOR_COURSES["Mandatory"])
    nav_role = "\n".join(f"- {x}" for x in NAVIGATOR_COURSES[role_key])
    toolkit = "\n".join(f"- {x}" for x in TOOLKIT["Common"] + TOOLKIT[role_key])
    acronyms = "\n".join(f"- {k}: {v}" for k, v in ACRONYMS.items())
    contacts = "\n".join(f"- {k}: {v}" for k, v in KEY_CONTACTS.items())
    links = "\n".join(f"- {k}: {v}" for k, v in IMPORTANT_LINKS.items())

    return f"""You are SPAE Buddy, a friendly and knowledgeable onboarding assistant for new {role_label} ({role_key}) employees at SPAE.

Your job is to help new hires navigate their onboarding smoothly. You are warm, concise, and encouraging. You answer questions about:
- System access (FAROS portal requests)
- Training courses (Navigator platform)
- Tools and internal portals
- Acronyms and jargon
- Contacts and support
- General onboarding advice

## Role
The employee's role is: {role_label} ({role_key})

## Systems to Request Access To (via FAROS portal)
Common systems for everyone:
{faros_common}

{role_key}-specific systems:
{faros_role}

## Training Courses (Navigator platform)
Mandatory for all:
{nav_mandatory}

{role_key}-specific:
{nav_role}

## Toolkit
{toolkit}

## Acronyms & Jargon
{acronyms}

## Key Contacts
{contacts}

## Important Links
{links}

## Guidelines
- Keep responses concise and friendly (2-4 sentences unless more detail is needed).
- If asked about something outside your knowledge, say so and suggest contacting HR or IT Helpdesk.
- Never make up system names, contacts, or links — only use the data above.
- Use bullet points for lists, but keep prose answers short and direct.
- Address the employee encouragingly — they're new and finding their feet!
"""


# --- 2. HELPER FUNCTIONS & ADVANCED UI STYLING ---

def inject_global_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, p, div, h1, h2, h3, h4, h5, h6, li, span, label, a {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .material-symbols-rounded, .material-icons {
            font-family: 'Material Symbols Rounded' !important;
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 5px;
            background: linear-gradient(90deg, #4f46e5, #0ea5e9, #10b981);
            z-index: 99999;
        }
        
        [data-testid="stMetricValue"] { font-weight: 800; font-size: 2.2rem; color: var(--text-color); }
        [data-testid="stMetricLabel"] > div { font-size: 0.95rem; font-weight: 600; opacity: 0.8; }

        .hero-card {
            padding: 2.0rem;
            border-radius: 1rem;
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 8px 24px -5px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .hero-card h1 { 
            margin-bottom: 0.2rem; 
            font-size: 2.5rem; 
            font-weight: 800;
            color: var(--text-color); 
            letter-spacing: -0.5px;
        }

        .pill {
            display: inline-flex; align-items: center; justify-content: center;
            padding: 0.4rem 1rem; border-radius: 999px; font-size: 0.85rem; font-weight: 700;
            border: 1px solid var(--primary-color); 
            background: linear-gradient(90deg, rgba(79, 70, 229, 0.1), rgba(16, 185, 129, 0.1));
            color: var(--primary-color);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
        }

        .muted { opacity: 0.85; font-size: 1.05rem; line-height: 1.6; }
        
        .checklist-row {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            border-left: 3px solid transparent;
            background-color: var(--secondary-background-color);
            margin-bottom: 0.5rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
        }
        .checklist-row:hover {
            border-left: 3px solid var(--primary-color);
            transform: translateX(4px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .mentor-badge {
            background-color: rgba(128, 128, 128, 0.15);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-color);
        }

        /* Chat bubble styles */
        .chat-user {
            background: linear-gradient(135deg, #4f46e5, #0ea5e9);
            color: white;
            padding: 0.6rem 0.9rem;
            border-radius: 1rem 1rem 0.2rem 1rem;
            margin: 0.4rem 0;
            font-size: 0.9rem;
            max-width: 85%;
            margin-left: auto;
        }
        .chat-assistant {
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,0.2);
            color: var(--text-color);
            padding: 0.6rem 0.9rem;
            border-radius: 1rem 1rem 1rem 0.2rem;
            margin: 0.4rem 0;
            font-size: 0.9rem;
            max-width: 85%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def create_donut_chart(progress: float):
    progress_pct = round(progress * 100)
    source = pd.DataFrame({
        "Category": ["Completed", "Remaining"],
        "Value": [progress_pct, 100 - progress_pct]
    })
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
    st.session_state['chat_history'] = []

def get_xp_and_level() -> Tuple[int, int, str]:
    df = pd.DataFrame(st.session_state['curriculum'])
    checklist_done = df['Status'].sum() if not df.empty else 0
    nav_done, nav_total = get_navigator_progress()
    xp = int((checklist_done * 20) + (nav_done * 50))
    max_xp = int((len(df) * 20) + (nav_total * 50)) if not df.empty else 100
    if xp == 0: level_name = "Welcome Aboard 👋"
    elif xp < max_xp * 0.4: level_name = "Rising Star ⭐"
    elif xp < max_xp * 0.8: level_name = "Momentum Builder 🚀"
    elif xp < max_xp: level_name = "Process Pro 🧠"
    else: level_name = "SPAE Champion 🏆"
    return xp, max_xp, level_name

def toggle_status(index: int) -> None:
    st.session_state['curriculum'][index]['Status'] = not st.session_state['curriculum'][index]['Status']
    if st.session_state['curriculum'][index]['Status']:
        task_name = st.session_state['curriculum'][index]['Task']
        st.toast(f"Boom! '{task_name}' is done. +20 XP! 🎉", icon="🔥")

def nav_click_callback(section: str, course: str) -> None:
    key = navigator_course_key(section, course)
    is_done = st.session_state[f"nav_{key}"]
    st.session_state['navigator_status'][key] = is_done
    if is_done:
        st.toast(f"Knowledge leveled up! Completed '{course}'. +50 XP! 🧠", icon="🌟")

def get_tech_stack_graph(role_key: str):
    if not has_graphviz: return None
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR', bgcolor='transparent')
    graph.attr('node', shape='box', style='filled', fontname='Helvetica, sans-serif', rx='5', ry='5')
    graph.attr('edge', color='#cbd5e1', fontcolor='#cbd5e1', fontname='Helvetica, sans-serif', fontsize='10')
    if role_key == "SE":
        graph.node('C', 'Customer Site', fillcolor='#bae6fd', color='#0284c7')
        graph.node('SF', 'Salesforce (CRM)', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('SAP', 'SAP Service Module', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('MOM', 'MOM App (Mobile)', fillcolor='#bbf7d0', color='#16a34a')
        graph.node('KOLA', 'KOLA (Parts DB)', shape='cylinder', fillcolor='#e9d5ff', color='#9333ea')
        graph.edge('C', 'SF', label=' Ticket Created')
        graph.edge('SF', 'SAP', label=' Job Dispatch')
        graph.edge('SAP', 'MOM', label=' Work Order Sync')
        graph.edge('MOM', 'KOLA', label=' Lookup Parts')
        graph.edge('MOM', 'SAP', label=' Submit Timesheet')
    else:
        graph.node('V', 'Vendor / Supplier', fillcolor='#bae6fd', color='#0284c7')
        graph.node('SAP', 'SAP GUI (ERP)', shape='ellipse', fillcolor='#fef08a', color='#ca8a04')
        graph.node('PLM', 'Agile PLM', shape='ellipse', fillcolor='#e9d5ff', color='#9333ea')
        graph.node('CAD', 'Creo / Vault', fillcolor='#bbf7d0', color='#16a34a')
        graph.node('GLOPPS', 'GLOPPS (Logistics)', shape='cylinder', fillcolor='#fecdd3', color='#e11d48')
        graph.edge('V', 'SAP', label=' Invoices')
        graph.edge('SAP', 'GLOPPS', label=' Inventory Check')
        graph.edge('PLM', 'SAP', label=' Part Number Gen')
        graph.edge('CAD', 'PLM', label=' Drawings Upload')
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

# --- AI CHATBOT FUNCTION ---
def get_ai_response(user_message: str, chat_history: list, role_key: str, role_label: str) -> str:
    """Call Claude API with full conversation history."""
    try:
        client = anthropic.Anthropic()
        system_prompt = build_chatbot_system_prompt(role_key, role_label)

        # Build messages from history + new user message
        messages = []
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=512,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        return f"⚠️ Sorry, I couldn't connect right now. Please try again or contact IT Helpdesk (Ext. 4040). \n\n_(Error: {e})_"


# --- 3. STATE INITIALIZATION ---
if 'user_role' not in st.session_state: st.session_state['user_role'] = "SPE (Spare Parts Engineer)"
if 'curriculum' not in st.session_state:
    st.session_state['curriculum'] = [{**t, "Status": False} for t in get_checklist_data(st.session_state['user_role'])]
if 'chat_history' not in st.session_state: st.session_state['chat_history'] = []
init_navigator_status()
inject_global_css()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px; margin-top: -10px;">
            <div style="background: linear-gradient(135deg, #4f46e5, #0ea5e9); padding: 10px; border-radius: 12px; color: white; font-size: 22px; line-height: 1; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);">
                ⚙️
            </div>
            <h1 style="margin: 0; padding: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; color: var(--text-color);">SPAE Hub</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    selected_role = st.selectbox("Current Role", list(ROLE_KEY_MAP.keys()), index=list(ROLE_KEY_MAP.keys()).index(st.session_state['user_role']))
    if selected_role != st.session_state['user_role']:
        st.session_state['user_role'] = selected_role
        reset_user()
        st.rerun()

    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Requests & Learning", "Checklist", "Mentor Guide", "Good to Know"], label_visibility="collapsed")
    st.markdown("---")

    # --- 🤖 AI CHATBOT POPOVER ---
    with st.popover("🤖 Ask SPAE Buddy (AI)", use_container_width=True):
        role_key_chat = get_role_key(st.session_state['user_role'])
        role_label_chat = st.session_state['user_role'].split("(")[0].strip()

        st.markdown(
            f"**SPAE Buddy** 🤖  \n"
            f"<span style='font-size:0.8rem; opacity:0.7;'>Your AI onboarding assistant for {role_key_chat}s. Ask me anything!</span>",
            unsafe_allow_html=True
        )

        # Suggested prompts (shown when chat is empty)
        if not st.session_state['chat_history']:
            st.markdown("<div style='font-size:0.8rem; opacity:0.6; margin-bottom:4px;'>Try asking:</div>", unsafe_allow_html=True)
            suggestions = [
                f"What systems do I need to request access for?",
                "What's LOTO?",
                "Who do I contact for IT issues?",
                "What training is mandatory for everyone?",
            ]
            for suggestion in suggestions:
                if st.button(suggestion, key=f"suggest_{suggestion[:20]}", use_container_width=True):
                    # Add to history and get response
                    st.session_state['chat_history'].append({"role": "user", "content": suggestion})
                    with st.spinner("Thinking..."):
                        reply = get_ai_response(suggestion, st.session_state['chat_history'][:-1], role_key_chat, role_label_chat)
                    st.session_state['chat_history'].append({"role": "assistant", "content": reply})
                    st.rerun()

        # Render chat history
        for msg in st.session_state['chat_history']:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-assistant'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

        # Input area
        user_input = st.text_input(
            "Message SPAE Buddy",
            placeholder="e.g. What is KOLA used for?",
            key="chat_input",
            label_visibility="collapsed"
        )

        col_send, col_clear = st.columns([3, 1])
        with col_send:
            send_clicked = st.button("Send ➤", use_container_width=True, type="primary")
        with col_clear:
            if st.button("🗑️", use_container_width=True, help="Clear chat"):
                st.session_state['chat_history'] = []
                st.rerun()

        if send_clicked and user_input.strip():
            st.session_state['chat_history'].append({"role": "user", "content": user_input.strip()})
            with st.spinner("SPAE Buddy is thinking..."):
                reply = get_ai_response(user_input.strip(), st.session_state['chat_history'][:-1], role_key_chat, role_label_chat)
            st.session_state['chat_history'].append({"role": "assistant", "content": reply})
            st.rerun()

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
    xp, max_xp, level_name = get_xp_and_level()
    
    st.markdown(
        f"""
        <div class="hero-card">
            <span class="pill">{level_name} • {xp} / {max_xp} XP</span>
            <h1>Welcome to the team, {role_label} 👋</h1>
            <p class="muted">Your personalized command center for mastering the {role_key} role. Track your gear, request access, and complete your training all in one place.</p>
        </div>
        """, unsafe_allow_html=True
    )

    checklist_p, navigator_p, overall_p = get_overall_progress()
    overall_percent = int(overall_p * 100)
    nav_done, nav_total = get_navigator_progress()
    df = pd.DataFrame(st.session_state['curriculum'])

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
        st.success("🎉 Incredible work! You are now a SPAE Champion.")

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
    st.markdown("Manage your system access and required certifications to earn more XP.")

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
                img_col, text_col = st.columns([1.2, 3])
                with img_col:
                    st.image(THEME_IMAGES[role_key], use_container_width=True)
                with text_col:
                    for item in FAROS_CATALOG[role_key]: st.markdown(f"🔹 **{item}**")

    with tab2:
        completed_nav, total_nav = get_navigator_progress()
        st.progress(completed_nav / total_nav if total_nav > 0 else 0, text=f"Course Completion: {completed_nav}/{total_nav}")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🚨 Mandatory Training (50 XP ea)")
                for course in NAVIGATOR_COURSES["Mandatory"]:
                    key = navigator_course_key("Mandatory", course)
                    st.checkbox(course, value=st.session_state['navigator_status'].get(key, False), key=f"nav_{key}", on_change=nav_click_callback, args=("Mandatory", course))
        with c2:
            with st.container(border=True):
                st.subheader(f"🧠 {role_key} Specific (50 XP ea)")
                for course in NAVIGATOR_COURSES[role_key]:
                    key = navigator_course_key(role_key, course)
                    st.checkbox(course, value=st.session_state['navigator_status'].get(key, False), key=f"nav_{key}", on_change=nav_click_callback, args=(role_key, course))

    with tab3:
        with st.container(border=True):
            st.subheader("🔗 Essential Tools")
            img_col, text_col = st.columns([1, 4])
            with img_col:
                st.image(THEME_IMAGES[role_key], use_container_width=True)
            with text_col:
                for item in TOOLKIT["Common"] + TOOLKIT[role_key]: st.markdown(f"- {item}")

# PAGE: CHECKLIST
elif page == "Checklist":
    st.markdown("## ✅ Master Checklist")
    df = pd.DataFrame(st.session_state['curriculum'])
    df['idx'] = df.index

    search_query = st.text_input("🔍 Filter tasks by keyword...", "").lower()

    if not df.empty:
        unique_phases = df['Phase'].unique().tolist()
        for phase in unique_phases:
            phase_tasks = df[df['Phase'] == phase]
            if search_query:
                phase_tasks = phase_tasks[phase_tasks['Task'].str.lower().str.contains(search_query) | phase_tasks['Category'].str.lower().str.contains(search_query)]
                if phase_tasks.empty: continue
            done = int(phase_tasks['Status'].sum())
            total = len(phase_tasks)
            with st.container(border=True):
                st.markdown(f"### 🗓 {phase} ({done}/{total})")
                for _, row in phase_tasks.iterrows():
                    idx = int(row['idx'])
                    st.markdown('<div class="checklist-row">', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([1, 14, 4])
                    with c1:
                        st.checkbox("Done", value=row['Status'], key=f"chk_{idx}", on_change=toggle_status, args=(idx,), label_visibility="collapsed")
                    with c2:
                        task_text = f"~~**{row['Task']}**~~" if row['Status'] else f"**{row['Task']}**"
                        st.markdown(task_text)
                        st.caption(f"Category: {row['Category']}")
                    with c3:
                        st.markdown(f"<div style='text-align:right; margin-top: 5px;'><span class='mentor-badge'>👤 {row['Mentor']}</span></div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# PAGE: MENTOR GUIDE
elif page == "Mentor Guide":
    st.markdown("## 📘 Mentor's Playbook")
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
