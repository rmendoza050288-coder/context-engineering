#!/usr/bin/env python3
"""
Context Engineering Assistant
A tkinter GUI app to generate AI agent context through a structured wizard interface.
Supports Beginner, Intermediate, and Expert skill levels.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

try:
    import tiktoken
    _encoder = tiktoken.encoding_for_model("gpt-4o")
    def count_tokens(text: str) -> int:
        return len(_encoder.encode(text))
except ImportError:
    def count_tokens(text: str) -> int:
        return max(1, len(text) // 4)  # rough approximation


# ---------------------------------------------------------------------------
# Page definitions per skill level
# Each entry: (field_name, field_type, helper_text)
# field_type is "text" (single line) or "textarea" (multi-line)
# ---------------------------------------------------------------------------

def beginner_pages() -> list:
    """Simplified pages with plain-English explanations and fewer fields."""
    return [
        {
            "title": "What Do You Want the AI To Do?",
            "description": (
                "Think of this like giving instructions to a very smart assistant "
                "who has never worked with you before. The clearer you are, the "
                "better the result."
            ),
            "fields": [
                ("What should the AI build or do?", "textarea",
                 "Describe the task in plain language. Example: 'Build me a website "
                 "that shows the weather for my city.'"),
                ("How will you know it worked?", "textarea",
                 "What does 'done' look like? Example: 'I can open the page and see "
                 "today's temperature.'"),
            ],
        },
        {
            "title": "Background & What You Have So Far",
            "description": (
                "Help the AI understand what already exists so it doesn't start "
                "from scratch or break something."
            ),
            "fields": [
                ("What already exists?", "textarea",
                 "Describe any files, code, or tools you already have. "
                 "Example: 'I have a Python script called app.py that runs a web server.'"),
                ("Anything the AI should know?", "textarea",
                 "Special rules, preferences, or things to avoid. "
                 "Example: 'Don't use JavaScript frameworks — keep it simple HTML.'"),
            ],
        },
        {
            "title": "How Should the AI Behave?",
            "description": (
                "Tell the AI what kind of helper it should be. Think of it like "
                "telling a new coworker how you like to work."
            ),
            "fields": [
                ("What role should the AI play?", "text",
                 "Example: 'A friendly tutor', 'A senior developer', 'A code reviewer'"),
                ("How should it talk to you?", "text",
                 "Example: 'Keep it simple, no jargon' or 'Be technical and detailed'"),
                ("Who is this for?", "text",
                 "Who will use the final result? Example: 'Me', 'My team', 'Customers'"),
            ],
        },
        {
            "title": "What Goes In and What Comes Out?",
            "description": (
                "The AI needs to know what you're giving it to work with and "
                "what the final product should look like."
            ),
            "fields": [
                ("What are you giving the AI to work with?", "textarea",
                 "Files, data, examples, etc. Example: 'A CSV file with customer names and emails.'"),
                ("What should the final result look like?", "textarea",
                 "Describe the format. Example: 'A Python script that I can run from the terminal.'"),
                ("Python - terminal free command option", "checkbox",
                 "Check this if you want a Python solution that can be run without a terminal (e.g., double-click to run)."),
            ],
        },
        {
            "title": "Steps and Priorities",
            "description": (
                "Break the work into steps if you can. If not, just describe "
                "what matters most — the AI will figure out the steps."
            ),
            "fields": [
                ("What steps should the AI follow?", "textarea",
                 "Numbered list if possible. Example:\n"
                 "1. Read the CSV file\n2. Clean up the data\n3. Save results to a new file"),
                ("What matters most?", "textarea",
                 "What's the #1 priority? Example: 'Accuracy over speed' or "
                 "'Get it working first, optimize later'"),
            ],
        },
        {
            "title": "Anything Else?",
            "description": (
                "Last chance to add anything the AI should know. No detail is "
                "too small — the more it knows, the better it performs."
            ),
            "fields": [
                ("What could go wrong?", "textarea",
                 "Things that might trip up the AI. Example: 'Some rows in the CSV are blank.'"),
                ("Any assumptions to mention?", "textarea",
                 "Example: 'Assume Python 3.10 is installed' or 'Assume the user is on macOS.'"),
                ("Additional notes", "textarea",
                 "Anything else at all! Paste links, references, or extra instructions here."),
            ],
        },
    ]


def intermediate_pages() -> list:
    """Balanced pages — the standard context engineering workflow."""
    return [
        {
            "title": "Task Definition",
            "description": "Define the core objective, how to measure success, and constraints.",
            "fields": [
                ("Primary Objective", "text",
                 "What is the core goal? (single sentence)"),
                ("Success Criteria", "textarea",
                 "How will you know the task is complete? (bullet points)"),
                ("Constraints & Boundaries", "textarea",
                 "What are the limits? (technical, resource, scope)"),
            ],
        },
        {
            "title": "Contextual Information",
            "description": "Share background the AI needs to understand the project.",
            "fields": [
                ("Domain Knowledge", "textarea",
                 "Specialized knowledge needed for this task"),
                ("Background & History", "textarea",
                 "Project history, previous decisions, related work"),
                ("Current State", "textarea",
                 "Existing codebase, known issues, environment details"),
            ],
        },
        {
            "title": "Role & Perspective",
            "description": "Define who the AI should be and who the output is for.",
            "fields": [
                ("Agent Role", "text",
                 "Role for AI (e.g., software engineer, architect, reviewer)"),
                ("Audience", "text",
                 "Who will consume the output? (e.g., developers, end users)"),
                ("Tone & Style", "textarea",
                 "Tone/approach (formal/conversational, technical depth)"),
            ],
        },
        {
            "title": "Input Specifications",
            "description": "Describe what data the AI will receive.",
            "fields": [
                ("Input Format & Structure", "textarea",
                 "File types, data structure, volume, encoding"),
                ("Examples", "textarea",
                 "Sample input, expected patterns, edge cases"),
                ("Dependencies", "textarea",
                 "Required libraries, tools, APIs, config files"),
            ],
        },
        {
            "title": "Output Specifications",
            "description": "Describe what the AI should produce.",
            "fields": [
                ("Output Format", "text",
                 "File type, structure, naming conventions"),
                ("Output Requirements", "textarea",
                 "Required sections, metadata, documentation, comments"),
                ("Example Output", "textarea",
                 "Show expected output structure"),
            ],
        },
        {
            "title": "Processing Instructions",
            "description": "Tell the AI how to approach the work step by step.",
            "fields": [
                ("Step-by-Step Process", "textarea",
                 "List steps to take (numbered)"),
                ("Decision Rules", "textarea",
                 "How to make choices, priority rankings, fallbacks"),
                ("Quality Checks", "textarea",
                 "Validation steps, common mistakes, testing approach"),
            ],
        },
        {
            "title": "Knowledge & References",
            "description": "Point the AI to useful resources and key concepts.",
            "fields": [
                ("Relevant Files & Locations", "textarea",
                 "Documentation, code directories, config files"),
                ("Key Concepts Summary", "textarea",
                 "Important concepts (concept: explanation format)"),
                ("Related Resources", "textarea",
                 "Links, similar projects, relevant standards"),
            ],
        },
        {
            "title": "Edge Cases & Exceptions",
            "description": "Prepare the AI for things that might go wrong.",
            "fields": [
                ("Edge Cases", "textarea",
                 "Special situations and how to handle them"),
                ("Error Handling", "textarea",
                 "Responses for invalid input, missing data, conflicts"),
                ("Fallback Approaches", "textarea",
                 "Alternative approaches if primary strategy fails"),
            ],
        },
        {
            "title": "Communication & Feedback",
            "description": "Set expectations for how the AI should report progress.",
            "fields": [
                ("Progress Updates", "textarea",
                 "How to communicate progress, frequency, detail level"),
                ("Questions & Clarifications", "textarea",
                 "When/how to ask questions, decision authority"),
                ("Assumptions", "textarea",
                 "List assumptions being made"),
            ],
        },
        {
            "title": "Optimization & Review",
            "description": "Define quality and performance expectations.",
            "fields": [
                ("Performance Considerations", "textarea",
                 "Speed, resource efficiency, scalability"),
                ("Maintainability", "textarea",
                 "Standards, documentation needs, future-proofing"),
                ("Best Practices", "textarea",
                 "Industry standards to follow for this domain"),
            ],
        },
    ]


def expert_pages() -> list:
    """Comprehensive pages for experienced practitioners."""
    return [
        {
            "title": "Task Definition & Scope",
            "description": "Precisely define the objective, deliverables, scope boundaries, and acceptance criteria.",
            "fields": [
                ("Primary Objective", "text",
                 "One-sentence mission statement for this task"),
                ("Detailed Deliverables", "textarea",
                 "Exhaustive list of artifacts to produce (code, docs, tests, configs)"),
                ("Success Criteria & Acceptance Tests", "textarea",
                 "Measurable conditions that MUST be true for sign-off"),
                ("In-Scope Items", "textarea",
                 "Explicitly state what IS included"),
                ("Out-of-Scope Items", "textarea",
                 "Explicitly state what is NOT included to prevent scope creep"),
                ("Priority Ranking", "textarea",
                 "Order deliverables by importance (P0 critical → P3 nice-to-have)"),
            ],
        },
        {
            "title": "Domain & Technical Context",
            "description": "Provide deep domain knowledge so the agent can reason correctly.",
            "fields": [
                ("Domain Knowledge", "textarea",
                 "Industry terminology, business rules, regulatory requirements"),
                ("Technical Stack & Versions", "textarea",
                 "Languages, frameworks, runtimes, and their exact versions"),
                ("Architecture Overview", "textarea",
                 "System components, data flow, service boundaries, deployment topology"),
                ("Codebase Conventions", "textarea",
                 "Naming conventions, directory structure, design patterns in use"),
                ("Background & History", "textarea",
                 "Prior decisions, tech debt, migrations in progress"),
                ("Current State", "textarea",
                 "Working features, known bugs, recent changes, branch state"),
            ],
        },
        {
            "title": "Agent Configuration",
            "description": "Configure the AI agent's identity, behavior, and operational boundaries.",
            "fields": [
                ("Agent Role & Persona", "text",
                 "Precise role (e.g., 'Senior backend engineer specializing in Go concurrency')"),
                ("Behavioral Directives", "textarea",
                 "How the agent should behave (e.g., 'Always write tests first', 'Prefer composition over inheritance')"),
                ("Audience & Stakeholders", "textarea",
                 "Primary and secondary consumers of the output with their skill levels"),
                ("Tone, Style & Voice", "textarea",
                 "Communication style, verbosity level, formality, use of jargon"),
                ("Authority & Autonomy Level", "textarea",
                 "What can the agent decide alone vs. what requires human approval?"),
                ("Tool & Resource Access", "textarea",
                 "Which tools, APIs, databases, or services the agent may use"),
            ],
        },
        {
            "title": "Input Specifications",
            "description": "Define every input the agent will work with.",
            "fields": [
                ("Input Sources & Formats", "textarea",
                 "File types, APIs, databases, streams — with schemas or examples"),
                ("Data Volume & Performance Constraints", "textarea",
                 "Expected row counts, file sizes, throughput, latency budgets"),
                ("Input Validation Rules", "textarea",
                 "How to verify input integrity, schemas, required fields"),
                ("Sample Inputs", "textarea",
                 "Paste representative examples here"),
                ("Dependencies & Prerequisites", "textarea",
                 "Libraries, packages, services, env vars, credentials needed"),
                ("Environment & Runtime", "textarea",
                 "OS, container, CI/CD pipeline, permissions, network access"),
            ],
        },
        {
            "title": "Output Specifications",
            "description": "Define every output the agent must produce — in detail.",
            "fields": [
                ("Output Formats & Schemas", "textarea",
                 "Exact file types, schemas, data structures for each deliverable"),
                ("Output Requirements", "textarea",
                 "Mandatory sections, headers, metadata, documentation, comments"),
                ("Naming & Organization", "textarea",
                 "File naming patterns, directory structure, module organization"),
                ("Code Style Requirements", "textarea",
                 "Linting rules, formatting standards, docstring conventions"),
                ("Sample / Template Output", "textarea",
                 "Paste or describe the ideal output structure"),
                ("Versioning & Compatibility", "textarea",
                 "API versioning, backward compatibility, deprecation strategy"),
            ],
        },
        {
            "title": "Processing & Execution Strategy",
            "description": "Specify HOW the agent should work — algorithms, order of operations, decision logic.",
            "fields": [
                ("Step-by-Step Process", "textarea",
                 "Numbered execution plan with rationale for each step"),
                ("Decision Rules & Branching Logic", "textarea",
                 "If/then rules, thresholds, priority rankings, tie-breakers"),
                ("Algorithm & Approach Preferences", "textarea",
                 "Preferred algorithms, design patterns, or architectural approaches"),
                ("Concurrency & Ordering", "textarea",
                 "What can run in parallel vs. what must be sequential"),
                ("Quality Gates & Checkpoints", "textarea",
                 "Validation at each stage — tests to run, assertions to check"),
                ("Rollback & Recovery", "textarea",
                 "How to undo partial work if a step fails"),
            ],
        },
        {
            "title": "Knowledge Base & References",
            "description": "Point the agent to every resource it might need.",
            "fields": [
                ("Key Files & Directories", "textarea",
                 "Critical file paths with brief descriptions of their purpose"),
                ("API Documentation", "textarea",
                 "Endpoints, auth methods, rate limits, response schemas"),
                ("Key Concepts & Glossary", "textarea",
                 "Domain terms with precise definitions"),
                ("Related Resources & Links", "textarea",
                 "Docs, RFCs, ADRs, design docs, wiki pages, Slack threads"),
                ("Code Examples & Patterns", "textarea",
                 "Paste reference implementations or link to exemplary code"),
            ],
        },
        {
            "title": "Edge Cases, Errors & Security",
            "description": "Prepare the agent for failure modes, adversarial inputs, and security concerns.",
            "fields": [
                ("Known Edge Cases", "textarea",
                 "Enumerate edge cases with expected behavior for each"),
                ("Error Handling Strategy", "textarea",
                 "For each error class: detection, logging, user messaging, recovery"),
                ("Fallback & Degraded Modes", "textarea",
                 "How to operate when dependencies fail or data is incomplete"),
                ("Security Requirements", "textarea",
                 "Auth, input sanitization, secrets management, OWASP considerations"),
                ("Data Privacy & Compliance", "textarea",
                 "PII handling, GDPR/HIPAA rules, data retention, audit logging"),
            ],
        },
        {
            "title": "Testing & Validation",
            "description": "Define the testing strategy the agent should follow or produce.",
            "fields": [
                ("Unit Test Requirements", "textarea",
                 "Coverage targets, mocking strategy, assertion patterns"),
                ("Integration & E2E Tests", "textarea",
                 "Test scenarios, environment setup, data fixtures"),
                ("Performance & Load Tests", "textarea",
                 "Benchmarks, SLAs, stress test scenarios"),
                ("Manual Verification Steps", "textarea",
                 "Checklist for human review after agent completes work"),
                ("Known Regressions to Watch", "textarea",
                 "Past bugs that could resurface — specific things to test for"),
            ],
        },
        {
            "title": "Communication & Coordination",
            "description": "Define how the agent should communicate and coordinate with humans or other agents.",
            "fields": [
                ("Progress Reporting", "textarea",
                 "When and how to report status (format, frequency, channel)"),
                ("Escalation Protocol", "textarea",
                 "When to stop and ask a human, thresholds for uncertainty"),
                ("Assumptions & Open Questions", "textarea",
                 "Document every assumption — flag questions needing human input"),
                ("Multi-Agent Coordination", "textarea",
                 "If multiple agents: handoff protocol, shared state, conflict resolution"),
                ("Feedback Loop", "textarea",
                 "How the agent should incorporate corrections and iterate"),
            ],
        },
        {
            "title": "Optimization & Operational Excellence",
            "description": "Define performance, observability, and long-term quality expectations.",
            "fields": [
                ("Performance Targets", "textarea",
                 "Latency, throughput, memory, CPU budgets with specific numbers"),
                ("Observability & Monitoring", "textarea",
                 "Logging, metrics, alerting, tracing requirements"),
                ("Maintainability Standards", "textarea",
                 "Code complexity limits, documentation, review processes"),
                ("Scalability Considerations", "textarea",
                 "Growth projections, horizontal/vertical scaling strategy"),
                ("Best Practices & Standards", "textarea",
                 "Industry standards, internal guidelines, compliance requirements"),
                ("Post-Completion Checklist", "textarea",
                 "Final checks before delivery: linting, security scan, docs, changelog"),
            ],
        },
    ]


# ---------------------------------------------------------------------------
# Skill level metadata
# ---------------------------------------------------------------------------

SKILL_LEVELS = {
    "beginner": {
        "label": "Beginner",
        "emoji": "🟢",
        "tagline": "New to context engineering",
        "description": (
            "Perfect if you're just getting started with AI agents.\n\n"
            "• Plain-English questions — no jargon\n"
            "• Only 6 pages with the essentials\n"
            "• Helpful examples for every field\n\n"
            "The app will walk you through everything you need step by step."
        ),
        "pages_fn": beginner_pages,
    },
    "intermediate": {
        "label": "Intermediate",
        "emoji": "🟡",
        "tagline": "Comfortable with AI tools",
        "description": (
            "The standard context engineering workflow.\n\n"
            "• 10 structured sections covering all key areas\n"
            "• Balanced depth — enough detail without overwhelm\n"
            "• Covers task, context, role, I/O, process, and more\n\n"
            "Good for most projects and teams."
        ),
        "pages_fn": intermediate_pages,
    },
    "expert": {
        "label": "Expert",
        "emoji": "🔴",
        "tagline": "Deep context engineering experience",
        "description": (
            "The comprehensive context package for demanding projects.\n\n"
            "• 11 in-depth sections with 50+ fields total\n"
            "• Covers security, testing, multi-agent coordination\n"
            "• Architecture, performance targets, observability\n"
            "• Scope control, rollback plans, compliance\n\n"
            "Gives the AI agent everything it could ever need."
        ),
        "pages_fn": expert_pages,
    },
}


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class ContextEngineeringApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Context Engineering Assistant")
        self.root.geometry("920x720")
        self.root.minsize(700, 500)

        # State
        self.skill_level: str | None = None
        self.pages: list = []
        self.data: Dict[str, Any] = {}
        self.current_page = 0
        self.page_widgets: Dict[str, tk.Widget] = {}
        self._update_scheduled = False

        # Permanent outer frames
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        # hidden until wizard starts

        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Show the skill-level chooser first
        self._show_skill_selector()

    # ------------------------------------------------------------------
    # Skill-level selector (landing screen)
    # ------------------------------------------------------------------
    def _show_skill_selector(self):
        self._clear_frames()
        self.progress.pack_forget()

        # Title
        ttk.Label(
            self.header_frame,
            text="Context Engineering Assistant",
            font=("Helvetica", 18, "bold"),
        ).pack(side=tk.LEFT)

        # Subtitle
        ttk.Label(
            self.content_frame,
            text="Choose your experience level",
            font=("Helvetica", 14),
        ).pack(pady=(10, 5))

        ttk.Label(
            self.content_frame,
            text="This determines the depth and number of questions you'll answer.",
            foreground="gray",
        ).pack(pady=(0, 20))

        # Cards frame
        cards = ttk.Frame(self.content_frame)
        cards.pack(fill=tk.BOTH, expand=True)

        for idx, (key, info) in enumerate(SKILL_LEVELS.items()):
            card = ttk.LabelFrame(cards, text=f"  {info['emoji']}  {info['label']}  ", padding=15)
            card.grid(row=0, column=idx, padx=12, pady=10, sticky="nsew")

            ttk.Label(card, text=info["tagline"], font=("Helvetica", 11, "bold")).pack(
                anchor=tk.W, pady=(0, 8)
            )
            ttk.Label(card, text=info["description"], wraplength=230, justify=tk.LEFT).pack(
                anchor=tk.W, fill=tk.BOTH, expand=True
            )

            btn = ttk.Button(
                card,
                text=f"Start {info['label']}",
                command=lambda k=key: self._select_skill(k),
            )
            btn.pack(pady=(12, 0))

        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.columnconfigure(2, weight=1)

    def _select_skill(self, level: str):
        self.skill_level = level
        self.pages = SKILL_LEVELS[level]["pages_fn"]()
        self.data = {}
        self.current_page = 0
        self._start_wizard()

    # ------------------------------------------------------------------
    # Wizard UI (pages)
    # ------------------------------------------------------------------
    def _start_wizard(self):
        self._clear_frames()

        # Header
        ttk.Label(
            self.header_frame,
            text="Context Engineering Assistant",
            font=("Helvetica", 16, "bold"),
        ).pack(side=tk.LEFT)

        level_info = SKILL_LEVELS[self.skill_level]
        self.level_label = ttk.Label(
            self.header_frame,
            text=f"{level_info['emoji']} {level_info['label']}",
            font=("Helvetica", 10),
        )
        self.level_label.pack(side=tk.LEFT, padx=(12, 0))

        self.progress_label = ttk.Label(self.header_frame, text="")
        self.progress_label.pack(side=tk.RIGHT)

        self.token_label = ttk.Label(
            self.header_frame,
            text="Tokens: 0",
            font=("Helvetica", 10),
            foreground="#555",
        )
        self.token_label.pack(side=tk.RIGHT, padx=(0, 16))

        self.progress.pack(fill=tk.X, padx=10, pady=5, before=self.content_frame)

        # Nav buttons
        self.prev_btn = ttk.Button(self.nav_frame, text="← Previous", command=self._prev_page)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(self.nav_frame, text="Next →", command=self._next_page)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.change_level_btn = ttk.Button(
            self.nav_frame, text="Change Level", command=self._confirm_change_level
        )
        self.change_level_btn.pack(side=tk.LEFT, padx=(20, 5))

        self.generate_btn = ttk.Button(
            self.nav_frame, text="Generate Files", command=self._generate_files, state=tk.DISABLED
        )
        self.generate_btn.pack(side=tk.RIGHT, padx=5)

        self._load_page()

    def _confirm_change_level(self):
        if any(self.data.values()):
            ok = messagebox.askyesno(
                "Change Level",
                "Changing the level will clear all your answers.\n\nContinue?",
            )
            if not ok:
                return
        self.data = {}
        self.current_page = 0
        self._show_skill_selector()

    # ------------------------------------------------------------------
    # Page rendering
    # ------------------------------------------------------------------
    def _load_page(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        page = self.pages[self.current_page]

        # Page title
        ttk.Label(
            self.content_frame, text=page["title"], font=("Helvetica", 14, "bold")
        ).pack(anchor=tk.W, pady=(0, 3))

        # Page description
        if page.get("description"):
            ttk.Label(
                self.content_frame,
                text=page["description"],
                wraplength=850,
                foreground="gray",
                font=("Helvetica", 10),
            ).pack(anchor=tk.W, pady=(0, 12))

        # Scrollable area
        canvas = tk.Canvas(self.content_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse-wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.page_widgets = {}
        for field_name, field_type, helper in page["fields"]:
            frame = ttk.Frame(inner)
            frame.pack(fill=tk.X, pady=(0, 14), anchor=tk.W)

            ttk.Label(frame, text=field_name, font=("Helvetica", 10, "bold")).pack(
                anchor=tk.W, pady=(0, 4)
            )

            if field_type == "checkbox":
                var = tk.BooleanVar(value=self.data.get(field_name, False))
                cb = ttk.Checkbutton(frame, text=field_name, variable=var)
                cb.pack(anchor=tk.W)
                var.trace_add("write", lambda *_: self._schedule_token_update())
                self.page_widgets[field_name] = var
            elif field_type == "text":
                entry = ttk.Entry(frame, width=90)
                entry.pack(anchor=tk.W, fill=tk.X)
                entry.insert(0, self.data.get(field_name, ""))
                entry.bind("<KeyRelease>", lambda e: self._schedule_token_update())
                self.page_widgets[field_name] = entry
            else:
                text = scrolledtext.ScrolledText(frame, height=5, width=90, wrap=tk.WORD)
                text.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
                text.insert(tk.END, self.data.get(field_name, ""))
                text.bind("<KeyRelease>", lambda e: self._schedule_token_update())
                self.page_widgets[field_name] = text

            ttk.Label(frame, text=helper, foreground="gray", font=("Helvetica", 9),
                      wraplength=830).pack(anchor=tk.W, pady=(3, 0))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Progress
        total = len(self.pages)
        self.progress["value"] = ((self.current_page + 1) / total) * 100
        self.progress_label.config(text=f"Page {self.current_page + 1} of {total}")

        self.prev_btn.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_page < total - 1 else tk.DISABLED)
        self.generate_btn.config(
            state=tk.NORMAL if self.current_page == total - 1 else tk.DISABLED
        )

        self._update_token_count()

    # ------------------------------------------------------------------
    # Token estimation
    # ------------------------------------------------------------------
    def _schedule_token_update(self):
        """Debounce token updates to avoid lag on every keystroke."""
        if not self._update_scheduled:
            self._update_scheduled = True
            self.root.after(300, self._do_token_update)

    def _do_token_update(self):
        self._update_scheduled = False
        self._update_token_count()

    def _update_token_count(self):
        """Recalculate token estimate from saved data + live widgets."""
        # Merge saved data with current page's live widget values
        merged = dict(self.data)
        for field_name, widget in self.page_widgets.items():
            if isinstance(widget, tk.BooleanVar):
                merged[field_name] = widget.get()
            elif isinstance(widget, tk.Text):
                merged[field_name] = widget.get(1.0, tk.END).strip()
            else:
                merged[field_name] = widget.get().strip()

        # Build the text that would be sent to the AI (mirrors _generate_markdown)
        parts: list[str] = []
        for page in self.pages:
            for field_name, _, _ in page["fields"]:
                value = merged.get(field_name, "")
                if value and value is not True:
                    parts.append(f"{field_name}\n{value}")
                elif value is True:
                    parts.append(field_name)

        full_text = "\n\n".join(parts)
        tokens = count_tokens(full_text) if full_text else 0

        # Color-code: green < 4k, orange 4k-8k, red > 8k
        if tokens < 4000:
            color = "#2e7d32"  # green
        elif tokens < 8000:
            color = "#e65100"  # orange
        else:
            color = "#c62828"  # red

        self.token_label.config(text=f"~{tokens:,} tokens", foreground=color)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def _save_page(self):
        for field_name, widget in self.page_widgets.items():
            if isinstance(widget, tk.BooleanVar):
                self.data[field_name] = widget.get()
            elif isinstance(widget, tk.Text):
                self.data[field_name] = widget.get(1.0, tk.END).strip()
            else:
                self.data[field_name] = widget.get().strip()

    def _next_page(self):
        self._save_page()
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self._load_page()

    def _prev_page(self):
        self._save_page()
        if self.current_page > 0:
            self.current_page -= 1
            self._load_page()

    # ------------------------------------------------------------------
    # File generation
    # ------------------------------------------------------------------
    def _generate_files(self):
        self._save_page()

        if not any(self.data.values()):
            messagebox.showwarning("Empty Context", "Please fill in at least some fields.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialfile=f"context_{self.skill_level}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        )
        if not file_path:
            return

        file_path = Path(file_path)

        md_file = file_path.with_suffix(".md")
        md_file.write_text(self._generate_markdown(), encoding="utf-8")

        json_file = file_path.with_suffix(".json")
        json_file.write_text(self._generate_json(), encoding="utf-8")

        messagebox.showinfo(
            "Success",
            f"Files generated!\n\nMarkdown: {md_file}\nJSON: {json_file}",
        )

    def _generate_markdown(self) -> str:
        level_info = SKILL_LEVELS[self.skill_level]
        lines = [
            "# AI Agent Context\n",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  ",
            f"*Level: {level_info['label']}*\n",
        ]

        for page in self.pages:
            section = page["title"]
            fields = page["fields"]
            has_content = any(self.data.get(f, "") or self.data.get(f) is True for f, _, _ in fields)
            if not has_content:
                continue

            lines.append(f"\n## {section}\n")
            for field_name, _, _ in fields:
                value = self.data.get(field_name, "")
                if value:
                    if isinstance(value, bool):
                        lines.append(f"### {field_name}\n")
                        lines.append(f"{'Yes' if value else 'No'}\n")
                    else:
                        lines.append(f"### {field_name}\n")
                        lines.append(f"{value}\n")

        return "\n".join(lines)

    def _generate_json(self) -> str:
        level_info = SKILL_LEVELS[self.skill_level]
        output: Dict[str, Any] = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "version": "1.0",
                "skill_level": self.skill_level,
            },
            "sections": {},
        }

        for page in self.pages:
            section_key = page["title"].lower().replace(" & ", "_and_").replace(" ", "_")
            section_data = {}
            for field_name, _, _ in page["fields"]:
                value = self.data.get(field_name, "")
                if value or value is True:
                    key = field_name.lower().replace(" & ", "_and_").replace("?", "").replace(" ", "_").strip("_")
                    section_data[key] = value
            if section_data:
                output["sections"][section_key] = section_data

        return json.dumps(output, indent=2)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _clear_frames(self):
        for frame in (self.header_frame, self.content_frame, self.nav_frame):
            for w in frame.winfo_children():
                w.destroy()


def main():
    root = tk.Tk()
    app = ContextEngineeringApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
