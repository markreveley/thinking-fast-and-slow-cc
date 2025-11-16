#!/usr/bin/env python3
"""
Agent Swarm Task Orchestrator

Coordinates the full S1 → S2 → Selection cycle for a given task.
This is the main entry point for running tasks through the agent swarm.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from memory import MemoryManager
from router import TaskRouter
from selector import EvolutionarySelector, create_candidate


class AgentSwarm:
    """Orchestrates the multi-agent cognitive architecture."""

    def __init__(self):
        self.memory = MemoryManager()
        self.router = TaskRouter()
        self.selector = EvolutionarySelector()

        # Agent definitions (loaded from markdown files)
        self.agents_dir = Path(__file__).parent / 'agents'

    def run_task(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a task through the agent swarm.

        Args:
            task: The user's task/question
            context: Optional context (urgency, depth, etc.)

        Returns:
            Final result with selected solution
        """
        print("=" * 80)
        print("🎯 AGENT SWARM - Task Execution")
        print("=" * 80)
        print()
        print(f"📝 Task: {task}")
        print()

        context = context or {}

        # Step 1: OVERSEER - Log and route
        print("🧠 [OVERSEER] Analyzing task and routing to agents...")
        self.memory.append_log(f"NEW TASK: {task}", level="TASK")

        # Route to agents
        agent_list = self.router.route(task, context)
        print(f"   → Routed to {len(agent_list)} agents: {', '.join(agent_list)}")
        print()

        routing_explanation = self.router.get_routing_explanation(task, agent_list)
        self.memory.append_log(f"ROUTING:\n{routing_explanation}", level="INFO")

        # Update context window
        self.memory.update_context(
            task=task,
            agents=agent_list,
            notes="Task execution in progress"
        )

        # Step 2: Run agents and collect candidates
        print("🤖 Running agents...")
        print()

        candidates = []

        for agent_name in agent_list:
            candidate = self._run_agent(agent_name, task, context)
            candidates.append(candidate)

            print(f"   ✅ {agent_name}")
            print(f"      Output: {candidate['output'][:100]}...")
            print(f"      Confidence: {candidate['confidence']:.2f}")
            print(f"      Score: {candidate.get('final_score', 'N/A')}")
            print()

        # Step 3: OVERSEER - Evolutionary selection
        print("🏆 [OVERSEER] Selecting best candidate...")
        print()

        winner, rationale = self.selector.select_best(candidates, task)

        print(f"   Winner: {winner['agent']}")
        print(f"   Score: {winner['final_score']:.2f}/100")
        print()
        print(f"   Rationale: {rationale}")
        print()

        # Step 4: Record outcome and learn
        print("💾 [OVERSEER] Recording outcome and learning...")

        self.memory.record_outcome(
            task=task,
            winner=winner,
            all_candidates=candidates,
            selection_rationale=rationale
        )

        # Extract learning
        learning = self._extract_learning(task, winner, candidates)
        if learning:
            self.memory.add_learning(learning, context=task[:100])
            print(f"   💡 Learning: {learning}")

        # Log to system
        self.memory.append_log(
            f"OUTCOME SELECTED:\nAgent: {winner['agent']}\nScore: {winner['final_score']:.2f}\n\n{rationale}",
            level="RESULT"
        )

        print()
        print("=" * 80)
        print("✅ TASK COMPLETE")
        print("=" * 80)
        print()

        # Return final result
        return {
            "task": task,
            "agents_used": agent_list,
            "num_candidates": len(candidates),
            "winner": winner,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        }

    def _run_agent(self, agent_name: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate running an individual agent.

        In a real implementation, this would:
        1. Load the agent's definition from agents/{agent_name}.md
        2. Invoke Claude Code with that agent's prompt
        3. Parse the response

        For this MVP, we'll generate realistic simulated responses.
        """
        # Load agent definition
        agent_file = self.agents_dir / f"{agent_name}.md"

        if not agent_file.exists():
            print(f"⚠️  Warning: Agent definition not found: {agent_file}")

        # Simulate agent execution based on agent type
        if 's1_pattern' in agent_name:
            return self._simulate_s1_pattern(task, context)
        elif 's1_option' in agent_name:
            return self._simulate_s1_option_gen(task, context)
        elif 's2_reasoner' in agent_name:
            return self._simulate_s2_reasoner(task, context)
        elif 's2_planner' in agent_name:
            return self._simulate_s2_planner(task, context)
        else:
            # Default
            return create_candidate(
                agent_name=agent_name,
                output=f"Response from {agent_name} for: {task}",
                confidence=0.5
            )

    def _simulate_s1_pattern(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate S1 Pattern Agent response."""
        # Quick pattern matching response
        output = f"Pattern recognized: This task is similar to 'creative project planning'. "
        output += f"Suggested approach: Start with user needs analysis, then brainstorm features. "
        output += f"Quick recommendation: Focus on MVP scope."

        return create_candidate(
            agent_name="s1_pattern_agent",
            output=output,
            scores={
                'completeness': 65,
                'correctness': 70,
                'clarity': 75,
                'feasibility': 80,
                'creativity': 70
            },
            confidence=0.72
        )

    def _simulate_s1_option_gen(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate S1 Option Generator response."""
        # Multiple quick options
        output = "Option 1: Build an MVP with core features only. "
        output += "Option 2: Start with market research and validation. "
        output += "Option 3: Create a prototype for user testing. "
        output += "Recommend Option 1 for speed to market."

        return create_candidate(
            agent_name="s1_option_generator",
            output=output,
            scores={
                'completeness': 75,
                'correctness': 65,
                'clarity': 80,
                'feasibility': 70,
                'creativity': 90
            },
            confidence=0.68
        )

    def _simulate_s2_reasoner(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate S2 Reasoner response."""
        # Deep analytical response
        output = "Analysis: After examining the requirements, I've identified 3 key considerations. "
        output += "1) Technical feasibility: achievable with standard tech stack. "
        output += "2) Resource requirements: 2-3 person team for 8-12 weeks. "
        output += "3) Risk factors: market validation needed before large investment. "
        output += "Recommendation: Proceed with phased approach - validate first, then build."

        return create_candidate(
            agent_name="s2_reasoner",
            output=output,
            scores={
                'completeness': 90,
                'correctness': 92,
                'clarity': 85,
                'feasibility': 88,
                'creativity': 60
            },
            confidence=0.87
        )

    def _simulate_s2_planner(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate S2 Planner response."""
        # Detailed plan
        output = "PLAN:\n\n"
        output += "Phase 1 (Weeks 1-4): Foundation\n"
        output += "- Set up infrastructure\n"
        output += "- Build core features\n"
        output += "- Initial testing\n\n"
        output += "Phase 2 (Weeks 5-8): Development\n"
        output += "- Implement main functionality\n"
        output += "- Integration testing\n"
        output += "- User feedback\n\n"
        output += "Phase 3 (Weeks 9-12): Polish & Launch\n"
        output += "- Bug fixes\n"
        output += "- Performance optimization\n"
        output += "- Launch preparation\n\n"
        output += "Total: 12 weeks, 2-person team"

        return create_candidate(
            agent_name="s2_planner",
            output=output,
            scores={
                'completeness': 95,
                'correctness': 88,
                'clarity': 92,
                'feasibility': 90,
                'creativity': 65
            },
            confidence=0.85
        )

    def _extract_learning(self, task: str, winner: Dict[str, Any],
                         all_candidates: List[Dict[str, Any]]) -> str:
        """Extract a learning from this task execution."""

        # Simple heuristic: if S2 won over S1, note that
        winner_type = "S2" if "s2_" in winner['agent'] else "S1"

        s1_count = sum(1 for c in all_candidates if "s1_" in c['agent'])
        s2_count = sum(1 for c in all_candidates if "s2_" in c['agent'])

        if winner_type == "S2" and s1_count > 0:
            return f"{winner_type} agent outperformed S1 on tasks requiring depth/planning"
        elif winner_type == "S1" and s2_count > 0:
            return f"{winner_type} agent was sufficient for this task (S2 overkill)"
        else:
            return f"Task completed successfully by {winner['agent']}"


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python run_task.py \"<your task>\"")
        print()
        print("Example:")
        print("  python run_task.py \"Design a webapp for musicians\"")
        sys.exit(1)

    task = sys.argv[1]

    # Optional context flags
    context = {}
    if "--urgent" in sys.argv:
        context['urgency'] = 'high'
    if "--deep" in sys.argv:
        context['depth'] = 'high'

    # Run the task
    swarm = AgentSwarm()
    result = swarm.run_task(task, context)

    # Print final answer
    print()
    print("📋 FINAL ANSWER:")
    print("-" * 80)
    print(result['winner']['output'])
    print("-" * 80)
    print()

    # Save result to temp folder
    output_file = Path(__file__).parent / "temp" / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"💾 Full result saved to: {output_file}")


if __name__ == "__main__":
    main()
