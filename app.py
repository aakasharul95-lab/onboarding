"""
SPAE Onboarding Hub — Main Application
=======================================
This file contains only app logic, routing, and UI rendering.
All editable content (tasks, courses, quizzes, etc.) lives in the content/ package.

To update content  → edit the relevant file in content/
To update UI/logic → edit this file

AZURE APP REGISTRATION SETUP:
──────────────────────────────
1. Go to https://portal.azure.com → Azure Active Directory → App registrations → New registration
2. Name: "SPAE Onboarding Hub"
3. Supported account types: "Accounts in this organizational directory only"
4. Redirect URI: Web → https://spaeonboardingtool.azurewebsites.net/
   (also add http://localhost:8501/ for local development)
5. Click Register → copy Application (client) ID  → client_id
6. Copy Directory (tenant) ID                     → tenant_id
7. Certificates & secrets → New client secret     → client_secret
8. API permissions → Microsoft Graph → Delegated:
   openid, profile, email, User.Read → Grant admin consent

.streamlit/secrets.toml  (never commit this file):
────────────────────────────────────────────────────
[azure]
client_id     = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
tenant_id     = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
client_secret = "your-client-secret-value"
redirect_uri  = "https://spaeonboardingtool.azurewebsites.net/"

[mongo]
uri = "mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
db  = "spae_hub"

INSTALL:
─────────
pip install streamlit pymongo dnspython msal
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Tuple, Dict, Optional
from datetime import date, datetime, timedelta

# ── All editable content lives in content/ ────────────────────────────────────
from content import (
    get_checklist_data,
    NAVIGATOR_COURSES,
    FAROS_CATALOG,
    TOOLKIT,
    QUICK_LINKS,
    IMPORTANT_LINKS,
    THEME_IMAGES,
    GLOSSARY,
    FAQS,
    ALL_BADGES,
    ACRONYMS,
)
from content.courses import ROLE_KEY_MAP
from content.systems import KEY_CONTACTS

# ── Optional dependencies ─────────────────────────────────────────────────────
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False

try:
    import msal
    MSAL_AVAILABLE = True
except ImportError:
    MSAL_AVAILABLE = False

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ModuleNotFoundError:
    HAS_GRAPHVIZ = False

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SPAE Onboarding Hub",
    layout="wide",
    page_icon="⚙️",
    initial_sidebar_state="expanded",
)


# =============================================================================
# MSAL AUTHENTICATION
# =============================================================================

SCOPES = ["openid", "profile", "email", "User.Read"]


@st.cache_resource
def get_msal_app() -> Optional[object]:
    if not MSAL_AVAILABLE:
        st.error("❌ `msal` not installed. Run: pip install msal")
        return None
    try:
        cfg       = st.secrets["azure"]
        authority = f"https://login.microsoftonline.com/{cfg['tenant_id']}"
        return msal.ConfidentialClientApplication(
            client_id=cfg["client_id"],
            client_credential=cfg["client_secret"],
            authority=authority,
        )
    except KeyError:
        st.error("❌ Azure credentials missing from st.secrets.")
        return None


def get_redirect_uri() -> str:
    try:
        return st.secrets["azure"]["redirect_uri"]
    except KeyError:
        return "http://localhost:8501/"


def build_auth_url() -> str:
    app = get_msal_app()
    if app is None:
        return "#"
    return app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=get_redirect_uri(),
        state=st.session_state.get("auth_state", "auth"),
    )


def exchange_code_for_token(auth_code: str) -> Optional[Dict]:
    app = get_msal_app()
    if app is None:
        return None
    result = app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=SCOPES,
        redirect_uri=get_redirect_uri(),
    )
    if "error" in result:
        st.error(f"Authentication error: {result.get('error_description', result['error'])}")
        return None
    return result


def get_user_claims(token_result: Dict) -> Dict:
    claims = token_result.get("id_token_claims", {})
    return {
        "oid":        claims.get("oid", ""),
        "name":       claims.get("name", ""),
        "email":      claims.get("preferred_username", claims.get("email", "")),
        "given_name": claims.get(
            "given_name",
            claims.get("name", "").split()[0] if claims.get("name") else "",
        ),
    }


def handle_auth_callback() -> bool:
    params = st.query_params
    code   = params.get("code",  None)
    error  = params.get("error", None)
    if error:
        st.error(f"Microsoft login failed: {params.get('error_description', error)}")
        st.query_params.clear()
        return False
    if code and not st.session_state.get("authenticated"):
        with st.spinner("Completing sign-in with Microsoft…"):
            result = exchange_code_for_token(code)
        if result:
            claims = get_user_claims(result)
            st.session_state.update({
                "authenticated":    True,
                "azure_oid":        claims["oid"],
                "azure_name":       claims["name"],
                "azure_email":      claims["email"],
                "azure_given_name": claims["given_name"],
                "access_token":     result.get("access_token", ""),
            })
            st.query_params.clear()
            return True
    return False


def show_login_page():
    inject_global_css()
    auth_url = build_auth_url()
    st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;min-height:80vh;text-align:center;">
            <div style="font-size:4rem;margin-bottom:1rem;">⚙️</div>
            <h1 style="font-size:2.4rem;font-weight:800;margin-bottom:0.5rem;">SPAE Onboarding Hub</h1>
            <p style="opacity:0.65;font-size:1.1rem;max-width:420px;margin-bottom:2rem;">
                Your personalised 90-day onboarding companion.<br>
                Sign in with your company Microsoft account to continue.
            </p>
            <a href="{auth_url}" target="_self"
               style="display:inline-flex;align-items:center;gap:10px;
                      background:#0078d4;color:white;font-weight:700;
                      padding:0.85rem 2rem;border-radius:0.6rem;
                      text-decoration:none;font-size:1rem;
                      box-shadow:0 4px 14px rgba(0,120,212,0.35);">
                <svg width="20" height="20" viewBox="0 0 21 21" xmlns="http://www.w3.org/2000/svg">
                  <rect x="1"  y="1"  width="9" height="9" fill="#f25022"/>
                  <rect x="11" y="1"  width="9" height="9" fill="#7fba00"/>
                  <rect x="1"  y="11" width="9" height="9" fill="#00a4ef"/>
                  <rect x="11" y="11" width="9" height="9" fill="#ffb900"/>
                </svg>
                Sign in with Microsoft
            </a>
            <p style="margin-top:1.5rem;font-size:0.8rem;opacity:0.45;">
                Secured by Azure Active Directory · Data stays within your organisation
            </p>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MONGODB LAYER
# =============================================================================

@st.cache_resource
def get_mongo_client():
    if not MONGO_AVAILABLE:
        return None
    try:
        client = MongoClient(st.secrets["mongo"]["uri"], serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client
    except Exception:
        return None


def get_collection():
    client = get_mongo_client()
    if client is None:
        return None
    try:
        return client[st.secrets["mongo"].get("db", "spae_hub")]["users"]
    except Exception:
        return None


def load_user_from_db(oid: str) -> Optional[Dict]:
    col = get_collection()
    if col is None:
        return None
    try:
        return col.find_one({"_id": oid})
    except Exception:
        return None


def save_user_to_db(oid: str, data: Dict) -> bool:
    col = get_collection()
    if col is None:
        return False
    try:
        col.update_one(
            {"_id": oid},
            {"$set": {
                **data,
                "_id":          oid,
                "azure_email":  st.session_state.get("azure_email", ""),
                "azure_name":   st.session_state.get("azure_name", ""),
                "last_updated": datetime.utcnow().isoformat(),
            }},
            upsert=True,
        )
        return True
    except Exception as e:
        st.warning(f"DB write error: {e}")
        return False


def build_db_payload() -> Dict:
    curriculum    = st.session_state.get("curriculum", [])
    checklist_map = {row["Task"]: bool(row["Status"]) for row in curriculum}
    return {
        "profile": {
            "name":       st.session_state.get("user_name", ""),
            "role":       st.session_state.get("user_role", ""),
            "start_date": str(st.session_state.get("start_date", date.today())),
            "buddy":      st.session_state.get("buddy_name", ""),
            "manager":    st.session_state.get("manager_name", ""),
        },
        "checklist":        checklist_map,
        "navigator_status": st.session_state.get("navigator_status", {}),
        "quiz": {
            "perfect_quiz": st.session_state.get("perfect_quiz", False),
            "quiz_state":   st.session_state.get("quiz_state", {}),
        },
        "badges": {
            "session_completions": st.session_state.get("session_completions", 0),
        },
    }


def restore_from_db(doc: Dict) -> None:
    profile = doc.get("profile", {})
    st.session_state["user_name"]    = profile.get("name", st.session_state.get("azure_given_name", ""))
    st.session_state["user_role"]    = profile.get("role", list(ROLE_KEY_MAP.keys())[0])
    try:
        st.session_state["start_date"] = date.fromisoformat(
            profile.get("start_date", str(date.today()))
        )
    except ValueError:
        st.session_state["start_date"] = date.today()
    st.session_state["buddy_name"]   = profile.get("buddy",   "Your Buddy")
    st.session_state["manager_name"] = profile.get("manager", "Your Manager")

    raw_data      = get_checklist_data(st.session_state["user_role"])
    checklist_map = doc.get("checklist", {})
    st.session_state["curriculum"] = [
        {**t, "Status": checklist_map.get(t["Task"], False)} for t in raw_data
    ]
    st.session_state["navigator_status"] = doc.get("navigator_status", {})
    init_navigator_status()

    quiz = doc.get("quiz", {})
    st.session_state["perfect_quiz"] = quiz.get("perfect_quiz", False)
    st.session_state["quiz_state"]   = quiz.get("quiz_state", {})
    st.session_state["session_completions"] = doc.get("badges", {}).get("session_completions", 0)
    st.session_state["wizard_done"]  = True


def sync_to_db() -> None:
    oid = st.session_state.get("azure_oid", "")
    if oid:
        save_user_to_db(oid, build_db_payload())


# =============================================================================
# STATE HELPERS
# =============================================================================

def get_role_key(full_role: str) -> str:
    return ROLE_KEY_MAP.get(full_role, "SPE")


def navigator_course_key(section: str, course: str) -> str:
    return f"{section}::{course}"


def init_navigator_status() -> None:
    role_key = get_role_key(st.session_state.get("user_role", list(ROLE_KEY_MAP.keys())[0]))
    st.session_state.setdefault("navigator_status", {})
    status = st.session_state["navigator_status"]
    for c in NAVIGATOR_COURSES["Mandatory"]:
        status.setdefault(navigator_course_key("Mandatory", c), False)
    for c in NAVIGATOR_COURSES.get(role_key, []):
        status.setdefault(navigator_course_key(role_key, c), False)


def get_navigator_progress() -> Tuple[int, int]:
    role_key = get_role_key(st.session_state["user_role"])
    status   = st.session_state.get("navigator_status", {})
    all_c    = (
        [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]]
        + [(role_key, c) for c in NAVIGATOR_COURSES.get(role_key, [])]
    )
    return (
        sum(1 for s, c in all_c if status.get(navigator_course_key(s, c), False)),
        len(all_c),
    )


def get_overall_progress() -> Tuple[float, float, float]:
    df = pd.DataFrame(st.session_state["curriculum"])
    cp = df["Status"].sum() / len(df) if not df.empty else 0.0
    nd, nt = get_navigator_progress()
    np_ = nd / nt if nt > 0 else 0.0
    return cp, np_, 0.5 * cp + 0.5 * np_


def get_xp_and_level() -> Tuple[int, int, str]:
    df = pd.DataFrame(st.session_state["curriculum"])
    cd = int(df["Status"].sum()) if not df.empty else 0
    nd, nt = get_navigator_progress()
    xp     = cd * 20 + nd * 50
    max_xp = len(df) * 20 + nt * 50 if not df.empty else 100
    if xp == 0:              lvl = "Welcome Aboard 👋"
    elif xp < max_xp * .30: lvl = "Rising Star ⭐"
    elif xp < max_xp * .60: lvl = "Momentum Builder 🚀"
    elif xp < max_xp * .85: lvl = "Process Pro 🧠"
    elif xp < max_xp:        lvl = "Almost There 🔥"
    else:                    lvl = "SPAE Champion 🏆"
    return xp, max_xp, lvl


def get_earned_badges() -> List[str]:
    df  = pd.DataFrame(st.session_state["curriculum"])
    nd, nt = get_navigator_progress()
    _, _, op = get_overall_progress()
    w1  = df[df["Phase"].isin(["Day 1", "Week 1"])]
    cd  = int(df["Status"].sum()) if not df.empty else 0
    earned = []
    if cd >= 1:                                               earned.append("first_step")
    if not w1.empty and w1["Status"].sum() == len(w1):       earned.append("week1_done")
    if op >= 0.5:                                             earned.append("half_way")
    if nt > 0 and nd == nt:                                   earned.append("learning_done")
    if op >= 1.0:                                             earned.append("champion")
    if st.session_state.get("session_completions", 0) >= 5:  earned.append("speed_runner")
    return earned


def reset_user() -> None:
    raw = get_checklist_data(st.session_state["user_role"])
    st.session_state["curriculum"]          = [{**t, "Status": False} for t in raw]
    st.session_state["navigator_status"]    = {}
    init_navigator_status()
    st.session_state["quiz_state"]          = {}
    st.session_state["session_completions"] = 0
    st.session_state["perfect_quiz"]        = False


def toggle_status(index: int) -> None:
    was = st.session_state["curriculum"][index]["Status"]
    st.session_state["curriculum"][index]["Status"] = not was
    if not was:
        st.toast(f"✅ '{st.session_state['curriculum'][index]['Task']}' done! +20 XP", icon="🔥")
        st.session_state["session_completions"] = st.session_state.get("session_completions", 0) + 1
    sync_to_db()


def nav_click_callback(section: str, course: str) -> None:
    key     = navigator_course_key(section, course)
    is_done = st.session_state[f"nav_{key}"]
    st.session_state["navigator_status"][key] = is_done
    if is_done:
        st.toast(f"🎓 '{course}' complete! +50 XP", icon="🌟")
    sync_to_db()


def days_since_start() -> int:
    return max(0, (date.today() - st.session_state.get("start_date", date.today())).days)


# =============================================================================
# CSS
# =============================================================================

def inject_global_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        html,body,p,div,h1,h2,h3,h4,h5,h6,li,span,label,a{font-family:'Plus Jakarta Sans',sans-serif;}
        .stApp::before{content:"";position:fixed;top:0;left:0;right:0;height:5px;
            background:linear-gradient(90deg,#4f46e5,#0ea5e9,#10b981);z-index:99999;}
        [data-testid="stMetricValue"]{font-weight:800;font-size:2.2rem;}
        [data-testid="stMetricLabel"]>div{font-size:0.95rem;font-weight:600;opacity:0.8;}
        .hero-card{padding:2rem;border-radius:1rem;
            background-color:var(--secondary-background-color);
            border:1px solid rgba(128,128,128,0.2);
            box-shadow:0 8px 24px -5px rgba(0,0,0,0.1);margin-bottom:2rem;}
        .hero-card h1{font-size:2.5rem;font-weight:800;letter-spacing:-0.5px;margin-bottom:0.2rem;}
        .pill{display:inline-flex;align-items:center;padding:0.4rem 1rem;border-radius:999px;
            font-size:0.85rem;font-weight:700;border:1px solid var(--primary-color);
            background:linear-gradient(90deg,rgba(79,70,229,0.1),rgba(16,185,129,0.1));
            color:var(--primary-color);}
        .badge-card{padding:1rem;border-radius:0.75rem;text-align:center;
            background-color:var(--secondary-background-color);
            border:1px solid rgba(128,128,128,0.15);transition:transform 0.2s;}
        .badge-card:hover{transform:translateY(-3px);}
        .badge-locked{opacity:0.35;filter:grayscale(1);}
        .badge-icon{font-size:2.5rem;line-height:1;}
        .badge-name{font-weight:700;font-size:0.85rem;margin-top:4px;}
        .badge-desc{font-size:0.75rem;opacity:0.7;margin-top:2px;}
        .checklist-row{padding:0.5rem 1rem;border-radius:0.5rem;
            border-left:3px solid transparent;
            background-color:var(--secondary-background-color);
            margin-bottom:0.5rem;transition:all 0.2s cubic-bezier(0.4,0,0.2,1);}
        .checklist-row:hover{border-left:3px solid var(--primary-color);transform:translateX(4px);}
        .tip-box{font-size:0.8rem;opacity:0.75;padding:2px 8px;
            border-left:2px solid #0ea5e9;margin-top:2px;}
        .mentor-badge{background:rgba(128,128,128,0.15);padding:4px 8px;
            border-radius:6px;font-size:0.8rem;font-weight:600;}
        .days-counter{font-size:3rem;font-weight:800;color:var(--primary-color);line-height:1;}
        .muted{opacity:0.85;font-size:1.05rem;line-height:1.6;}
        </style>
    """, unsafe_allow_html=True)


