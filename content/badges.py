"""
badges.py — Achievement Badges
================================
Define badges here. Each badge has a unique id that the app uses internally
to track which badges have been earned.

Fields:
  id   : unique snake_case identifier — do NOT change once deployed (breaks saved state)
  name : display name shown in the UI
  icon : emoji shown on the badge card
  desc : short description of how to unlock it (shown when locked)

Badge unlock logic lives in the main app (get_earned_badges) to keep it
close to session state. If you add a new badge here, also add its
unlock condition in spae_onboarding_hub.py → get_earned_badges().
"""

from typing import Dict, List

ALL_BADGES: List[Dict] = [
    {
        "id":   "first_step",
        "name": "First Step",
        "icon": "👟",
        "desc": "Complete your very first checklist task",
    },
    {
        "id":   "week1_done",
        "name": "Week 1 Warrior",
        "icon": "⚔️",
        "desc": "Complete all Day 1 & Week 1 tasks",
    },
    {
        "id":   "half_way",
        "name": "Halfway There",
        "icon": "🌗",
        "desc": "Reach 50% overall onboarding progress",
    },
    {
        "id":   "learning_done",
        "name": "Scholar",
        "icon": "🎓",
        "desc": "Complete all Navigator training modules",
    },
    {
        "id":   "champion",
        "name": "SPAE Champion",
        "icon": "🏆",
        "desc": "Reach 100% overall onboarding completion",
    },
    {
        "id":   "speed_runner",
        "name": "Speed Runner",
        "icon": "⚡",
        "desc": "Complete 5 tasks in a single session",
    },
]