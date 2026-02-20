"""
Example: Compare collaboration patterns on same problem.

Demonstrates how different patterns solve the same task.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from patterns import (
    SupervisorAgent,
    DebateOrchestrator,
    ConsensusEngine,
    SwarmIntelligence
)


def compare_patterns():
    """Compare all collaboration patterns."""
    
    task = "Optimize production deployment strategy"
    
    print(f"Task: {task}\n")
    
    # 1. Supervisor Pattern
    print("=== Supervisor Pattern ===")
    supervisor = SupervisorAgent("ProductionSupervisor")
    print(f"Supervisor: {supervisor.name}")
    print(f"Workers registered: {len(supervisor.workers)}")
    status = supervisor.get_status()
    print(f"Status: {status['success_rate']:.2%} success rate\n")
    
    # 2. Debate Pattern
    print("=== Debate Pattern ===")
    debate = DebateOrchestrator(num_rounds=3)
    result = debate.run_debate(
        topic="Microservices vs Monolithic",
        proposer_position="Use microservices for scalability"
    )
    print(f"Debate rounds: {result['total_rounds']}")
    print(f"Consensus score: {result['avg_consensus_score']:.2f}")
    print(f"Consensus reached: {result['consensus_reached']}\n")
    
    # 3. Consensus Pattern
    print("=== Consensus Pattern ===")
    consensus = ConsensusEngine()
    consensus.add_vote("DataEngineer", "PostgreSQL", 0.9, "ACID guarantees")
    consensus.add_vote("AppDev", "MongoDB", 0.7, "Flexibility")
    consensus.add_vote("DevOps", "PostgreSQL", 0.95, "Operational stability")
    
    result = consensus.calculate_consensus()
    print(f"Consensus option: {result['consensus']}")
    print(f"Consensus confidence: {result['confidence']:.2f}\n")
    
    # 4. Swarm Pattern
    print("=== Swarm Pattern ===")
    swarm = SwarmIntelligence(num_agents=20)
    
    # Run a few iterations
    for _ in range(5):
        stats = swarm.run_iteration()
    
    print(f"Timesteps: {stats['timestep']}")
    print(f"Unique locations: {stats['unique_locations']}")
    print(f"Convergence ratio: {stats['convergence_ratio']:.2f}\n")


if __name__ == "__main__":
    compare_patterns()
