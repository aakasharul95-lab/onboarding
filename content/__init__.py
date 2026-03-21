"""
SPAE Onboarding Hub — Content Package
======================================
All editable content lives here. The main app (spae_onboarding_hub.py)
imports from this package and never needs to be touched when content changes.

To update any content, edit the relevant file:
  - tasks.py       → checklist tasks (Day 1 → Month 3)
  - courses.py     → Navigator training courses
  - systems.py     → FAROS access lists & toolkit links
  - glossary.py    → role-specific glossary terms
  - faqs.py        → frequently asked questions
  - badges.py      → badge definitions & unlock conditions
  - acronyms.py    → internal acronym dictionary
"""

from content.tasks     import get_checklist_data
from content.courses   import NAVIGATOR_COURSES
from content.systems   import FAROS_CATALOG, TOOLKIT, QUICK_LINKS, IMPORTANT_LINKS, THEME_IMAGES
from content.glossary  import GLOSSARY
from content.faqs      import FAQS
from content.badges    import ALL_BADGES
from content.acronyms  import ACRONYMS

__all__ = [
    "get_checklist_data",
    "NAVIGATOR_COURSES",
    "FAROS_CATALOG",
    "TOOLKIT",
    "QUICK_LINKS",
    "IMPORTANT_LINKS",
    "THEME_IMAGES",
    "GLOSSARY",
    "FAQS",
    "ALL_BADGES",
    "ACRONYMS",
]