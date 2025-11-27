"""
Configuration for UK Estate Agency AI System
"""

import os

# ============================================================================
# API KEYS
# ============================================================================

# OpenAI API Key - REPLACE WITH YOUR KEY
OPENAI_API_KEY = "sk-your-api-key-here"

# OpenAI Model
OPENAI_MODEL = "gpt-4o-mini"  # or "gpt-4o" for better quality

# ============================================================================
# DATA DIRECTORY
# ============================================================================

# Data directory containing Stage_1 and Stage_2 folders
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Expected folder structure:
# data/
#   Stage_1/
#     leads.csv
#     buyers.csv
#     vendors.csv
#     properties.csv
#     enquiries.csv
#     viewings.csv
#     offers.csv
#     communications.csv
#     marketing_campaigns.csv
#     financial_qualifications.csv
#     buyer_requirements.csv
#     workflow_paths.csv
#     sub_tasks.csv
#     agent_executions.csv
#   Stage_2/
#     stage2_valuations.csv
#     stage2_property_research.csv
#     stage2_cma_reports.csv
#     stage2_marketing_proposals.csv
#     stage2_valuation_visits.csv
#     stage2_instructions.csv
#     stage2_workflow_paths.csv
#     stage2_sub_tasks.csv
#     stage2_agent_executions.csv
#     stage2_communications.csv

# ============================================================================
# SERVER CONFIGURATION
# ============================================================================

HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# ============================================================================
# AI AGENTS CONFIGURATION
# ============================================================================

AGENT_CONFIG = {
    "orchestrator": {
        "name": "Orchestrator",
        "icon": "🎯",
        "color": "#667eea",
        "description": "Plans and coordinates workflow execution"
    },
    "scout": {
        "name": "Scout",
        "icon": "🔍",
        "color": "#3b82f6",
        "description": "Searches databases and retrieves information"
    },
    "intelligence": {
        "name": "Intelligence",
        "icon": "🧠",
        "color": "#8b5cf6",
        "description": "Analyzes data and provides insights"
    },
    "content": {
        "name": "Content",
        "icon": "✍️",
        "color": "#ec4899",
        "description": "Generates descriptions, emails, and reports"
    },
    "comms": {
        "name": "Comms",
        "icon": "📧",
        "color": "#14b8a6",
        "description": "Handles communications and notifications"
    },
    "compliance": {
        "name": "Compliance",
        "icon": "✅",
        "color": "#10b981",
        "description": "Verifies regulatory compliance and documents"
    },
    "valuator": {
        "name": "Valuator",
        "icon": "📊",
        "color": "#f59e0b",
        "description": "Performs property valuations and CMA"
    }
}

# ============================================================================
# STAGES CONFIGURATION
# ============================================================================

STAGES = {
    1: {
        "name": "Lead Generation & Customer Acquisition",
        "enabled": True,
        "folder": "Stage_1",
        "sub_stages": ["1.1", "1.2", "1.3"],
        "sub_tasks_count": 10
    },
    2: {
        "name": "Valuation Appointment",
        "enabled": True,
        "folder": "Stage_2",
        "sub_stages": ["2.1", "2.2", "2.3"],
        "sub_tasks_count": 12
    },
    3: {
        "name": "Instruction & Onboarding",
        "enabled": False,
        "folder": "Stage_3",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    4: {
        "name": "Property Marketing Preparation",
        "enabled": False,
        "folder": "Stage_4",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    5: {
        "name": "Marketing Launch & Syndication",
        "enabled": False,
        "folder": "Stage_5",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    6: {
        "name": "Enquiry Management",
        "enabled": False,
        "folder": "Stage_6",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    7: {
        "name": "Vendor Reporting & Communication",
        "enabled": False,
        "folder": "Stage_7",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    8: {
        "name": "Offer Negotiation",
        "enabled": False,
        "folder": "Stage_8",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    9: {
        "name": "SSTC Management",
        "enabled": False,
        "folder": "Stage_9",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    10: {
        "name": "Sales Progression",
        "enabled": False,
        "folder": "Stage_10",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    11: {
        "name": "Exchange & Completion",
        "enabled": False,
        "folder": "Stage_11",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    12: {
        "name": "Post-Completion",
        "enabled": False,
        "folder": "Stage_12",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    13: {
        "name": "Fall-Through Management",
        "enabled": False,
        "folder": "Stage_13",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    14: {
        "name": "Financial Administration",
        "enabled": False,
        "folder": "Stage_14",
        "sub_stages": [],
        "sub_tasks_count": 0
    },
    15: {
        "name": "Reporting & Analytics",
        "enabled": False,
        "folder": "Stage_15",
        "sub_stages": [],
        "sub_tasks_count": 0
    }
}

# ============================================================================
# CHECKPOINT CONFIGURATION
# ============================================================================

# Sub-tasks that require human confirmation before proceeding
CHECKPOINT_SUBTASKS = {
    "1.3.2": "Financial qualification complete. Proceed with this lead?",
    "2.1.3": "Pre-valuation preparation complete. Ready to proceed to appointment?",
    "2.2.7": "Has the vendor signed the instruction?"
}