# Agent Swarm Cognitive Architecture

A multi-agent System-1/System-2 cognitive architecture built entirely inside Claude Code using local files, scripts, and threads. No external frameworks—just Python and persistence.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    OVERSEER                         │
│            (Meta-Agent Orchestrator)                │
│  • Routes tasks to agents                           │
│  • Performs evolutionary selection                  │
│  • Manages memory                                   │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
    ┌───▼────┐          ┌───▼────┐
    │ S1     │          │ S2     │
    │ Fast   │          │ Slow   │
    └───┬────┘          └───┬────┘
        │                   │
  ┌─────┴─────┐       ┌─────┴─────┐
  │           │       │           │
┌─▼─┐      ┌──▼┐   ┌──▼┐      ┌──▼─┐
│S1 │      │S1 │   │S2 │      │S2  │
│Pat│      │Opt│   │Rea│      │Plan│
│tern│      │Gen│   │son│      │ner │
└───┘      └───┘   └───┘      └────┘
```

### Components

**Overseer**: Coordinates all agents, routes tasks, performs evolutionary selection, manages memory

**System-1 Agents** (Fast/Heuristic):
- `s1_pattern_agent`: Pattern recognition, quick insights
- `s1_option_generator`: Creative brainstorming, multiple alternatives

**System-2 Agents** (Slow/Deliberative):
- `s2_reasoner`: Deep analysis, verification, critique
- `s2_planner`: Strategic planning, architecture, roadmaps

**Memory System**: Persistent storage using local files
- `knowledge.json`: Facts, patterns, learnings
- `outcomes.json`: Selected solutions history
- `system_log.md`: Chronological reasoning trace
- `context_window.md`: Short-term working memory

## Project Structure

```
thinking-fast-and-slow-cc/
├── agents/
│   ├── overseer.md              # Meta-agent definition
│   ├── s1_pattern_agent.md      # S1 pattern matcher
│   ├── s1_option_generator.md   # S1 option generator
│   ├── s2_reasoner.md           # S2 analytical reasoner
│   └── s2_planner.md            # S2 strategic planner
│
├── lib/
│   ├── memory.py                # Memory management
│   ├── router.py                # Task routing logic
│   └── selector.py              # Evolutionary selection
│
├── memory/
│   ├── knowledge.json           # Long-term knowledge
│   ├── outcomes.json            # Solution history
│   ├── system_log.md            # Reasoning trace
│   └── context_window.md        # Current task context
│
├── temp/                        # Temporary candidate storage
│
├── init_memory.py               # Initialize memory system
├── run_task.py                  # Main task orchestrator
├── test_cycle.py                # Demo/test script
└── README.md                    # This file
```

## Quick Start

### 1. Initialize the System

```bash
# Initialize memory (first time)
python init_memory.py

# Or reset and add demo data
python init_memory.py --reset --demo
```

### 2. Run the Demo

```bash
# Run the example task
python test_cycle.py
```

This will execute:
> "Design a small webapp idea for musicians and outline the MVP architecture."

### 3. Run Your Own Tasks

```bash
# Basic usage
python run_task.py "Your task here"

# With context flags
python run_task.py "Your task" --urgent  # High urgency
python run_task.py "Your task" --deep    # Deep analysis
```

## Example Output

```
================================================================================
🎯 AGENT SWARM - Task Execution
================================================================================

📝 Task: Design a small webapp idea for musicians and outline the MVP architecture.

🧠 [OVERSEER] Analyzing task and routing to agents...
   → Routed to 4 agents: s1_pattern_agent, s1_option_generator, s2_reasoner, s2_planner

