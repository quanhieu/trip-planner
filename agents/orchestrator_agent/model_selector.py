from typing import Dict, Any, List
from enum import Enum
import logging
from common.config import settings

logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskType(Enum):
    SEARCH = "search"
    ENTERTAINMENT = "entertainment"
    MEAL = "meal"
    STAY = "stay"

class ModelSelector:
    """Selects appropriate model based on task requirements."""
    
    # Task type to required strengths mapping
    TASK_REQUIREMENTS = {
        TaskType.SEARCH: ["factual_queries", "information_extraction"],
        TaskType.ENTERTAINMENT: ["creative_tasks", "detailed_planning"],
        TaskType.MEAL: ["basic_planning", "analysis"],
        TaskType.STAY: ["analysis", "structured_output", "travel_planning"]
    }
    
    def __init__(self):
        self.model_capabilities = {}
        self._load_model_configs()
        logger.info(f"ModelSelector initialized with {len(self.model_capabilities)} models: {list(self.model_capabilities.keys())}")

    def _load_model_configs(self):
        """Load model configurations from settings."""
        for model_name, config in settings.MODEL_CONFIGS.items():
            try:
                self.model_capabilities[model_name] = {
                    "complexity": TaskComplexity[config["complexity"]],
                    "context_length": config["context_length"],
                    "cost_per_token": config["cost_per_token"],
                    "strengths": config["strengths"]
                }
                logger.debug(f"Loaded config for model: {model_name}")
            except KeyError as e:
                logger.error(f"Error loading model {model_name} config: {str(e)}")
                # Continue loading other models even if one fails

    def select_model(self, task_type: str, task_data: Dict[str, Any]) -> str:
        """Select the most appropriate model for a given task."""
        try:
            # Validate task type
            if not task_type or not isinstance(task_type, str):
                logger.warning(f"Invalid task_type: {task_type}. Using default model.")
                return settings.DEFAULT_MODEL
                
            # Convert to enum
            try:
                task_enum = TaskType(task_type)
            except ValueError:
                logger.warning(f"Unknown task type: {task_type}. Using default model.")
                return settings.DEFAULT_MODEL
                
            # Analyze complexity
            complexity = self._analyze_task_complexity(task_type, task_data)
            
            # Check if we have required strengths for this task type
            if task_enum not in self.TASK_REQUIREMENTS:
                logger.warning(f"No strength requirements defined for task type: {task_type}")
                return settings.DEFAULT_MODEL
                
            # Get required strengths for the task
            required_strengths = self.TASK_REQUIREMENTS[task_enum]
            
            # Score each model based on their suitability for the task
            model_scores = self._score_models(required_strengths, complexity)
            
            if not model_scores:
                logger.warning("No models scored. Using default model.")
                return settings.DEFAULT_MODEL
                
            # Log all model scores for debugging
            logger.debug(f"Model scores for {task_type} ({complexity.value}): {model_scores}")
            
            # Select the model with the highest score
            selected_model = max(model_scores.items(), key=lambda x: x[1])[0]
            
            logger.info(f"Selected model {selected_model} for task {task_type} "
                       f"with complexity {complexity.value}")
            
            return selected_model
                
        except Exception as e:
            logger.error(f"Error selecting model: {str(e)}", exc_info=True)
            # Get the default high-complexity model from settings
            try:
                default_model = next(
                    (name for name, config in settings.MODEL_CONFIGS.items() 
                     if config["complexity"] == "HIGH"),
                    "gpt-4o-mini"  # Fallback if no HIGH complexity model found
                )
                logger.info(f"Using fallback model: {default_model}")
                return default_model
            except Exception as fallback_error:
                logger.error(f"Error selecting fallback model: {str(fallback_error)}")
                return settings.DEFAULT_MODEL

    def _score_models(self, required_strengths: List[str], 
                     complexity: TaskComplexity) -> Dict[str, float]:
        """Score models based on their suitability for the task."""
        scores = {}
        
        for model_name, capabilities in self.model_capabilities.items():
            score = 0.0
            
            # Score based on matching strengths
            model_strengths = set(capabilities["strengths"])
            required_strengths_set = set(required_strengths)
            strength_match = len(model_strengths & required_strengths_set) / len(required_strengths_set)
            score += strength_match * 0.4  # 40% weight for strength match
            
            # Score based on complexity match
            if capabilities["complexity"] == complexity:
                score += 0.3  # 30% weight for matching complexity
            elif capabilities["complexity"].value > complexity.value:
                score += 0.2  # 20% weight for higher complexity
            
            # Score based on cost efficiency (inverse of cost)
            cost_score = 1 - (capabilities["cost_per_token"] / 0.03)  # Normalize by highest cost
            score += cost_score * 0.3  # 30% weight for cost efficiency
            
            scores[model_name] = score
            
        return scores

    def _analyze_task_complexity(self, task_type: str, task_data: Dict[str, Any]) -> TaskComplexity:
        """Analyze the complexity of a task based on its data."""
        # Count the number of requirements/constraints
        num_requirements = len(task_data.get("requirements", []))
        num_constraints = len(task_data.get("constraints", []))
        
        # Check if there are special requirements
        has_special_reqs = bool(task_data.get("special_requirements"))
        
        # Check for task-specific complexity factors
        try:
            task_enum = TaskType(task_type)
            additional_complexity = self._get_task_specific_complexity(task_enum, task_data)
        except ValueError:
            logger.warning(f"Invalid task type when analyzing complexity: {task_type}")
            additional_complexity = 0
        
        # Calculate total complexity score
        complexity_score = num_requirements + num_constraints + additional_complexity
        if has_special_reqs:
            complexity_score += 2
        
        # Log complexity calculation
        logger.debug(f"Task complexity for {task_type}: score={complexity_score} "
                   f"(reqs={num_requirements}, constraints={num_constraints}, "
                   f"additional={additional_complexity}, special={has_special_reqs})")
        
        # Determine complexity based on score
        if complexity_score > 5:
            return TaskComplexity.HIGH
        elif complexity_score > 2:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.LOW

    def _get_task_specific_complexity(self, task_type: TaskType, 
                                    task_data: Dict[str, Any]) -> int:
        """Get additional complexity score based on task-specific factors."""
        if task_type == TaskType.SEARCH:
            # More complex if searching multiple categories or detailed filters
            return len(task_data.get("categories", [])) + len(task_data.get("filters", []))
            
        elif task_type == TaskType.ENTERTAINMENT:
            # More complex if handling multiple days or specific time slots
            return len(task_data.get("days", [])) + len(task_data.get("time_slots", []))
            
        elif task_type == TaskType.MEAL:
            # More complex if handling dietary restrictions or specific cuisines
            return (len(task_data.get("dietary_restrictions", [])) + 
                   len(task_data.get("preferred_cuisines", [])))
            
        elif task_type == TaskType.STAY:
            # More complex if handling specific amenities or location requirements
            return (len(task_data.get("required_amenities", [])) + 
                   len(task_data.get("location_preferences", [])))
            
        return 0

    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model."""
        try:
            if model_name not in self.model_capabilities:
                logger.warning(f"Unknown model: {model_name}. Using default model.")
                model_name = settings.DEFAULT_MODEL
                
            if model_name not in self.model_capabilities:
                logger.error(f"Default model {model_name} not found in capabilities!")
                # Return a basic config as last resort
                return {
                    "model": model_name,
                    "temperature": settings.DEFAULT_TEMPERATURE,
                    "max_tokens": settings.DEFAULT_MAX_TOKENS
                }
                
            return {
                "model": model_name,
                "temperature": settings.DEFAULT_TEMPERATURE,
                "max_tokens": min(settings.DEFAULT_MAX_TOKENS, 
                                self.model_capabilities[model_name]["context_length"])
            }
        except Exception as e:
            logger.error(f"Error getting model config: {str(e)}")
            return {
                "model": settings.DEFAULT_MODEL,
                "temperature": settings.DEFAULT_TEMPERATURE,
                "max_tokens": settings.DEFAULT_MAX_TOKENS
            } 