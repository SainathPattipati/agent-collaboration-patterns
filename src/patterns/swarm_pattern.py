"""
Swarm pattern for emergent multi-agent coordination.

Implements pheromone-inspired coordination without central control.
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import math


@dataclass
class Pheromone:
    """Represents a pheromone trail."""
    
    location: str
    value: float  # 0 to 1
    age: int = 0  # number of timesteps
    created_at: datetime = field(default_factory=datetime.now)


class SwarmAgent:
    """Individual agent in the swarm."""
    
    def __init__(self, agent_id: str, initial_position: str = "origin"):
        """
        Initialize swarm agent.
        
        Args:
            agent_id: Unique agent identifier
            initial_position: Starting position
        """
        self.agent_id = agent_id
        self.position = initial_position
        self.local_pheromones: Dict[str, float] = {}
        self.visited_locations: Set[str] = {initial_position}
    
    def sense_pheromones(self, environment_pheromones: Dict[str, float]) -> None:
        """
        Sense pheromones in current environment.
        
        Args:
            environment_pheromones: Pheromones from environment
        """
        self.local_pheromones = environment_pheromones.copy()
    
    def decide_next_location(self) -> str:
        """
        Decide next location based on pheromones.
        
        Returns:
            Next location to move to
        """
        if not self.local_pheromones:
            return self.position
        
        # Choose location with highest pheromone
        best_location = max(
            self.local_pheromones.keys(),
            key=lambda loc: self.local_pheromones[loc]
        )
        
        return best_location
    
    def move(self, new_position: str) -> None:
        """Move agent to new position."""
        self.position = new_position
        self.visited_locations.add(new_position)


class SwarmIntelligence:
    """
    Coordinates multiple agents through emergent behavior.
    
    Implements pheromone-inspired coordination for convergence to solutions.
    """
    
    def __init__(self, num_agents: int = 10, decay_rate: float = 0.1):
        """
        Initialize swarm intelligence.
        
        Args:
            num_agents: Number of agents in swarm
            decay_rate: Pheromone decay rate per timestep
        """
        self.agents: List[SwarmAgent] = [
            SwarmAgent(f"agent_{i}")
            for i in range(num_agents)
        ]
        self.environment_pheromones: Dict[str, Pheromone] = {}
        self.decay_rate = decay_rate
        self.timestep = 0
    
    def deposit_pheromone(self, location: str, value: float) -> None:
        """
        Deposit pheromone at location.
        
        Args:
            location: Location to deposit
            value: Pheromone amount (0-1)
        """
        if location not in self.environment_pheromones:
            self.environment_pheromones[location] = Pheromone(
                location=location,
                value=value
            )
        else:
            pheromone = self.environment_pheromones[location]
            pheromone.value = min(1.0, pheromone.value + value)
    
    def evaporate_pheromones(self) -> None:
        """Apply pheromone decay."""
        for location, pheromone in self.environment_pheromones.items():
            pheromone.value *= (1 - self.decay_rate)
            pheromone.age += 1
    
    def update_agent_positions(self) -> None:
        """Update positions for all agents based on pheromones."""
        # Get pheromone values at each location
        pheromone_map = {
            loc: pheromone.value
            for loc, pheromone in self.environment_pheromones.items()
        }
        
        for agent in self.agents:
            # Sense pheromones
            agent.sense_pheromones(pheromone_map)
            
            # Decide and move
            next_location = agent.decide_next_location()
            agent.move(next_location)
            
            # Deposit pheromone at new location
            self.deposit_pheromone(next_location, 0.1)
    
    def run_iteration(self) -> Dict[str, any]:
        """
        Run one iteration of swarm algorithm.
        
        Returns:
            Iteration statistics
        """
        self.update_agent_positions()
        self.evaporate_pheromones()
        self.timestep += 1
        
        # Calculate convergence
        all_positions = [agent.position for agent in self.agents]
        unique_positions = len(set(all_positions))
        convergence_ratio = 1.0 - (unique_positions / len(self.agents))
        
        return {
            "timestep": self.timestep,
            "unique_locations": unique_positions,
            "convergence_ratio": convergence_ratio,
            "avg_pheromone": (
                sum(p.value for p in self.environment_pheromones.values()) /
                max(1, len(self.environment_pheromones))
            )
        }
    
    def is_converged(self, threshold: float = 0.8) -> bool:
        """Check if swarm has converged."""
        all_positions = [agent.position for agent in self.agents]
        convergence = (
            (len(set(all_positions)) - 1) /
            max(1, len(self.agents) - 1)
        )
        return convergence <= (1 - threshold)

def swarm_optimization(swarm: SwarmIntelligence, max_iterations: int = 100) -> float:
    """Run swarm until convergence or max iterations."""
    for _ in range(max_iterations):
        if swarm.is_converged():
            break
        swarm.run_iteration()
    return swarm.agents[0].position