🤖 Running agents...

   ✅ s1_pattern_agent
      Output: Pattern recognized: This task is similar to 'creative project planning'...
      Confidence: 0.72
      Score: 72.00

   ✅ s1_option_generator
      Output: Option 1: Build an MVP with core features only...
      Confidence: 0.68
      Score: 73.50

   ✅ s2_reasoner
      Output: Analysis: After examining the requirements...
      Confidence: 0.87
      Score: 87.40

   ✅ s2_planner
      Output: PLAN: Phase 1 (Weeks 1-4): Foundation...
      Confidence: 0.85
      Score: 90.00

🏆 [OVERSEER] Selecting best candidate...

   Winner: s2_planner
   Score: 90.00/100

   Rationale:
   Selected candidate from s2_planner with score 90.00/100.

   Key strengths:
   - Completeness: 95.00/100
   - Clarity: 92.00/100
   - Feasibility: 90.00/100

   Margin over runner-up: 2.60 points

   Total candidates evaluated: 4

💾 [OVERSEER] Recording outcome and learning...
   💡 Learning: S2 agent outperformed S1 on tasks requiring depth/planning

================================================================================
✅ TASK COMPLETE
================================================================================
```

## How It Works

### Task Execution Flow

1. **User submits task** → `run_task.py "<task>"`

2. **Overseer receives task**
   - Logs to `memory/system_log.md`
   - Updates `memory/context_window.md`

3. **Routing**
   - `TaskRouter` analyzes task characteristics
   - Determines which agents to use (S1, S2, or both)
   - Routes based on: speed needs, depth needs, creativity, planning

4. **Agent Execution** (simulated in MVP)
   - S1 agents: Fast pattern matching, option generation
   - S2 agents: Deep reasoning, detailed planning
   - Each produces a candidate solution with scores

5. **Evolutionary Selection**
   - `EvolutionarySelector` scores all candidates
   - Weights: completeness (25%), correctness (30%), clarity (20%), feasibility (15%), creativity (10%)
   - Selects winner, generates rationale

6. **Learning & Memory**
   - Records outcome to `memory/outcomes.json`
   - Extracts learning, adds to `memory/knowledge.json`
   - Logs full trace to `memory/system_log.md`

7. **Return result** to user

### Routing Logic

The `TaskRouter` uses keyword analysis to determine agent selection:

- **S1 keywords**: brainstorm, ideas, quick, creative, options
- **S2 keywords**: analyze, design, plan, verify, optimize
- **Planning keywords**: roadmap, architecture, strategy
- **Pattern keywords**: similar, recognize, classify

**Escalation**: S1 results with confidence < 0.6 escalate to S2 for verification.

### Evolutionary Selection

Candidates are scored on multiple criteria:
- **Completeness** (25%): Coverage of requirements
- **Correctness** (30%): Accuracy and soundness
- **Clarity** (20%): Understandability
- **Feasibility** (15%): Practicality
- **Creativity** (10%): Novelty

The highest-scoring candidate is selected as the winner.

## Memory System

### knowledge.json
```json
{
  "facts": [{"content": "...", "category": "...", "timestamp": "..."}],
  "patterns": [{"name": "...", "description": "...", "success_rate": 0.85}],
  "learnings": [{"content": "...", "context": "...", "timestamp": "..."}],
  "domain_knowledge": {"webapp": {"preferred_stack": "React + Node.js"}}
}
```

### outcomes.json
```json
{
  "history": [
    {
      "timestamp": "...",
      "task": "...",
      "winner": {"agent": "s2_planner", "output": "...", "final_score": 90},
      "num_candidates": 4,
      "selection_rationale": "...",
      "all_scores": [72, 73.5, 87.4, 90]
    }
  ]
}
```

## Agent Personalities

### S1 Pattern Agent
- **Speed**: Very fast (<5 sec)
- **Style**: Intuitive, pattern-matching
- **Strength**: Familiar problems, quick insights
- **Weakness**: Novel problems, may miss edge cases

### S1 Option Generator
- **Speed**: Very fast (<5 sec)
- **Style**: Divergent thinking, high volume
- **Strength**: Creative brainstorming, multiple alternatives
- **Weakness**: Limited quality filtering

### S2 Reasoner
- **Speed**: Slow (30-60 sec)
- **Style**: Analytical, verification-focused
- **Strength**: Correctness, critique, deep analysis
- **Weakness**: Less creative, slower

### S2 Planner
- **Speed**: Slow (45-90 sec)
- **Style**: Strategic, structured
- **Strength**: Detailed plans, dependencies, roadmaps
- **Weakness**: Can be overly detailed for simple tasks

## Advanced Usage

### Show Agent Information
```bash
python test_cycle.py --info
```

### Run Multiple Test Tasks
```bash
python test_cycle.py --multiple
```

### Check Memory Stats
```python
from lib.memory import MemoryManager

