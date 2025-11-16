#!/usr/bin/env python3
"""
Test Cycle - Demo Script

Runs the example task through the agent swarm:
"Design a small webapp idea for musicians and outline the MVP architecture."

This demonstrates the full S1→S2→Selection cycle.
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from run_task import AgentSwarm
from memory import MemoryManager


def run_demo():
    """Run the demo task through the swarm."""

    print("\n" + "=" * 80)
    print("🎵 DEMO: Musician Webapp Design")
    print("=" * 80)
    print()
    print("This demo will run the following task through the agent swarm:")
    print()
    print("  'Design a small webapp idea for musicians and outline the MVP architecture.'")
    print()
    print("The swarm will:")
    print("  1. Route to appropriate agents (S1 + S2)")
    print("  2. Collect multiple candidate solutions")
    print("  3. Use evolutionary selection to pick the best")
    print("  4. Record the outcome and learnings")
    print()
    input("Press ENTER to start...")
    print()

    # Define the task
    task = "Design a small webapp idea for musicians and outline the MVP architecture."

    # Create swarm
    swarm = AgentSwarm()

    # Run task
    result = swarm.run_task(task, context={'depth': 'high'})

    # Display detailed results
    print("\n" + "=" * 80)
    print("📊 DETAILED RESULTS")
    print("=" * 80)
    print()

    print(f"Task: {result['task']}")
    print()

    print(f"Agents Used: {len(result['agents_used'])}")
    for agent in result['agents_used']:
        print(f"  - {agent}")
    print()

    print(f"Candidates Evaluated: {result['num_candidates']}")
    print()

    print(f"Winner: {result['winner']['agent']}")
    print(f"Score: {result['winner']['final_score']:.2f}/100")
    print()

    print("Selection Rationale:")
    print(result['rationale'])
    print()

    print("-" * 80)
    print("FINAL SOLUTION:")
    print("-" * 80)
    print(result['winner']['output'])
    print("-" * 80)
    print()

    # Show memory stats
    print("=" * 80)
    print("💾 MEMORY SYSTEM STATUS")
    print("=" * 80)
    print()

    mm = MemoryManager()
    stats = mm.get_stats()

    print(f"Facts stored: {stats['num_facts']}")
    print(f"Patterns recognized: {stats['num_patterns']}")
    print(f"Learnings accumulated: {stats['num_learnings']}")
    print(f"Outcomes recorded: {stats['num_outcomes']}")
    print()

    # Show recent outcomes
    print("Recent outcomes:")
    recent = mm.get_recent_outcomes(n=3)
    for i, outcome in enumerate(recent[-3:], 1):
        print(f"  {i}. {outcome['task'][:60]}... → {outcome['winner']['agent']}")
    print()

    print("=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  - Check memory/outcomes.json to see recorded results")
    print("  - Check memory/system_log.md to see reasoning trace")
    print("  - Run your own tasks: python run_task.py \"<your task>\"")
    print()


def show_agent_info():
    """Display information about available agents."""

    print("\n" + "=" * 80)
    print("🤖 AVAILABLE AGENTS")
    print("=" * 80)
    print()

    agents = [
        {
            "name": "s1_pattern_agent",
            "type": "System-1 (Fast)",
            "role": "Pattern recognition and heuristic responses",
            "strength": "Quick insights, familiar problems",
            "speed": "Very fast (<5 sec)"
        },
        {
            "name": "s1_option_generator",
            "type": "System-1 (Fast)",
            "role": "Divergent thinking and option generation",
            "strength": "Creative brainstorming, multiple alternatives",
            "speed": "Very fast (<5 sec)"
        },
        {
            "name": "s2_reasoner",
            "type": "System-2 (Slow)",
            "role": "Deep analysis and verification",
            "strength": "Rigorous logic, critique, correctness",
            "speed": "Slow (30-60 sec)"
        },
        {
            "name": "s2_planner",
            "type": "System-2 (Slow)",
            "role": "Strategic planning and architecture",
            "strength": "Detailed plans, dependencies, roadmaps",
            "speed": "Slow (45-90 sec)"
        }
    ]

    for agent in agents:
        print(f"📌 {agent['name']}")
        print(f"   Type: {agent['type']}")
        print(f"   Role: {agent['role']}")
        print(f"   Strength: {agent['strength']}")
        print(f"   Speed: {agent['speed']}")
        print()

    print("=" * 80)
    print()


def run_multiple_tests():
    """Run multiple test tasks to populate memory."""

    print("\n" + "=" * 80)
    print("🔄 RUNNING MULTIPLE TEST TASKS")
    print("=" * 80)
    print()

    test_tasks = [
        "Design a small webapp idea for musicians and outline the MVP architecture.",
        "Brainstorm creative marketing ideas for a new mobile app",
        "Analyze the trade-offs between using REST vs GraphQL for an API",
        "Create a 3-month roadmap for building a SaaS product"
    ]

    swarm = AgentSwarm()

    for i, task in enumerate(test_tasks, 1):
        print(f"\n--- Test {i}/{len(test_tasks)} ---")
        print(f"Task: {task}\n")

        result = swarm.run_task(task)

        print(f"Winner: {result['winner']['agent']}")
        print(f"Score: {result['winner']['final_score']:.2f}")
        print()

    print("=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print()

    # Show updated stats
    mm = MemoryManager()
    stats = mm.get_stats()
    print(f"Total outcomes recorded: {stats['num_outcomes']}")
    print(f"Total learnings: {stats['num_learnings']}")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the agent swarm")
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show information about available agents"
    )
    parser.add_argument(
        "--multiple",
        action="store_true",
        help="Run multiple test tasks"
    )

    args = parser.parse_args()

    if args.info:
        show_agent_info()
    elif args.multiple:
        run_multiple_tests()
    else:
        # Default: run single demo
        run_demo()
