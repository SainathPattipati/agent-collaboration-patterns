"""
Supervisor pattern implementation for agent coordination.

Supervisor delegates tasks to worker agents and manages results.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
import asyncio


@dataclass
class Task:
    """Represents a delegated task."""
    
    task_id: str
    description: str
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Any] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class WorkerAgent(ABC):
    """Base class for worker agents."""
    
    def __init__(self, name: str, expertise: Optional[str] = None):
        """
        Initialize worker agent.
        
        Args:
            name: Agent name
            expertise: Domain of expertise
        """
        self.name = name
        self.expertise = expertise
        self.completed_tasks = 0
        self.failed_tasks = 0
    
    @abstractmethod
    async def execute(self, task: Task) -> Any:
        """
        Execute a task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        pass
    
    def get_load(self) -> float:
        """Get current load score (0-1)."""
        return self.failed_tasks / max(1, self.completed_tasks + self.failed_tasks)


class SupervisorAgent:
    """
    Supervises and coordinates worker agents.
    
    Handles task delegation, result validation, and retry logic.
    """
    
    def __init__(
        self,
        name: str,
        max_retries: int = 3,
        timeout: float = 30.0
    ):
        """
        Initialize supervisor.
        
        Args:
            name: Supervisor name
            max_retries: Max retries on failure
            timeout: Task timeout in seconds
        """
        self.name = name
        self.workers: Dict[str, WorkerAgent] = {}
        self.tasks: Dict[str, Task] = {}
        self.max_retries = max_retries
        self.timeout = timeout
    
    def register_worker(self, worker: WorkerAgent) -> None:
        """Register a worker agent."""
        self.workers[worker.name] = worker
    
    def select_worker(self, expertise: Optional[str] = None) -> Optional[WorkerAgent]:
        """
        Select best worker based on load and expertise.
        
        Args:
            expertise: Required expertise
            
        Returns:
            Selected worker or None
        """
        candidates = list(self.workers.values())
        
        if expertise:
            candidates = [
                w for w in candidates
                if w.expertise == expertise
            ]
        
        if not candidates:
            return None
        
        # Select worker with lowest load
        return min(candidates, key=lambda w: w.get_load())
    
    async def delegate_task(
        self,
        task_description: str,
        expertise: Optional[str] = None
    ) -> Optional[Any]:
        """
        Delegate a task to suitable worker.
        
        Args:
            task_description: Description of task
            expertise: Required expertise
            
        Returns:
            Task result
        """
        worker = self.select_worker(expertise)
        if not worker:
            return None
        
        task = Task(
            task_id=f"task_{len(self.tasks)}",
            description=task_description,
            assigned_to=worker.name
        )
        self.tasks[task.task_id] = task
        
        # Try to execute with retries
        for attempt in range(self.max_retries):
            try:
                task.status = "running"
                result = await asyncio.wait_for(
                    worker.execute(task),
                    timeout=self.timeout
                )
                task.status = "completed"
                task.result = result
                task.completed_at = datetime.now()
                worker.completed_tasks += 1
                return result
            except asyncio.TimeoutError:
                task.status = "failed"
                worker.failed_tasks += 1
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get supervisor status."""
        completed = sum(
            1 for t in self.tasks.values()
            if t.status == "completed"
        )
        failed = sum(
            1 for t in self.tasks.values()
            if t.status == "failed"
        )
        
        return {
            "supervisor": self.name,
            "total_workers": len(self.workers),
            "total_tasks": len(self.tasks),
            "completed_tasks": completed,
            "failed_tasks": failed,
            "success_rate": completed / max(1, len(self.tasks))
        }
