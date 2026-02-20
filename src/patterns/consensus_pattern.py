"""
Consensus pattern for weighted voting among agents.

Agents vote with confidence scores to reach agreement.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class VotingStrategy(Enum):
    """Available voting strategies."""
    SIMPLE_MAJORITY = "simple_majority"
    WEIGHTED_CONFIDENCE = "weighted_confidence"
    UNANIMOUS = "unanimous"


@dataclass
class Vote:
    """Represents a single agent vote."""
    
    agent_name: str
    option: str
    confidence: float  # 0.0 to 1.0
    reasoning: str = ""


class ConsensusEngine:
    """
    Implements consensus mechanism with weighted voting.
    
    Agents vote based on options and confidence levels.
    """
    
    def __init__(self, strategy: VotingStrategy = VotingStrategy.WEIGHTED_CONFIDENCE):
        """
        Initialize consensus engine.
        
        Args:
            strategy: Voting strategy to use
        """
        self.strategy = strategy
        self.votes: List[Vote] = []
    
    def add_vote(
        self,
        agent_name: str,
        option: str,
        confidence: float,
        reasoning: str = ""
    ) -> None:
        """
        Record a vote from an agent.
        
        Args:
            agent_name: Name of voting agent
            option: The option being voted for
            confidence: Confidence level (0-1)
            reasoning: Reasoning behind the vote
        """
        vote = Vote(
            agent_name=agent_name,
            option=option,
            confidence=max(0.0, min(1.0, confidence)),
            reasoning=reasoning
        )
        self.votes.append(vote)
    
    def calculate_consensus(self) -> Dict[str, Any]:
        """
        Calculate consensus from recorded votes.
        
        Returns:
            Consensus results
        """
        if not self.votes:
            return {"consensus": None, "confidence": 0.0}
        
        if self.strategy == VotingStrategy.WEIGHTED_CONFIDENCE:
            return self._weighted_consensus()
        elif self.strategy == VotingStrategy.SIMPLE_MAJORITY:
            return self._majority_consensus()
        elif self.strategy == VotingStrategy.UNANIMOUS:
            return self._unanimous_consensus()
        
        return {"consensus": None}
    
    def _weighted_consensus(self) -> Dict[str, Any]:
        """Calculate weighted consensus by confidence."""
        option_scores: Dict[str, float] = {}
        option_counts: Dict[str, int] = {}
        
        for vote in self.votes:
            if vote.option not in option_scores:
                option_scores[vote.option] = 0.0
                option_counts[vote.option] = 0
            
            option_scores[vote.option] += vote.confidence
            option_counts[vote.option] += 1
        
        if not option_scores:
            return {"consensus": None}
        
        # Find option with highest weighted score
        best_option = max(option_scores.keys(),
                         key=lambda x: option_scores[x])
        total_confidence = sum(option_scores.values())
        
        return {
            "consensus": best_option,
            "confidence": option_scores[best_option] / total_confidence,
            "vote_breakdown": {
                opt: option_scores[opt] / option_counts[opt]
                for opt in option_scores.keys()
            }
        }
    
    def _majority_consensus(self) -> Dict[str, Any]:
        """Calculate simple majority consensus."""
        option_counts: Dict[str, int] = {}
        
        for vote in self.votes:
            option_counts[vote.option] = option_counts.get(vote.option, 0) + 1
        
        if not option_counts:
            return {"consensus": None}
        
        best_option = max(option_counts.keys(),
                         key=lambda x: option_counts[x])
        
        return {
            "consensus": best_option,
            "votes_for": option_counts[best_option],
            "total_votes": len(self.votes)
        }
    
    def _unanimous_consensus(self) -> Dict[str, Any]:
        """Check for unanimous consensus."""
        if not self.votes:
            return {"consensus": None, "unanimous": False}
        
        first_option = self.votes[0].option
        unanimous = all(v.option == first_option for v in self.votes)
        
        return {
            "consensus": first_option if unanimous else None,
            "unanimous": unanimous
        }
    
    def handle_tie(self, tied_options: List[str]) -> str:
        """
        Handle tie-breaking between tied options.
        
        Args:
            tied_options: Options with equal votes
            
        Returns:
            Chosen option
        """
        # Choose option with highest average confidence
        option_confidences: Dict[str, List[float]] = {opt: [] for opt in tied_options}
        
        for vote in self.votes:
            if vote.option in option_confidences:
                option_confidences[vote.option].append(vote.confidence)
        
        best_option = max(
            tied_options,
            key=lambda opt: (
                sum(option_confidences[opt]) /
                max(1, len(option_confidences[opt]))
            )
        )
        
        return best_option
