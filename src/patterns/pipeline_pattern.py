"""
Pipeline pattern for sequential agent chains.

Validates input/output schemas between stages.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class SchemaValidation:
    """Schema validation between pipeline stages."""
    
    required_fields: List[str]
    optional_fields: List[str] = None
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate data against schema."""
        return all(field in data for field in self.required_fields)


class PipelineStage(ABC):
    """Base class for pipeline stages."""
    
    def __init__(
        self,
        name: str,
        input_schema: SchemaValidation,
        output_schema: SchemaValidation
    ):
        """
        Initialize pipeline stage.
        
        Args:
            name: Stage name
            input_schema: Input validation schema
            output_schema: Output validation schema
        """
        self.name = name
        self.input_schema = input_schema
        self.output_schema = output_schema
    
    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute stage logic."""
        pass


class PipelineOrchestrator:
    """
    Orchestrates sequential agent chains with validation.
    
    Validates data at each stage and supports branching and skipping.
    """
    
    def __init__(self, name: str = "Pipeline"):
        """Initialize pipeline."""
        self.name = name
        self.stages: List[PipelineStage] = []
        self.execution_history: List[Dict[str, Any]] = []
    
    def add_stage(self, stage: PipelineStage) -> None:
        """
        Add a stage to the pipeline.
        
        Args:
            stage: Pipeline stage to add
        """
        self.stages.append(stage)
    
    def execute(
        self,
        initial_data: Dict[str, Any],
        skip_stages: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute pipeline stages sequentially.
        
        Args:
            initial_data: Initial input data
            skip_stages: Optional list of stages to skip
            
        Returns:
            Final result or None if validation fails
        """
        current_data = initial_data
        skip_stages = skip_stages or []
        
        for stage in self.stages:
            if stage.name in skip_stages:
                continue
            
            # Validate input
            if not stage.input_schema.validate(current_data):
                return None
            
            # Execute stage
            result = stage.execute(current_data)
            if result is None:
                return None
            
            # Validate output
            if not stage.output_schema.validate(result):
                return None
            
            current_data = result
            self.execution_history.append({
                "stage": stage.name,
                "data": result
            })
        
        return current_data
    
    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Get execution history."""
        return self.execution_history
