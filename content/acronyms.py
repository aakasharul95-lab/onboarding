"""
acronyms.py — Internal Acronym Dictionary
==========================================
Add any internal jargon, system abbreviations, or company-specific terms here.
These appear in the "Acronym Buster" search popover in the sidebar.

Format:  "ACRONYM": "Full meaning or explanation"

TIPS:
  - Use ALL CAPS for the key (makes searching case-insensitive easier)
  - Include a brief explanation in the value, not just the expansion
  - Add both IT system names and process/role acronyms
"""

from typing import Dict

ACRONYMS: Dict[str, str] = {

    # ── Roles ─────────────────────────────────────────────────────────────────
    "SPE":   "Spare Parts Engineer — manages parts ordering, inventory, and logistics",
    "SE":    "Service Engineer — field technician responsible for on-site maintenance and repair",

    # ── Systems ───────────────────────────────────────────────────────────────
    "SAP":   "Systems, Applications, and Products — the company's core ERP platform",
    "KOLA":  "Key On-Line Access — the parts documentation and part number database",
    "GLOPPS":"Global Logistics & Parts System — used to check global stock and logistics",
    "RUMBA": "Legacy parts lookup system — use as a fallback when GLOPPS shows 0 stock",
    "MOM":   "Mobile Order Management — the field app used by SEs for timesheets and work orders",
    "PLM":   "Product Lifecycle Management — manages product data from design to end-of-life (Agile PLM)",
    "CRM":   "Customer Relationship Management — Salesforce is the company CRM",
    "ESR":   "Electronic Service Report — the digital job record SEs must file same day",
    "HSV":   "Hydraulic Schematics Viewer — used by SEs to view machine hydraulic diagrams",
    "VPN":   "Virtual Private Network — required for remote access to company systems (Cisco AnyConnect)",
    "ERP":   "Enterprise Resource Planning — the integrated system managing finance, HR, and supply chain (SAP)",

    # ── Processes & Terms ─────────────────────────────────────────────────────
    "LOTO":  "Lock Out Tag Out — mandatory safety isolation procedure before working on energised equipment",
    "BOM":   "Bill of Materials — structured list of all components needed to build or service a product",
    "PO":    "Purchase Order — a formal document authorising the purchase of goods from a supplier",
    "PPE":   "Personal Protective Equipment — mandatory safety gear (boots, hi-vis, hard hat, gloves)",
    "SOP":   "Standard Operating Procedure — a documented step-by-step process for a routine task",
    "SLA":   "Service Level Agreement — contracted response/fix time promised to a customer",
    "MOQ":   "Minimum Order Quantity — the smallest number of units a supplier will sell in one order",
    "GRN":   "Goods Receipt Note — confirms that ordered parts have arrived and been checked in",
    "MRP":   "Material Requirements Planning — SAP process for automatic stock replenishment calculation",
    "RAMS":  "Risk Assessment and Method Statement — required before starting any non-routine field task",

    # ── HR & Company ──────────────────────────────────────────────────────────
    "HR":    "Human Resources — Workday is the self-service HR portal",
    "L&D":   "Learning & Development — Navigator is the L&D training platform",
    "GDPR":  "General Data Protection Regulation — EU data privacy law; mandatory training in Navigator",
    "MFA":   "Multi-Factor Authentication — required for all company system logins (Microsoft Authenticator)",
    "SSO":   "Single Sign-On — log in once with your Microsoft account to access all connected systems",
    "OID":   "Object ID — your unique identifier in Azure Active Directory (used by IT for access requests)",
    "UPN":   "User Principal Name — your work email address as recognised by Azure AD (e.g. you@company.com)",
    "FAROS": "Internal system access request portal — submit all new system access requests here",

}
