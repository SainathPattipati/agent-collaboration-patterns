"""
Tests for collaboration patterns.

Validates core functionality of each pattern.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from patterns import (
    DebateOrchestrator,
    ConsensusEngine,
    SwarmIntelligence
)


class TestPatterns(unittest.TestCase):
    """Test cases for collaboration patterns."""
    
    def test_debate_orchestrator(self):
        """Test debate pattern."""
        debate = DebateOrchestrator(num_rounds=3)
        result = debate.run_debate(
            topic="Test topic",
            proposer_position="Test position"
        )
        
        self.assertEqual(result['total_rounds'], 3)
        self.assertIn('consensus', result)
        self.assertGreaterEqual(result['avg_consensus_score'], 0)
        self.assertLessEqual(result['avg_consensus_score'], 1)
    
    def test_consensus_engine(self):
        """Test consensus pattern."""
        consensus = ConsensusEngine()
        consensus.add_vote("Agent1", "OptionA", 0.9)
        consensus.add_vote("Agent2", "OptionA", 0.8)
        consensus.add_vote("Agent3", "OptionB", 0.6)
        
        result = consensus.calculate_consensus()
        self.assertEqual(result['consensus'], "OptionA")
        self.assertGreater(result['confidence'], 0)
    
    def test_swarm_convergence(self):
        """Test swarm convergence."""
        swarm = SwarmIntelligence(num_agents=10)
        
        for _ in range(10):
            stats = swarm.run_iteration()
        
        self.assertGreater(stats['convergence_ratio'], 0)
        self.assertLess(stats['convergence_ratio'], 1)


if __name__ == "__main__":
    unittest.main()
