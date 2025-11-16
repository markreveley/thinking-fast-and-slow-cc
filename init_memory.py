#!/usr/bin/env python3
"""
Initialize Memory System

This script initializes or resets the memory system for the agent swarm.
Run this before starting a fresh session.
"""

import os
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from memory import MemoryManager


def init_memory(reset: bool = False):
    """
    Initialize the memory system.

    Args:
        reset: If True, clears existing memory. If False, preserves existing data.
    """
    print("🧠 Initializing Agent Swarm Memory System...")
    print()

    # Create memory manager
    mm = MemoryManager()

    if reset:
        print("⚠️  RESET MODE: Clearing all existing memory...")
        # Clear by writing fresh templates
        mm.write_knowledge({
            "version": "1.0.0",
            "last_updated": "",
            "facts": [],
            "patterns": [],
            "learnings": [],
            "domain_knowledge": {}
        })

        mm.write_outcomes({
            "version": "1.0.0",
            "history": []
        })

        mm.clear_context()

        # Clear log by rewriting header
        with open(mm.log_path, 'w') as f:
            f.write("# System Log\n\n## Purpose\n")
            f.write("Chronological trace of all reasoning cycles, decisions, and agent interactions.\n\n")
            f.write("---\n\n## Log Entries\n\n")
            f.write("<!-- Entries will be appended below -->\n")

        print("✅ Memory reset complete")
    else:
        print("📂 Preserving existing memory")

    # Add initial log entry
    mm.append_log(
        "Memory system initialized. Agent swarm ready.",
        level="SYSTEM"
    )

    # Get stats
    stats = mm.get_stats()
    print()
    print("📊 Memory System Stats:")
    print(f"   - Facts: {stats['num_facts']}")
    print(f"   - Patterns: {stats['num_patterns']}")
    print(f"   - Learnings: {stats['num_learnings']}")
    print(f"   - Outcomes: {stats['num_outcomes']}")
    print(f"   - Domains: {len(stats['domains'])}")
    print()

    print("✅ Memory system ready!")
    print()
    print("Next steps:")
    print("  1. Run: python run_task.py \"<your task>\"")
    print("  2. Or run demo: python test_cycle.py")


def demo_populate():
    """Populate memory with some example data for testing."""
    print("📝 Populating with demo data...")

    mm = MemoryManager()

    # Add some facts
    mm.add_fact("Agent swarms use evolutionary selection to choose best outputs", "architecture")
    mm.add_fact("System-1 agents are fast but less accurate", "agent_behavior")
    mm.add_fact("System-2 agents are slow but more rigorous", "agent_behavior")

    # Add a pattern
    mm.add_pattern({
        "name": "webapp_design",
        "description": "Webapp design tasks benefit from S1 ideation + S2 verification",
        "success_rate": 0.85
    })

    # Add a learning
    mm.add_learning(
        "For complex planning tasks, S2 Planner outperforms S1 agents",
        context="Based on 5 trials"
    )

    # Update domain knowledge
    mm.update_domain_knowledge("webapp", "preferred_stack", "React + Node.js + PostgreSQL")

    print("✅ Demo data added")
    print()
    print(mm.get_stats())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialize agent swarm memory")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset all memory (WARNING: deletes existing data)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Populate with demo data"
    )

    args = parser.parse_args()

    init_memory(reset=args.reset)

    if args.demo:
        print()
        demo_populate()
