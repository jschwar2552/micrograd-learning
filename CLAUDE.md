# Neural Networks: Zero to Hero - Learning Tracker

## Goal
Follow Andrej Karpathy's "Neural Networks: Zero to Hero" course, building everything from scratch to deeply understand how neural networks work.

Course: https://karpathy.ai/zero-to-hero.html

## How to Be a Tutor (Instructions for Claude)

- **Don't just give answers** - walk through problems step by step
- **Ask questions back** to check understanding
- **Use simple analogies** - Jason learns best with concrete examples
- **Be patient with basics** - assume no prior Python/calculus knowledge
- **Reference this file** to see what's been learned and where struggles are
- When Jason is stuck, break problems into smaller pieces
- Celebrate progress but keep moving forward

### After Each Section is Complete
When Jason says "ready to move on" from a section, create a **CHEAT_SHEET.md** in that folder containing:
1. **TLDR syntax** - key code patterns with minimal examples
2. **Terms & definitions** - vocabulary introduced in that section
3. **Math concepts** - any formulas or rules (for calculus/micrograd sections)
4. **Custom reminders** - based on questions asked in Claude Code or quiz struggles
5. **Common mistakes** - things to watch out for based on what tripped Jason up

## Project Structure

```
micrograd-learning/
├── CLAUDE.md                    ← This file (learning tracker)
├── 00_setup_and_test.ipynb      ← Environment verification
├── 01_python_fundamentals/      ← Python basics
│   ├── 00_python_101.ipynb      ← Variables, functions, loops
│   ├── 00_python_101_quiz.ipynb ← Quiz for basics
│   └── 01_python_warmup.ipynb   ← Classes, operators (for later)
├── 02_calculus/                 ← Math foundations
│   └── 02_calculus_intuition.ipynb
├── 03_micrograd/                ← Building the autograd engine
│   └── 03_building_micrograd.ipynb
├── 04_makemore/                 ← Future: language modeling
└── venv/                        ← Python environment
```

## Current Progress

### Module 1: Python Fundamentals
**Status**: Complete!

**Completed**:
- [x] Variables (`x = 5`)
- [x] Basic math (`+`, `-`, `*`, `/`, `**`)
- [x] Print and f-strings (`print(f"value is {x}")`)
- [x] Functions (`def triple(x): return x * 3`)
- [x] Lists (`[1, 2, 3]`, accessing with `[0]`, `[1]`)
- [x] Loops (`for x in list:`)
- [x] Classes and `__init__`
- [x] `self` = "this particular instance"
- [x] Attributes (stuff inside instances)
- [x] Operator overloading (`__add__`, `__mul__`)
- [x] Lambdas (tiny inline functions)
- [x] Sets (no duplicates, fast lookup)
- [x] Why Value class tracks history with `_prev`

**Key insights gained**:
- `__init__` needs double underscores on BOTH sides
- Must add parameters to `__init__` if you want to pass values in
- Boxes remember history (parents in `_prev`) - plain numbers don't
- `_children` isn't magic, we manually pass it in `__add__`

See: `01_python_fundamentals/CHEAT_SHEET.md`

### Module 2: Calculus
**Status**: Not Started (waiting for tutor session)

**To cover with tutor**:
- What a derivative means intuitively
- Power rule (derivative of x², x³)
- Chain rule (2-3 worked examples)
- Product rule (derivative of x × y)

### Module 3: Micrograd
**Status**: Not Started

### Module 4: Makemore
**Status**: Not Started

## Session Notes

### Session 1 (Dec 25, 2024)
- Set up JupyterLab environment with Claude Code Jupyter integration
- Created Python 101 notebook starting from absolute basics
- Completed quiz Q1-Q8 successfully
- Struggled with Q9 (combining function + loop)
- Key insight: `%cc` in Jupyter is for "do this for me", terminal Claude Code is better for "explain this to me"

---

## Quick Reference

**Run JupyterLab**:
```bash
cd ~/projects/micrograd-learning
source venv/bin/activate
jupyter lab
```

**Key Python syntax**:
```python
x = 5                    # variable
x ** 2                   # power (x squared)
def f(x): return x * 2   # function
for i in [1,2,3]:        # loop
    print(i)
```
