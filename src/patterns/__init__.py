"""Agent collaboration patterns package."""

from .supervisor_pattern import SupervisorAgent, WorkerAgent
from .debate_pattern import DebateOrchestrator
from .consensus_pattern import ConsensusEngine
from .pipeline_pattern import PipelineOrchestrator
from .swarm_pattern import SwarmIntelligence

__all__ = [
    'SupervisorAgent',
    'WorkerAgent',
    'DebateOrchestrator',
    'ConsensusEngine',
    'PipelineOrchestrator',
    'SwarmIntelligence'
]
