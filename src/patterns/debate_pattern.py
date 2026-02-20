"""
Debate pattern for structured multi-agent argumentation.

Implements N-round debate with proposer and critic agents.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DebatePosition(Enum):
    """Debate position in an argument."""
    PROPOSER = "proposer"
    CRITIC = "critic"


@dataclass
class Argument:
    """Represents a debate argument."""
    
    position: DebatePosition
    content: str
    confidence_score: float
    supporting_evidence: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DebateRound:
    """Represents a single debate round."""
    
    round_number: int
    proposer_argument: Optional[Argument] = None
    critic_argument: Optional[Argument] = None
    consensus_score: float = 0.0


class DebateOrchestrator:
    """
    Orchestrates multi-round debates between agents.
    
    Manages argumentation, scoring, and consensus detection.
    """
    
    def __init__(
        self,
        num_rounds: int = 3,
        scoring_strategy: str = "entropy_reduction"
    ):
        """
        Initialize debate orchestrator.
        
        Args:
            num_rounds: Number of debate rounds
            scoring_strategy: How to score arguments
        """
        self.num_rounds = num_rounds
        self.scoring_strategy = scoring_strategy
        self.rounds: List[DebateRound] = []
    
    def run_debate(
        self,
        topic: str,
        proposer_position: str,
        initial_arguments: Optional[Dict[str, str]] = None
    ) -> Dict[str, any]:
        """
        Run a multi-round debate.
        
        Args:
            topic: Debate topic
            proposer_position: Initial proposer stance
            initial_arguments: Initial arguments from each side
            
        Returns:
            Debate results with consensus
        """
        self.rounds = []
        
        for round_num in range(1, self.num_rounds + 1):
            debate_round = DebateRound(round_number=round_num)
            
            # Proposer argument
            proposer_arg = Argument(
                position=DebatePosition.PROPOSER,
                content=f"Round {round_num}: {proposer_position}",
                confidence_score=0.8 + (round_num * 0.05)
            )
            
            # Critic argument
            critic_arg = Argument(
                position=DebatePosition.CRITIC,
                content=f"Round {round_num}: Counter-argument",
                confidence_score=0.7 + (round_num * 0.04)
            )
            
            debate_round.proposer_argument = proposer_arg
            debate_round.critic_argument = critic_arg
            debate_round.consensus_score = self._calculate_consensus(
                proposer_arg,
                critic_arg
            )
            
            self.rounds.append(debate_round)
        
        return self._generate_consensus()
    
    def _calculate_consensus(
        self,
        proposer_arg: Argument,
        critic_arg: Argument
    ) -> float:
        """Calculate consensus score between arguments."""
        if self.scoring_strategy == "entropy_reduction":
            # Higher confidence convergence = higher consensus
            return min(
                proposer_arg.confidence_score,
                critic_arg.confidence_score
            )
        elif self.scoring_strategy == "agreement_measure":
            # Measure agreement between positions
            return (proposer_arg.confidence_score +
                    critic_arg.confidence_score) / 2
        
        return 0.5
    
    def _generate_consensus(self) -> Dict[str, any]:
        """Generate debate consensus from all rounds."""
        avg_consensus = (
            sum(r.consensus_score for r in self.rounds) /
            len(self.rounds)
        )
        
        final_round = self.rounds[-1]
        
        return {
            "topic": "Debate topic",
            "total_rounds": len(self.rounds),
            "avg_consensus_score": avg_consensus,
            "proposer_final_confidence": final_round.proposer_argument.confidence_score,
            "critic_final_confidence": final_round.critic_argument.confidence_score,
            "consensus_reached": avg_consensus > 0.75,
            "rounds": [
                {
                    "round": r.round_number,
                    "consensus": r.consensus_score
                }
                for r in self.rounds
            ]
        }
