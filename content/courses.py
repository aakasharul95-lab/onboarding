"""
courses.py — Navigator Training Courses
=========================================
Add or remove courses here. Changes are picked up automatically by the app.

Structure:
  NAVIGATOR_COURSES["Mandatory"]  → shown to ALL roles (compliance courses)
  NAVIGATOR_COURSES["SPE"]        → shown only to Spare Parts Engineers
  NAVIGATOR_COURSES["SE"]         → shown only to Service Engineers

Each entry is a plain string: "Course Title (duration)"
Duration is shown in the UI but not enforced — it's informational only.

ROLE_KEY_MAP maps the full dropdown label → short role key used throughout the app.
Add a new role here and in tasks.py / systems.py to support it.
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# Role label → short key mapping
# Add new roles here if the company expands
# ---------------------------------------------------------------------------
ROLE_KEY_MAP: Dict[str, str] = {
    "SPE (Spare Parts Engineer)": "SPE",
    "SE (Service Engineer)":      "SE",
}

# ---------------------------------------------------------------------------
# Navigator courses
# ---------------------------------------------------------------------------
NAVIGATOR_COURSES: Dict[str, List[str]] = {

    # Mandatory for everyone — compliance & company-wide training
    "Mandatory": [
        "Global Data Privacy & GDPR (30 mins)",
        "Cybersecurity Awareness: Phishing (15 mins)",
        "Code of Conduct: Anti-Bribery (45 mins)",
        "Diversity & Inclusion Basics (20 mins)",
        "Health & Safety: Office Ergonomics (15 mins)",
    ],

    # SPE-specific courses
    "SPE": [
        "SAP ERP: Supply Chain Basics (60 mins)",
        "Logistics 101: Incoterms (30 mins)",
        "Agile PLM: Document Control (45 mins)",
    ],

    # SE-specific courses
    "SE": [
        "Field Safety: Electrical Hazards (60 mins)",
        "Defensive Driving Certification (External)",
        "Customer Service: Handling Conflict (30 mins)",
    ],

}