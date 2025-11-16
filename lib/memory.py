"""
Memory Management System
Handles read/write/update operations for the agent swarm's persistent memory.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class MemoryManager:
    """Manages all persistent memory operations for the agent swarm."""

    def __init__(self, base_path: str = "memory"):
        self.base_path = Path(base_path)
        self.knowledge_path = self.base_path / "knowledge.json"
        self.outcomes_path = self.base_path / "outcomes.json"
        self.log_path = self.base_path / "system_log.md"
        self.context_path = self.base_path / "context_window.md"

    # ===== KNOWLEDGE BASE =====

    def read_knowledge(self) -> Dict[str, Any]:
        """Read the entire knowledge base."""
        with open(self.knowledge_path, 'r') as f:
            return json.load(f)

    def write_knowledge(self, data: Dict[str, Any]) -> None:
        """Write the entire knowledge base."""
        data['last_updated'] = datetime.now().isoformat()
        with open(self.knowledge_path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_fact(self, fact: str, category: str = "general") -> None:
        """Add a new fact to the knowledge base."""
        knowledge = self.read_knowledge()
        knowledge['facts'].append({
            'content': fact,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })
        self.write_knowledge(knowledge)

    def add_pattern(self, pattern: Dict[str, Any]) -> None:
        """Add a recognized pattern to the knowledge base."""
        knowledge = self.read_knowledge()
        pattern['timestamp'] = datetime.now().isoformat()
        knowledge['patterns'].append(pattern)
        self.write_knowledge(knowledge)

    def add_learning(self, learning: str, context: str = "") -> None:
        """Add a distilled learning to the knowledge base."""
        knowledge = self.read_knowledge()
        knowledge['learnings'].append({
            'content': learning,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        self.write_knowledge(knowledge)

    def update_domain_knowledge(self, domain: str, key: str, value: Any) -> None:
        """Update domain-specific knowledge."""
        knowledge = self.read_knowledge()
        if domain not in knowledge['domain_knowledge']:
            knowledge['domain_knowledge'][domain] = {}
        knowledge['domain_knowledge'][domain][key] = value
        self.write_knowledge(knowledge)

    def query_knowledge(self, query_type: str = "all") -> Any:
        """Query the knowledge base."""
        knowledge = self.read_knowledge()
        if query_type == "all":
            return knowledge
        elif query_type in knowledge:
            return knowledge[query_type]
        else:
            return None

    # ===== OUTCOMES HISTORY =====

    def read_outcomes(self) -> Dict[str, Any]:
        """Read the outcomes history."""
        with open(self.outcomes_path, 'r') as f:
            return json.load(f)

    def write_outcomes(self, data: Dict[str, Any]) -> None:
        """Write the outcomes history."""
        with open(self.outcomes_path, 'w') as f:
            json.dump(data, f, indent=2)

    def record_outcome(self, task: str, winner: Dict[str, Any],
                      all_candidates: List[Dict[str, Any]],
                      selection_rationale: str) -> None:
        """Record a selected outcome from the evolutionary process."""
        outcomes = self.read_outcomes()
        outcomes['history'].append({
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'winner': winner,
            'num_candidates': len(all_candidates),
            'selection_rationale': selection_rationale,
            'all_scores': [c.get('score', 0) for c in all_candidates]
        })
        self.write_outcomes(outcomes)

    # ===== SYSTEM LOG =====

    def append_log(self, entry: str, level: str = "INFO") -> None:
        """Append an entry to the system log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n### [{level}] {timestamp}\n\n{entry}\n\n---\n"

        with open(self.log_path, 'a') as f:
            f.write(log_entry)

    def read_log(self, num_entries: Optional[int] = None) -> str:
        """Read the system log (optionally last N entries)."""
        with open(self.log_path, 'r') as f:
            content = f.read()

        if num_entries:
            entries = content.split('---')
            return '---'.join(entries[-num_entries:])
        return content

    # ===== CONTEXT WINDOW =====

    def update_context(self, task: str = "", agents: List[str] = None,
                      results: str = "", notes: str = "") -> None:
        """Update the context window with current task state."""
        content = f"""# Context Window (Scratchpad)

## Current Task
{task if task else "None"}

## Active Agents
{', '.join(agents) if agents else "None"}

## Intermediate Results
{results if results else "None"}

## Notes
{notes if notes else "Working memory for current task."}

---
Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        with open(self.context_path, 'w') as f:
            f.write(content)

    def read_context(self) -> str:
        """Read the current context window."""
        with open(self.context_path, 'r') as f:
            return f.read()

    def clear_context(self) -> None:
        """Clear the context window."""
        self.update_context()

    # ===== UTILITY =====

    def get_recent_outcomes(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get the N most recent outcomes."""
        outcomes = self.read_outcomes()
        return outcomes['history'][-n:] if outcomes['history'] else []

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the memory system."""
        knowledge = self.read_knowledge()
        outcomes = self.read_outcomes()

        return {
            'num_facts': len(knowledge.get('facts', [])),
            'num_patterns': len(knowledge.get('patterns', [])),
            'num_learnings': len(knowledge.get('learnings', [])),
            'num_outcomes': len(outcomes.get('history', [])),
            'domains': list(knowledge.get('domain_knowledge', {}).keys())
        }


if __name__ == "__main__":
    # Quick test
    mm = MemoryManager()
    print("Memory Manager initialized")
    print("Stats:", mm.get_stats())