# =============================================================================
# CHART & CERTIFICATE
# =============================================================================

def create_donut_chart(progress: float):
    pct = round(progress * 100)
    src = pd.DataFrame({"Category": ["Completed", "Remaining"], "Value": [pct, 100 - pct]})
    return (
        alt.Chart(src)
        .mark_arc(innerRadius=60, cornerRadius=15)
        .encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(
                field="Category", type="nominal",
                scale=alt.Scale(
                    domain=["Completed", "Remaining"],
                    range=["#3b82f6", "rgba(128,128,128,0.15)"],
                ),
                legend=None,
            ),
            tooltip=["Category", "Value"],
        )
        .properties(width=220, height=220)
    )


def generate_certificate_html() -> str:
    name  = st.session_state.get("user_name", "Team Member")
    role  = st.session_state.get("user_role", "")
    mgr   = st.session_state.get("manager_name", "Line Manager")
    today = date.today().strftime("%B %d, %Y")
    return f"""<!DOCTYPE html><html><head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');
        body{{margin:0;background:#f8f7f4;display:flex;justify-content:center;align-items:center;min-height:100vh;}}
        .cert{{width:780px;padding:60px 70px;background:white;border:12px solid transparent;
               border-image:linear-gradient(135deg,#4f46e5,#0ea5e9,#10b981) 1;
               text-align:center;font-family:'Plus Jakarta Sans',sans-serif;
               box-shadow:0 20px 60px rgba(0,0,0,0.12);}}
        h1{{font-family:'Playfair Display',serif;font-size:2.6rem;color:#1f2937;margin:0 0 8px;}}
        .name{{font-family:'Playfair Display',serif;font-size:3.2rem;color:#4f46e5;
               border-bottom:2px solid #e5e7eb;padding-bottom:12px;margin-bottom:24px;}}
        .role-badge{{display:inline-block;background:linear-gradient(90deg,#4f46e5,#0ea5e9);
                     color:white;padding:8px 24px;border-radius:999px;font-weight:600;margin-bottom:32px;}}
        .footer{{display:flex;justify-content:space-between;margin-top:40px;
                 border-top:1px solid #e5e7eb;padding-top:24px;color:#9ca3af;font-size:0.8rem;}}
    </style></head><body>
    <div class="cert">
        <div style="font-size:3rem">⚙️</div>
        <p style="color:#6b7280;letter-spacing:3px;text-transform:uppercase;font-size:0.9rem">
            SPAE Onboarding Hub</p>
        <h1>Certificate of Completion</h1>
        <p style="color:#6b7280">This certifies that</p>
        <div class="name">{name}</div>
        <div class="role-badge">{role}</div>
        <p style="color:#374151;max-width:560px;margin:0 auto 32px;line-height:1.7">
            has successfully completed the SPAE onboarding programme, fulfilling all required
            training modules, system access tasks, and milestone activities.
        </p>
        <div class="footer">
            <div style="text-align:left">
                <b style="color:#374151">{mgr}</b><br>Line Manager
            </div>
            <div style="font-size:2rem">🏆</div>
            <div style="text-align:right">
                <b style="color:#374151">{today}</b><br>Date of Completion
            </div>
        </div>
    </div></body></html>"""


