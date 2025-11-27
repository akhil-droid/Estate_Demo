"""
UK Estate Agency AI - Multi-Agent System
=========================================
Backend package initialization
"""

from .agents import (
    BaseAgent,
    OrchestratorAgent,
    ScoutAgent,
    IntelligenceAgent,
    ContentAgent,
    ComplianceAgent,
    AgentManager,
    HumanApproval
)

from .data_loader import DataLoader

__all__ = [
    "BaseAgent",
    "OrchestratorAgent",
    "ScoutAgent",
    "IntelligenceAgent",
    "ContentAgent",
    "ComplianceAgent",
    "AgentManager",
    "HumanApproval",
    "DataLoader"
]

__version__ = "1.0.0"