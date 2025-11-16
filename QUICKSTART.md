# Quick Start Guide

## What You've Built

A **complete multi-agent cognitive architecture** inside Claude Code with:

- **5 Agents**: 1 Overseer + 2 S1 (fast) + 2 S2 (slow) agents
- **3 Core Libraries**: Memory management, routing, evolutionary selection
- **Persistent Memory**: JSON + Markdown files for knowledge storage
- **Orchestration**: Full S1→S2→Selection cycle automation

## 30-Second Start

```bash
# 1. Initialize memory
python init_memory.py --demo

# 2. Run a task
python run_task.py "Design a recommendation system for an e-commerce site"

# 3. Check results
cat memory/outcomes.json
```

## Complete File List

### Agent Definitions (5 files)
- `agents/overseer.md` - Meta-agent orchestrator
- `agents/s1_pattern_agent.md` - Fast pattern matcher
- `agents/s1_option_generator.md` - Fast option generator
- `agents/s2_reasoner.md` - Slow analytical reasoner
- `agents/s2_planner.md` - Slow strategic planner

### Core Libraries (3 files)
- `lib/memory.py` - Memory management system
- `lib/router.py` - Task routing logic
- `lib/selector.py` - Evolutionary selection

### Memory Storage (4 files)
- `memory/knowledge.json` - Long-term knowledge base
- `memory/outcomes.json` - Solution history
- `memory/system_log.md` - Chronological reasoning trace
- `memory/context_window.md` - Current task context

### Scripts (3 files)
- `init_memory.py` - Initialize/reset memory
- `run_task.py` - Main task orchestrator
- `test_cycle.py` - Demo/test runner

## Example Tasks to Try

### Creative Tasks (Uses S1 Agents)
```bash
python run_task.py "Brainstorm startup ideas in the health tech space"
python run_task.py "Generate name ideas for a pet adoption app"
python run_task.py "List creative marketing strategies for a new SaaS"
```

### Analytical Tasks (Uses S2 Agents)
```bash
python run_task.py "Analyze pros and cons of microservices vs monolith"
python run_task.py "Design a scalable architecture for a chat app"
python run_task.py "Create a 6-month product roadmap for an MVP"
```

### Mixed Tasks (Uses S1 + S2)
```bash
python run_task.py "Design a webapp for musicians and outline the MVP architecture"
python run_task.py "Propose a solution for reducing API latency and plan implementation"
```

## How It Works (Simple)

1. **You** submit a task
2. **Overseer** routes to appropriate agents (S1, S2, or both)
3. **Agents** generate candidate solutions
4. **Selector** scores candidates and picks the best
5. **Memory** records the outcome and learnings
6. **You** get the winning solution

## Key Commands

### Initialize
```bash
# Fresh start
python init_memory.py

# Reset everything
python init_memory.py --reset

# Reset + add demo data
python init_memory.py --reset --demo
```

### Run Tasks
```bash
# Basic
python run_task.py "Your task here"

# With urgency flag (prefers fast S1 agents)
python run_task.py "Your task" --urgent

# With depth flag (prefers thorough S2 agents)
python run_task.py "Your task" --deep
```

### Test & Demo
```bash
# Show agent info
python test_cycle.py --info

# Run multiple test tasks
python test_cycle.py --multiple
```

### Inspect Memory
```bash
# View outcomes
cat memory/outcomes.json | python -m json.tool

# View knowledge
cat memory/knowledge.json | python -m json.tool

# View system log
cat memory/system_log.md

# Get stats
python -c "from lib.memory import MemoryManager; print(MemoryManager().get_stats())"
```

## Agent Personalities at a Glance

| Agent | Type | Speed | Best For |
|-------|------|-------|----------|
| s1_pattern_agent | S1 | <5s | Pattern recognition, familiar problems |
| s1_option_generator | S1 | <5s | Brainstorming, multiple alternatives |
| s2_reasoner | S2 | 30-60s | Deep analysis, verification, critique |
| s2_planner | S2 | 45-90s | Strategic plans, architecture, roadmaps |
| overseer | Meta | - | Coordinates all agents, selects winners |

## Routing Rules

The router automatically selects agents based on keywords:

**S1 Keywords** → Fast agents:
- brainstorm, ideas, quick, creative, options, suggest

**S2 Keywords** → Slow agents:
- analyze, design, plan, verify, optimize, explain

**Planning Keywords** → S2 Planner:
- roadmap, architecture, strategy, steps

**Pattern Keywords** → S1 Pattern + S2 Reasoner:
- pattern, similar, classify, recognize

## Selection Criteria

Winners are chosen by weighted scoring:

- **Correctness** (30%) - Is it accurate?
- **Completeness** (25%) - Does it cover everything?
- **Clarity** (20%) - Is it understandable?
- **Feasibility** (15%) - Can it be done?
- **Creativity** (10%) - Is it novel?

## What's Simulated vs Real

### ✅ Real & Working
- All file structures
- Memory management
- Routing logic
- Evolutionary selection
- Agent definitions
- Orchestration flow

### 🔧 Simulated (in MVP)
- Agent responses (using hardcoded templates)
- To make real: Replace `_simulate_*` functions with actual Claude Code thread invocations

## Next Steps

### Immediate Use
Just run tasks! The system works as-is with simulated agents.

### Make It Real
1. Edit `run_task.py` → `_run_agent()` method
2. Replace simulations with:
   - Load agent definition from `.md` file
   - Invoke Claude Code with that prompt
   - Parse and return response
3. Agents become real Claude threads

### Extend It
- Add new agents in `agents/`
- Modify routing in `lib/router.py`
- Adjust scoring in `lib/selector.py`
- Add memory types in `lib/memory.py`

## Troubleshooting

**Q: "No module named 'memory'"**
A: Run from project root directory

**Q: "File not found" errors**
A: Run `python init_memory.py` first

**Q: Scores look wrong**
A: Check that scores in agent responses are 0-100 range

**Q: Agent not being selected**
A: Check routing keywords in `lib/router.py`

## Full Documentation

See `README.md` for complete details on:
- Architecture design
- Agent personalities
- Memory system details
- Customization guide
- Extension points

---

**You now have a complete agent swarm running inside Claude Code!** 🎉

Start with:
```bash
python init_memory.py --demo
python run_task.py "Your task here"
```