def get_tech_stack_graph(role_key: str):
    if not HAS_GRAPHVIZ:
        return None
    g = graphviz.Digraph()
    g.attr(rankdir="LR", bgcolor="transparent")
    g.attr("node", shape="box", style="filled", fontname="Helvetica, sans-serif")
    g.attr("edge", color="#cbd5e1", fontcolor="#cbd5e1", fontsize="10")
    if role_key == "SE":
        g.node("C",   "Customer Site",      fillcolor="#bae6fd", color="#0284c7")
        g.node("SF",  "Salesforce (CRM)",   shape="ellipse", fillcolor="#fef08a", color="#ca8a04")
        g.node("SAP", "SAP Service Module", shape="ellipse", fillcolor="#fef08a", color="#ca8a04")
        g.node("MOM", "MOM App (Mobile)",   fillcolor="#bbf7d0", color="#16a34a")
        g.node("KOLA","KOLA (Parts DB)",    shape="cylinder",   fillcolor="#e9d5ff", color="#9333ea")
        g.edge("C",   "SF",  label=" Ticket")
        g.edge("SF",  "SAP", label=" Dispatch")
        g.edge("SAP", "MOM", label=" Work Order")
        g.edge("MOM", "KOLA",label=" Lookup")
        g.edge("MOM", "SAP", label=" Timesheet")
    else:
        g.node("V",     "Vendor / Supplier",  fillcolor="#bae6fd", color="#0284c7")
        g.node("SAP",   "SAP GUI (ERP)",      shape="ellipse",   fillcolor="#fef08a", color="#ca8a04")
        g.node("PLM",   "Agile PLM",          shape="ellipse",   fillcolor="#e9d5ff", color="#9333ea")
        g.node("CAD",   "Creo / Vault",       fillcolor="#bbf7d0", color="#16a34a")
        g.node("GLOPPS","GLOPPS (Logistics)", shape="cylinder",   fillcolor="#fecdd3", color="#e11d48")
        g.edge("V",   "SAP",    label=" Invoices")
        g.edge("SAP", "GLOPPS", label=" Inventory")
        g.edge("PLM", "SAP",    label=" Part No.")
        g.edge("CAD", "PLM",    label=" Drawings")
    return g


