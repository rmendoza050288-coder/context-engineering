# Context Engineering Assistant

A Python desktop application that guides you through creating comprehensive AI agent context documents.

## Overview

This app walks you through a 10-step wizard to collect information for your AI agent context. At the end, it generates both **Markdown** and **JSON** formatted files ready for AI consumption.

## Features

- **Multi-page wizard interface** - 10 structured sections
- **Progress tracking** - Visual progress bar and page counter
- **Dual output formats** - Generates both `.md` (readable) and `.json` (structured) files
- **Persistent input** - Your data is saved as you navigate pages
- **Scrollable forms** - Handles many fields gracefully
- **Easy export** - Choose where to save your generated files

## Quick Start

### Option 1: Run directly with Python

```bash
python3 context_engineering_app.py
```

### Option 2: Run with launcher script

```bash
chmod +x run_context_app.sh
./run_context_app.sh
```

## Pages/Sections

1. **Task Definition** - Core goal, success criteria, constraints
2. **Contextual Information** - Domain knowledge, background, current state
3. **Role & Perspective** - Agent role, audience, tone
4. **Input Specifications** - Input format, examples, dependencies
5. **Output Specifications** - Output format, requirements, examples
6. **Processing Instructions** - Steps, decision rules, quality checks
7. **Knowledge & References** - Files, concepts, resources
8. **Edge Cases & Exceptions** - Edge cases, error handling, fallbacks
9. **Communication & Feedback** - Updates, questions, assumptions
10. **Optimization & Review** - Performance, maintainability, best practices

## Output Format Examples

### Markdown Output
Clean, readable documentation format:
```markdown
# AI Agent Context

## Task Definition

### Primary Objective
Build a web scraper that...

### Success Criteria
- Handles 1000+ pages...
```

### JSON Output
Structured format for programmatic use:
```json
{
  "metadata": {
    "generated": "2026-04-07T10:30:00",
    "version": "1.0"
  },
  "sections": {
    "task_definition": {
      "primary_objective": "...",
      "success_criteria": "..."
    }
  }
}
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)

## Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"
On Linux, install tkinter:
```bash
sudo apt-get install python3-tk
```

### App doesn't open
Make sure you're using Python 3:
```bash
python3 context_engineering_app.py
```

## Usage Tips

1. **Fill in as much as relevant** - You don't need to fill every field
2. **Use descriptions as guides** - Each field has helper text
3. **Scroll within pages** - If there are many fields, scroll to see all
4. **Go back and edit** - Use Previous/Next to revise previous answers
5. **Generate when ready** - Only appears on the last page

## Generated Files

Your context files will be named with timestamps:
- `context_20260407_103000.md` - Readable markdown format
- `context_20260407_103000.json` - Machine-readable JSON format

Use these files to:
- Pass to AI agents/models
- Share with team members
- Version control in your project
- Feed into automated workflows

## File Locations

- Main app: `context_engineering_app.py`
- Template reference: `CONTEXT_ENGINEERING_TEMPLATE.md`
- This guide: `CONTEXT_APP_README.md`
