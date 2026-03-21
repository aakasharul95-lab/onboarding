"""
systems.py — FAROS System Access, Toolkit & Links
===================================================
Edit this file to add/remove systems, tools, or quick links.

FAROS_CATALOG : systems that need to be requested via FAROS portal
TOOLKIT       : internal tools (no access request needed)
QUICK_LINKS   : sidebar quick links — shared + role-specific
                "Common" links appear for everyone
                "SPE" links appear only for Spare Parts Engineers
                "SE"  links appear only for Service Engineers
THEME_IMAGES  : hero images per role (replace URLs to change)
KEY_CONTACTS  : support contacts shown in the Directory popover
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# FAROS System Access Catalog
# "Common" = shown to all roles
# "SPE" / "SE" = role-specific systems
# ---------------------------------------------------------------------------
FAROS_CATALOG: Dict[str, List[str]] = {

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
    ],

    "SPE": [
        "SAP GUI: ERP System (Production)",
        "GLOPPS (Global Logistics & Parts)",
        "KOLA (Parts Documentation DB)",
        "RUMBA (Legacy Parts Lookup)",
        "Autodesk Vault (CAD Data Management)",
        "Creo MCAD (View & Edit License)",
        "Agile PLM: Product Lifecycle Mgmt",
        "PowerBI Desktop (Inventory Analytics)",
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
    ],

}

# ---------------------------------------------------------------------------
# Toolkit — internal tools (no FAROS request required)
# ---------------------------------------------------------------------------
TOOLKIT: Dict[str, List[str]] = {

    "Common": [
        "Tidinfo – Technical information portal",
        "SCORE – Service & Customer Operations Reporting Engine",
    ],

    "SPE": [
        "Parts Costing Calculator",
        "BOM Comparison Utility",
    ],

    "SE": [
        "Service Checklists Mobile Pack",
        "Field Report Template Pack",
    ],

}

# ---------------------------------------------------------------------------
# Quick Links shown in the sidebar
#
# "Common" links appear for ALL roles
# "SPE"    links appear only for Spare Parts Engineers
# "SE"     links appear only for Service Engineers
#
# Format for each entry:
#   "Display Name": "https://full-url-here"
#
# The sidebar shows Common links first, then the role-specific ones below.
# ---------------------------------------------------------------------------
QUICK_LINKS: Dict[str, Dict[str, str]] = {

    "Common": {
        "FAROS (Access Portal)": "https://faros.internal.example.com",
        "Navigator (Learning)":  "https://navigator.internal.example.com",
        "Workday (HR)":          "https://www.myworkday.com",
        "Concur (Expenses)":     "https://www.concursolutions.com",
        "ServiceNow (IT Help)":  "https://servicenow.internal.example.com",
    },

    "SPE": {
        "SAP GUI (Production)":  "https://sap.internal.example.com",
        "KOLA (Parts DB)":       "https://kola.internal.example.com",
        "GLOPPS (Logistics)":    "https://glopps.internal.example.com",
        "Agile PLM":             "https://plm.internal.example.com",
        "PowerBI (Inventory)":   "https://powerbi.internal.example.com",
        "SharePoint: SPE Hub":   "https://sharepoint.internal.example.com/spe",
    },

    "SE": {
        "SAP Service Cloud":     "https://c4c.internal.example.com",
        "MOM App (Mobile)":      "https://mom.internal.example.com",
        "LOTO Safety Portal":    "https://loto.internal.example.com",
        "ESR Tool":              "https://esr.internal.example.com",
        "Salesforce (CRM)":      "https://salesforce.internal.example.com",
        "SharePoint: SE Hub":    "https://sharepoint.internal.example.com/se",
    },

}

# ---------------------------------------------------------------------------
# Keep IMPORTANT_LINKS as an alias for backward compatibility
# (points to Common links — do not edit this line, edit QUICK_LINKS above)
# ---------------------------------------------------------------------------
IMPORTANT_LINKS = QUICK_LINKS["Common"]

# ---------------------------------------------------------------------------
# Hero images shown on the FAROS Access tab per role
# Replace the URL with any Unsplash or company-hosted image
# ---------------------------------------------------------------------------
THEME_IMAGES: Dict[str, str] = {
    "SPE": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=600&q=80",
    "SE":  "https://images.unsplash.com/photo-1581092335397-9583eb92d232?auto=format&fit=crop&w=600&q=80",
}

# ---------------------------------------------------------------------------
# Key contacts shown in the Directory & Help popover
# ---------------------------------------------------------------------------
KEY_CONTACTS: Dict[str, str] = {
    "IT Helpdesk":   "Ext. 4040",
    "HR Onboarding": "Ext. 2000",
    "Safety Officer": "Ext. 9110",
}