mm = MemoryManager()
print(mm.get_stats())
print(mm.get_recent_outcomes(n=5))
```

### Customize Routing
Edit `lib/router.py` to modify routing logic:
- Add new keywords
- Change routing rules
- Adjust escalation thresholds

### Customize Selection
Edit `lib/selector.py` to modify scoring:
- Change criterion weights
- Add new scoring criteria
- Adjust selection algorithm

## Extending the System

### Add a New Agent

1. Create agent definition: `agents/new_agent.md`
2. Add simulation in `run_task.py`: `_simulate_new_agent()`
3. Update router in `lib/router.py` to route to new agent

### Add Custom Memory Types

1. Add new fields to memory files
2. Extend `MemoryManager` class with new methods
3. Update Overseer to use new memory features

### Connect Real Claude Code Threads

Replace simulated agents in `run_task.py._run_agent()` with:
1. Load agent definition from `.md` file
2. Invoke Claude Code with that prompt
3. Parse and return actual response

## Implementation Notes

### Current State (MVP)

✅ Full architecture implemented
✅ Memory system working
✅ Routing logic functional
✅ Evolutionary selection operational
✅ Agent definitions complete
✅ Simulated agent responses

### Future Enhancements

- [ ] Connect to actual Claude Code threads (replace simulations)
- [ ] Add agent learning from past mistakes
- [ ] Implement reflection cycles
- [ ] Add more sophisticated routing (ML-based)
- [ ] Create web UI for interaction
- [ ] Add multi-turn conversations
- [ ] Implement agent specialization over time

## Design Philosophy

**No External Frameworks**: Built using only Python stdlib and local files. No Letta, AutoGen, crewAI, or LangGraph.

**Transparent**: All logic is visible and hackable. Agent definitions are markdown files. Memory is JSON/markdown.

**Minimal**: ~500 lines of Python + agent definitions. Easy to understand and modify.

**Extensible**: Clean abstractions make it easy to add new agents, memory types, or routing logic.

## Testing

```bash
# Initialize with demo data
python init_memory.py --reset --demo

# Run single demo
python test_cycle.py

# Run multiple tests
python test_cycle.py --multiple

# Run custom task
python run_task.py "Design a recommendation system"
```

## Memory Inspection

```bash
# View outcomes
cat memory/outcomes.json | python -m json.tool

# View knowledge
cat memory/knowledge.json | python -m json.tool

# View reasoning trace
cat memory/system_log.md

# View current context
cat memory/context_window.md
```

## Troubleshooting

**Issue**: `ModuleNotFoundError`
- **Fix**: Make sure you're running from project root

**Issue**: Memory files not found
- **Fix**: Run `python init_memory.py` first

**Issue**: No agents selected
- **Fix**: Check routing logic in `lib/router.py`

## License

MIT - Feel free to use, modify, and extend!

## Credits

Built as a demonstration of System-1/System-2 cognitive architecture inspired by:
- Daniel Kahneman's "Thinking, Fast and Slow"
- Multi-agent systems research
- Evolutionary selection algorithms
- Claude Code's agent capabilities

---

**Ready to build an agentic swarm inside Claude Code? Start with:**
```bash
python init_memory.py --demo
python test_cycle.py
```
