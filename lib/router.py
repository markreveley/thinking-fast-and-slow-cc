"""
Task Router
Determines which agents should handle which tasks based on task characteristics.
"""

import re
from typing import List, Dict, Any, Optional
from enum import Enum


class AgentType(Enum):
    """Types of agents available in the swarm."""
    S1_PATTERN = "s1_pattern_agent"
    S1_OPTION_GEN = "s1_option_generator"
    S2_REASONER = "s2_reasoner"
    S2_PLANNER = "s2_planner"


class TaskRouter:
    """
    Routes tasks to appropriate agents based on task characteristics.
    Uses rule-based logic to determine optimal agent assignment.
    """

    def __init__(self):
        # Keywords that suggest System-1 (fast/heuristic) processing
        self.s1_keywords = [
            'brainstorm', 'ideas', 'options', 'alternatives', 'quick',
            'suggest', 'possibilities', 'variants', 'creative', 'imagine',
            'what if', 'list', 'generate'
        ]

        # Keywords that suggest System-2 (slow/deliberative) processing
        self.s2_keywords = [
            'analyze', 'design', 'plan', 'architect', 'implement',
            'reason', 'prove', 'verify', 'calculate', 'optimize',
            'explain', 'why', 'how does', 'debug', 'review', 'evaluate'
        ]

        # Keywords for planning tasks
        self.planning_keywords = [
            'plan', 'roadmap', 'strategy', 'approach', 'steps',
            'architecture', 'design', 'structure', 'organize', 'workflow'
        ]

        # Keywords for pattern recognition
        self.pattern_keywords = [
            'pattern', 'similar', 'like', 'recognize', 'match',
            'category', 'classify', 'identify', 'detect'
        ]

    def route(self, task: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Route a task to appropriate agents.

        Args:
            task: The task description
            context: Optional context (previous results, urgency, etc.)

        Returns:
            List of agent names that should process this task
        """
        task_lower = task.lower()

        # Default routing decision
        agents = []

        # Compute task characteristics
        needs_speed = self._needs_speed(task_lower, context)
        needs_depth = self._needs_depth(task_lower, context)
        needs_creativity = self._needs_creativity(task_lower)
        needs_planning = self._needs_planning(task_lower)
        needs_patterns = self._needs_patterns(task_lower)

        # Routing logic
        if needs_speed and needs_creativity:
            # Fast, creative task → both S1 agents
            agents.extend([AgentType.S1_PATTERN.value, AgentType.S1_OPTION_GEN.value])

        elif needs_depth and needs_planning:
            # Deep planning task → S2 planner + reasoner for verification
            agents.extend([AgentType.S2_PLANNER.value, AgentType.S2_REASONER.value])

        elif needs_patterns:
            # Pattern recognition → S1 pattern agent + S2 reasoner for validation
            agents.extend([AgentType.S1_PATTERN.value, AgentType.S2_REASONER.value])

        elif needs_planning:
            # Planning task → S2 planner primarily
            agents.append(AgentType.S2_PLANNER.value)
            # Optionally add S1 for initial ideas
            if needs_creativity:
                agents.append(AgentType.S1_OPTION_GEN.value)

        elif needs_depth:
            # Deep reasoning → S2 reasoner
            agents.append(AgentType.S2_REASONER.value)

        elif needs_speed or needs_creativity:
            # Fast/creative → S1 agents
            agents.extend([AgentType.S1_PATTERN.value, AgentType.S1_OPTION_GEN.value])

        else:
            # Default: use all agents for comprehensive coverage
            agents.extend([
                AgentType.S1_PATTERN.value,
                AgentType.S1_OPTION_GEN.value,
                AgentType.S2_REASONER.value,
                AgentType.S2_PLANNER.value
            ])

        # Remove duplicates while preserving order
        seen = set()
        unique_agents = []
        for agent in agents:
            if agent not in seen:
                seen.add(agent)
                unique_agents.append(agent)

        return unique_agents

    def _needs_speed(self, task: str, context: Optional[Dict[str, Any]]) -> bool:
        """Determine if task requires fast processing."""
        if context and context.get('urgency') == 'high':
            return True

        speed_indicators = ['quick', 'fast', 'immediately', 'asap', 'urgent']
        return any(indicator in task for indicator in speed_indicators)

    def _needs_depth(self, task: str, context: Optional[Dict[str, Any]]) -> bool:
        """Determine if task requires deep reasoning."""
        if context and context.get('depth') == 'high':
            return True

        return any(keyword in task for keyword in self.s2_keywords)

    def _needs_creativity(self, task: str) -> bool:
        """Determine if task requires creative thinking."""
        creativity_indicators = ['creative', 'innovative', 'novel', 'unique',
                                'brainstorm', 'ideas', 'imagine']
        return any(indicator in task for indicator in creativity_indicators)

    def _needs_planning(self, task: str) -> bool:
        """Determine if task requires planning."""
        return any(keyword in task for keyword in self.planning_keywords)

    def _needs_patterns(self, task: str) -> bool:
        """Determine if task involves pattern recognition."""
        return any(keyword in task for keyword in self.pattern_keywords)

    def should_escalate_to_s2(self, s1_result: Dict[str, Any],
                             confidence_threshold: float = 0.6) -> bool:
        """
        Determine if S1 result should be escalated to S2 for verification.

        Args:
            s1_result: Result from S1 agent
            confidence_threshold: Minimum confidence to avoid escalation

        Returns:
            True if should escalate to S2
        """
        confidence = s1_result.get('confidence', 0.5)

        # Low confidence → escalate
        if confidence < confidence_threshold:
            return True

        # High complexity → escalate
        if s1_result.get('metadata', {}).get('complexity') == 'high':
            return True

        # Flagged for verification
        if s1_result.get('needs_verification', False):
            return True

        return False

    def should_downgrade_to_s1(self, task: str, s2_available: bool = True) -> bool:
        """
        Determine if a task can be handled by S1 instead of S2.

        Args:
            task: Task description
            s2_available: Whether S2 agents are available

        Returns:
            True if S1 is sufficient
        """
        task_lower = task.lower()

        # If it's just brainstorming, S1 is fine
        if any(word in task_lower for word in ['brainstorm', 'ideas', 'options']):
            return True

        # If it's a simple query
        simple_indicators = ['what are', 'list', 'name', 'show']
        if any(indicator in task_lower for indicator in simple_indicators):
            return True

        return False

    def get_routing_explanation(self, task: str, agents: List[str]) -> str:
        """
        Generate human-readable explanation of routing decision.

        Args:
            task: The task
            agents: List of routed agents

        Returns:
            Explanation string
        """
        explanation = f"Task: '{task[:100]}...'\n\n"
        explanation += f"Routed to {len(agents)} agent(s):\n"

        for agent in agents:
            if 's1_' in agent:
                explanation += f"- {agent}: System-1 (fast/heuristic)\n"
            elif 's2_' in agent:
                explanation += f"- {agent}: System-2 (slow/deliberative)\n"

        task_lower = task.lower()
        characteristics = []

        if self._needs_speed(task_lower, None):
            characteristics.append("speed")
        if self._needs_depth(task_lower, None):
            characteristics.append("depth")
        if self._needs_creativity(task_lower):
            characteristics.append("creativity")
        if self._needs_planning(task_lower):
            characteristics.append("planning")

        if characteristics:
            explanation += f"\nTask characteristics: {', '.join(characteristics)}"

        return explanation


if __name__ == "__main__":
    # Quick test
    router = TaskRouter()

    test_tasks = [
        "Brainstorm ideas for a new mobile app",
        "Design a scalable architecture for user authentication",
        "Quickly list some options for database technologies",
        "Analyze the trade-offs between REST and GraphQL"
    ]

    for task in test_tasks:
        agents = router.route(task)
        print(f"\nTask: {task}")
        print(f"Agents: {agents}")