# =============================================================================
# ONBOARDING WIZARD
# =============================================================================

def show_wizard():
    given_name = st.session_state.get("azure_given_name", "")
    email      = st.session_state.get("azure_email", "")
    st.markdown(f"""
        <div style="max-width:640px;margin:40px auto 0 auto;text-align:center;">
            <div style="font-size:3rem;">⚙️</div>
            <h1 style="font-size:2rem;font-weight:800;margin:8px 0 4px;">
                Welcome, {given_name or 'there'}!
            </h1>
            <p style="opacity:0.7;">
                Signed in as <strong>{email}</strong>.<br>
                Let's personalise your onboarding — takes 30 seconds.
            </p>
        </div>
    """, unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        with st.container(border=True):
            st.markdown("#### 👤 Your Details")
            name  = st.text_input("Preferred First Name", value=given_name, placeholder="e.g. Jordan")
            role  = st.selectbox("Your Role", list(ROLE_KEY_MAP.keys()))
            start = st.date_input(
                "Your Start Date",
                value=date.today(),
                max_value=date.today() + timedelta(days=30),
            )
            st.markdown("#### 🤝 Your Support Network")
            buddy   = st.text_input("Buddy's Name",   placeholder="e.g. Sarah J.")
            manager = st.text_input("Manager's Name", placeholder="e.g. Mike R.")
            st.markdown("")
            if st.button("🚀 Start My Onboarding", use_container_width=True, type="primary"):
                if not name.strip():
                    st.error("Please enter your preferred name to continue.")
                else:
                    st.session_state.update({
                        "user_name":    name.strip(),
                        "user_role":    role,
                        "start_date":   start,
                        "buddy_name":   buddy.strip()   or "Your Buddy",
                        "manager_name": manager.strip() or "Your Manager",
                        "wizard_done":  True,
                    })
                    reset_user()
                    sync_to_db()
                    st.rerun()


# =============================================================================
# BOOTSTRAP — runs on every page load
# =============================================================================

inject_global_css()
handle_auth_callback()

# Gate: must be authenticated
if not st.session_state.get("authenticated"):
    show_login_page()
    st.stop()

# First time seeing this user: try to load their saved state from MongoDB
if not st.session_state.get("db_loaded"):
    oid = st.session_state.get("azure_oid", "")
    doc = load_user_from_db(oid) if oid else None
    if doc:
        restore_from_db(doc)
        st.session_state["db_loaded"]   = True
        st.session_state["wizard_done"] = True
    else:
        st.session_state["db_loaded"]   = True
        st.session_state["wizard_done"] = False
        st.session_state.setdefault("user_role", list(ROLE_KEY_MAP.keys())[0])
        st.session_state.setdefault("curriculum", [
            {**t, "Status": False}
            for t in get_checklist_data(st.session_state["user_role"])
        ])
        init_navigator_status()

# New users see the profile wizard
if not st.session_state.get("wizard_done"):
    show_wizard()
    st.stop()


# =============================================================================
# SIDEBAR
# =============================================================================

role_key     = get_role_key(st.session_state["user_role"])
user_name    = st.session_state.get("user_name", "New Hire")
buddy_name   = st.session_state.get("buddy_name", "Your Buddy")
manager_name = st.session_state.get("manager_name", "Your Manager")
azure_email  = st.session_state.get("azure_email", "")
db_ok        = get_collection() is not None
db_pill      = (
    '<span style="background:rgba(16,185,129,0.15);color:#10b981;'
    'border:1px solid rgba(16,185,129,0.3);border-radius:999px;'
    'padding:1px 8px;font-size:0.7rem;font-weight:700;">🗄️ Synced</span>'
    if db_ok else
    '<span style="background:rgba(239,68,68,0.1);color:#ef4444;'
    'border:1px solid rgba(239,68,68,0.2);border-radius:999px;'
    'padding:1px 8px;font-size:0.7rem;font-weight:700;">⚠️ Local</span>'
)

with st.sidebar:
    st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;
                    margin-bottom:20px;margin-top:-10px;">
            <div style="background:linear-gradient(135deg,#4f46e5,#0ea5e9);
                        padding:10px;border-radius:12px;color:white;
                        font-size:22px;line-height:1;">⚙️</div>
            <h1 style="margin:0;font-size:26px;font-weight:800;
                       letter-spacing:-0.5px;">SPAE Hub</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background:rgba(79,70,229,0.08);border-radius:0.75rem;
                    padding:12px 14px;margin-bottom:16px;
                    border:1px solid rgba(79,70,229,0.15);">
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="font-weight:700;font-size:1rem;">👋 {user_name}</div>
                {db_pill}
            </div>
            <div style="font-size:0.78rem;opacity:0.6;margin-top:3px;">{azure_email}</div>
            <div style="font-size:0.78rem;opacity:0.6;margin-top:6px;">
                {st.session_state['user_role'].split('(')[0].strip()}
            </div>
            <div style="font-size:0.78rem;opacity:0.6;margin-top:4px;">
                🤝 Buddy: <b>{buddy_name}</b>
            </div>
            <div style="font-size:0.78rem;opacity:0.6;margin-top:2px;">
                👔 Manager: <b>{manager_name}</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

    days = days_since_start()
    st.markdown(f"""
        <div style="text-align:center;padding:8px;
                    background:rgba(16,185,129,0.08);border-radius:0.5rem;
                    margin-bottom:12px;border:1px solid rgba(16,185,129,0.2);">
            <div class="days-counter">{days}</div>
            <div style="font-size:0.8rem;opacity:0.7;font-weight:600;">
                day{"s" if days != 1 else ""} on the team
            </div>
        </div>
    """, unsafe_allow_html=True)

    selected_role = st.selectbox(
        "Switch Role",
        list(ROLE_KEY_MAP.keys()),
        index=list(ROLE_KEY_MAP.keys()).index(st.session_state["user_role"]),
    )
    if selected_role != st.session_state["user_role"]:
        st.session_state["user_role"] = selected_role
        reset_user()
        sync_to_db()
        st.rerun()

    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Requests & Learning", "Checklist",
         "Achievements", "Mentor Guide", "Good to Know"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    with st.popover("🆘 Directory & Help", use_container_width=True):
        st.markdown("**Support Contacts**")
        for dept, contact in KEY_CONTACTS.items():
            st.info(f"**{dept}:** `{contact}`")

    with st.popover("🧠 Acronym Buster", use_container_width=True):
        q = st.text_input("Search...", placeholder="e.g. KOLA").strip().lower()
        if q:
            hits = {k: v for k, v in ACRONYMS.items() if q in k.lower() or q in v.lower()}
            if hits:
                for k, v in hits.items():
                    st.success(f"**{k}**: {v}")
            else:
                st.error("No matches found.")

    st.markdown("---")
    st.caption("Quick Links")

    # Common links — shown to everyone
    for link_name, url in QUICK_LINKS.get("Common", {}).items():
        st.markdown(f"🔗 [{link_name}]({url})")

    # Role-specific links — only shown to the active role
    role_links = QUICK_LINKS.get(role_key, {})
    if role_links:
        st.caption(f"{role_key} Links")
        for link_name, url in role_links.items():
            st.markdown(f"🔗 [{link_name}]({url})")

    st.markdown("---")
    if st.button("🚪 Sign Out", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# =============================================================================
# PAGES
# =============================================================================

role_key = get_role_key(st.session_state["user_role"])

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
if page == "Dashboard":
    xp, max_xp, level_name           = get_xp_and_level()
    earned_badges                     = get_earned_badges()
    checklist_p, nav_p, overall_p     = get_overall_progress()
    nd, nt                            = get_navigator_progress()
    df                                = pd.DataFrame(st.session_state["curriculum"])

    st.markdown(f"""
        <div class="hero-card">
            <span class="pill">{level_name} · {xp} / {max_xp} XP</span>
            <h1>Welcome, {user_name} 👋</h1>
            <p class="muted">Your personalised command centre for mastering the
            <strong>{role_key}</strong> role.
            You're on day <strong>{days_since_start()}</strong> of your journey — keep going!</p>
        </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4, chart_col = st.columns([1, 1, 1, 1, 1.2])
    with k1:
        with st.container(border=True): st.metric("Overall",   f"{int(overall_p * 100)}%")
    with k2:
        with st.container(border=True): st.metric("Checklist", f"{int(checklist_p * 100)}%")
    with k3:
        with st.container(border=True): st.metric("Training",  f"{nd}/{nt}")
    with k4:
        with st.container(border=True): st.metric("Badges",    f"{len(earned_badges)}/{len(ALL_BADGES)}")
    with chart_col:
        st.altair_chart(create_donut_chart(overall_p), use_container_width=True)

    if overall_p >= 1.0:
        st.balloons()
        st.success("🎉 You're a SPAE Champion! Download your certificate from Achievements.")

    col_action, col_badges = st.columns([3, 2])
    with col_action:
        st.markdown("### 🎯 Action Centre")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("Next Tasks")
                pending = df[df["Status"] == False].sort_values("Phase").head(4)
                if not pending.empty:
                    st.dataframe(pending[["Phase", "Task"]], hide_index=True, use_container_width=True)
                else:
                    st.success("All tasks complete! ✅")
        with c2:
            with st.container(border=True):
                st.subheader("Next Training")
                status    = st.session_state["navigator_status"]
                nav_focus = [
                    {"Type": s, "Course": c}
                    for s, c in (
                        [("Mandatory", c) for c in NAVIGATOR_COURSES["Mandatory"]]
                        + [(role_key, c) for c in NAVIGATOR_COURSES.get(role_key, [])]
                    )
                    if not status.get(navigator_course_key(s, c), False)
                ][:4]
                if nav_focus:
                    st.dataframe(pd.DataFrame(nav_focus), hide_index=True, use_container_width=True)
                else:
                    st.success("All training complete! ✅")

    with col_badges:
        st.markdown("### 🏅 Badges")
        bcols = st.columns(3)
        for i, badge in enumerate(ALL_BADGES[:6]):
            unlocked = badge["id"] in earned_badges
            with bcols[i % 3]:
                st.markdown(f"""
                    <div class="badge-card {'badge-locked' if not unlocked else ''}"
                         title="{badge['desc']}">
                        <div class="badge-icon">{badge['icon']}</div>
                        <div class="badge-name">{badge['name']}</div>
                    </div>
                """, unsafe_allow_html=True)

# ── REQUESTS & LEARNING ───────────────────────────────────────────────────────
elif page == "Requests & Learning":
    st.markdown("## 📚 Requests & Learning")
    tab1, tab2, tab3 = st.tabs(["🔐 FAROS Access", "🎓 Navigator Hub", "🧰 Toolkit"])

    with tab1:
        st.info("💡 Use the **FAROS Portal** link in the sidebar. Attach your manager's approval email.")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🏢 Core Systems (All Roles)")
                for item in FAROS_CATALOG["Common"]:
                    st.markdown(f"✅ {item}")
        with c2:
            with st.container(border=True):
                st.subheader(f"🛠 {role_key}-Specific Systems")
                ic, tc = st.columns([1.2, 3])
                with ic:
                    st.image(THEME_IMAGES[role_key], use_container_width=True)
                with tc:
                    for item in FAROS_CATALOG.get(role_key, []):
                        st.markdown(f"🔹 **{item}**")

    with tab2:
        nd, nt = get_navigator_progress()
        st.progress(nd / nt if nt > 0 else 0, text=f"Course Completion: {nd}/{nt}")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🚨 Mandatory Training (50 XP ea)")
                for course in NAVIGATOR_COURSES["Mandatory"]:
                    key = navigator_course_key("Mandatory", course)
                    st.checkbox(
                        course,
                        value=st.session_state["navigator_status"].get(key, False),
                        key=f"nav_{key}",
                        on_change=nav_click_callback,
                        args=("Mandatory", course),
                    )
        with c2:
            with st.container(border=True):
                st.subheader(f"🧠 {role_key} Specific (50 XP ea)")
                for course in NAVIGATOR_COURSES.get(role_key, []):
                    key = navigator_course_key(role_key, course)
                    st.checkbox(
                        course,
                        value=st.session_state["navigator_status"].get(key, False),
                        key=f"nav_{key}",
                        on_change=nav_click_callback,
                        args=(role_key, course),
                    )

    with tab3:
        with st.container(border=True):
            st.subheader("🔗 Essential Tools")
            for item in TOOLKIT.get("Common", []) + TOOLKIT.get(role_key, []):
                st.markdown(f"- {item}")

# ── CHECKLIST ─────────────────────────────────────────────────────────────────
elif page == "Checklist":
    st.markdown("## ✅ Master Checklist")
    st.caption(
        f"Personalised for **{user_name}** · "
        f"Buddy: **{buddy_name}** · Manager: **{manager_name}**"
    )
    df = pd.DataFrame(st.session_state["curriculum"])
    df["idx"] = df.index
    search_q  = st.text_input("🔍 Filter tasks...", "").lower()

    for phase in ["Day 1", "Week 1", "Month 1", "Month 2", "Month 3"]:
        pt = df[df["Phase"] == phase]
        if pt.empty:
            continue
        if search_q:
            pt = pt[
                pt["Task"].str.lower().str.contains(search_q)
                | pt["Category"].str.lower().str.contains(search_q)
            ]
            if pt.empty:
                continue
        done, total = int(pt["Status"].sum()), len(pt)
        with st.container(border=True):
            st.markdown(f"### 🗓 {phase} — {done}/{total} complete")
            st.progress(done / total)
            for _, row in pt.iterrows():
                idx = int(row["idx"])
                mentor_display = (
                    row["Mentor"]
                    .replace("Buddy",   buddy_name)
                    .replace("Manager", manager_name)
                )
                st.markdown('<div class="checklist-row">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1, 14, 4])
                with c1:
                    st.checkbox(
                        "Done", value=row["Status"], key=f"chk_{idx}",
                        on_change=toggle_status, args=(idx,),
                        label_visibility="collapsed",
                    )
                with c2:
                    st.markdown(
                        f"~~**{row['Task']}**~~" if row["Status"] else f"**{row['Task']}**"
                    )
                    if row.get("Tip"):
                        st.markdown(
                            f"<div class='tip-box'>💡 {row['Tip']}</div>",
                            unsafe_allow_html=True,
                        )
                    st.caption(f"Category: {row['Category']}")
                with c3:
                    st.markdown(
                        f"<div style='text-align:right;margin-top:5px;'>"
                        f"<span class='mentor-badge'>👤 {mentor_display}</span></div>",
                        unsafe_allow_html=True,
                    )
                st.markdown("</div>", unsafe_allow_html=True)

# ── KNOWLEDGE QUIZ ────────────────────────────────────────────────────────────
# ── ACHIEVEMENTS ──────────────────────────────────────────────────────────────
elif page == "Achievements":
    st.markdown("## 🏅 Achievements")
    earned_badges           = get_earned_badges()
    xp, max_xp, level_name = get_xp_and_level()
    _, _, overall_p         = get_overall_progress()

    cA, cB = st.columns([2, 1])
    with cA:
        st.markdown(f"### {level_name}")
        st.progress(
            xp / max_xp if max_xp > 0 else 0,
            text=f"{xp} / {max_xp} XP — {len(earned_badges)}/{len(ALL_BADGES)} badges",
        )
    with cB:
        with st.container(border=True):
            st.metric("Days on Team", days_since_start())

    st.markdown("### Your Badges")
    cols = st.columns(4)
    for i, badge in enumerate(ALL_BADGES):
        unlocked   = badge["id"] in earned_badges
        status_txt = "✅ Unlocked" if unlocked else f"🔒 {badge['desc']}"
        with cols[i % 4]:
            st.markdown(f"""
                <div class="badge-card {'badge-locked' if not unlocked else ''}">
                    <div class="badge-icon">{badge['icon']}</div>
                    <div class="badge-name">{badge['name']}</div>
                    <div class="badge-desc">{status_txt}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎓 Completion Certificate")
    if overall_p >= 1.0:
        st.success("🏆 You've completed everything! Your certificate is ready.")
        st.download_button(
            label="⬇️ Download Certificate (HTML)",
            data=generate_certificate_html(),
            file_name=f"SPAE_Certificate_{user_name.replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True,
        )
        st.components.v1.html(generate_certificate_html(), height=520, scrolling=False)
    else:
        st.info(
            f"🔒 Complete 100% of your onboarding to unlock your certificate. "
            f"{int((1 - overall_p) * 100)}% remaining."
        )

# ── MENTOR GUIDE ──────────────────────────────────────────────────────────────
elif page == "Mentor Guide":
    st.markdown("## 📘 Mentor's Playbook")
    st.warning("🔒 **Restricted:** Intended for Mentors & Managers.")
    tab_tips, tab_faq = st.tabs(["💡 Best Practices", "❓ New Hire FAQs"])

    with tab_tips:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("Week-by-Week Mentor Agenda")
                st.markdown("""
**Day 1:** Meet at reception. Walk them through the office. Sit with them during IT setup. Have lunch together.

**Week 1:** Daily 15-min check-in. Introduce to at least 5 colleagues. Shadow one real task together.

**Month 1:** Weekly 1:1s (30 mins). Review checklist together. Flag system access blockers proactively.

**Month 2:** Fortnightly 1:1s. Structured feedback on first independent tasks. Discuss career goals.

**Month 3:** 90-day review prep. Encourage them to mentor someone newer. Celebrate the milestone.
                """)
        with c2:
            with st.container(border=True):
                st.subheader("👀 Red Flags to Watch For")
                st.markdown("""
- Signs of overload (missed stand-ups, short responses) in Week 1
- System access blockers still unresolved beyond Day 5 — escalate to IT
- Misunderstanding of safety protocols — stop and re-train immediately
- Not asking questions — often means confusion, not confidence
- Late ESRs or timesheets — address the habit early
                """)

    with tab_faq:
        all_faqs = FAQS.get("Common", []) + FAQS.get(role_key, [])
        for faq in all_faqs:
            with st.expander(f"❓ {faq['q']}"):
                st.markdown(faq["a"])

# ── GOOD TO KNOW ──────────────────────────────────────────────────────────────
elif page == "Good to Know":
    tab_arch, tab_gloss, tab_faq = st.tabs(
        ["🗺 System Architecture", "📖 Role Glossary", "❓ FAQ"]
    )

    with tab_arch:
        st.markdown("## 🧩 System Architecture")
        st.markdown("Understanding how data flows between tools is key to mastering your workflow.")
        with st.container(border=True):
            if HAS_GRAPHVIZ:
                st.markdown(f"**Data Flow: {st.session_state['user_role']}**")
                st.graphviz_chart(get_tech_stack_graph(role_key))
            else:
                st.error("Install graphviz: `pip install graphviz`")

    with tab_gloss:
        st.markdown("## 📖 Role Glossary")
        sq = st.text_input("🔍 Search terms...", "").lower()
        for term, defn in GLOSSARY.get(role_key, {}).items():
            if sq and sq not in term.lower() and sq not in defn.lower():
                continue
            with st.expander(f"**{term}**"):
                st.markdown(defn)

    with tab_faq:
        st.markdown("## ❓ Frequently Asked Questions")
        fq = st.text_input("🔍 Search FAQs...", "").lower()
        for faq in FAQS.get("Common", []) + FAQS.get(role_key, []):
            if fq and fq not in faq["q"].lower() and fq not in faq["a"].lower():
                continue
            with st.expander(f"❓ {faq['q']}"):
                st.markdown(faq["a"])
