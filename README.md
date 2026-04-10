# Context Engineering Assistant

A Python desktop application that guides you through creating comprehensive AI agent context documents using a structured wizard interface.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

Context Engineering Assistant walks you through a structured wizard to collect the information AI agents need to perform at their best. It supports three skill levels — **Beginner**, **Intermediate**, and **Expert** — and generates both Markdown and JSON output files ready for AI consumption.

## Features

- **Three skill levels** — Beginner (6 pages), Intermediate (10 pages), Expert (11 pages with 50+ fields)
- **Multi-page wizard interface** with progress tracking
- **Dual output formats** — generates `.md` (human-readable) and `.json` (structured) files
- **Persistent input** — your data is saved as you navigate between pages
- **Scrollable forms** — handles many fields gracefully
- **No external dependencies** — uses only Python standard library (tkinter)

## Quick Start

### Option 1: Run directly with Python

```bash
python3 context_engineering_app.py
```

### Option 2: Use the launcher script

```bash
chmod +x run_context_app.sh
./run_context_app.sh
```

### Option 3: Double-click (macOS)

Double-click `Run Context App.command` in Finder.

## Skill Levels

| Level | Pages | Fields | Best For |
|-------|-------|--------|----------|
| 🟢 Beginner | 6 | ~14 | New to context engineering — plain-English questions with examples |
| 🟡 Intermediate | 10 | ~30 | Standard workflow — balanced depth covering all key areas |
| 🔴 Expert | 11 | 50+ | Demanding projects — security, testing, multi-agent coordination |

## Wizard Sections (Intermediate)

1. **Task Definition** — Core goal, success criteria, constraints
2. **Contextual Information** — Domain knowledge, background, current state
3. **Role & Perspective** — Agent role, audience, tone
4. **Input Specifications** — Input format, examples, dependencies
5. **Output Specifications** — Output format, requirements, examples
6. **Processing Instructions** — Steps, decision rules, quality checks
7. **Knowledge & References** — Files, concepts, resources
8. **Edge Cases & Exceptions** — Edge cases, error handling, fallbacks
9. **Communication & Feedback** — Updates, questions, assumptions
10. **Optimization & Review** — Performance, maintainability, best practices

## Output Examples

### Markdown

```markdown
# AI Agent Context

*Generated: 2026-04-10 14:30:00*
*Level: Intermediate*

## Task Definition

### Primary Objective
Build a web scraper that collects product prices daily.

### Success Criteria
- Handles 1000+ pages without errors
- Runs in under 5 minutes
```

### JSON

```json
{
  "metadata": {
    "generated": "2026-04-10T14:30:00",
    "version": "1.0",
    "skill_level": "intermediate"
  },
  "sections": {
    "task_definition": {
      "primary_objective": "Build a web scraper...",
      "success_criteria": "- Handles 1000+ pages..."
    }
  }
}
```

## Requirements

- **Python 3.7+**
- **tkinter** (included with most Python installations)

### Troubleshooting

If tkinter is not installed (Linux):

```bash
sudo apt-get install python3-tk
```

## Project Structure

```
├── context_engineering_app.py      # Main application
├── CONTEXT_ENGINEERING_TEMPLATE.md # Reference template for context engineering
├── CONTEXT_APP_README.md           # Detailed app documentation
├── run_context_app.sh              # Shell launcher script
├── Run Context App.command         # macOS double-click launcher
└── README.md                       # This file
```

## Template

The included [CONTEXT_ENGINEERING_TEMPLATE.md](CONTEXT_ENGINEERING_TEMPLATE.md) is a standalone reference framework you can use manually (without the app) to structure context for AI agents.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
