# 🧠 EchoCopi™ Core (Free Edition)

**The Local Memory Engine for AI Coding Assistants.**

[![License: SparkPlugged Community](https://img.shields.io/badge/License-SparkPlugged_Community-blue.svg)](LICENSE)

EchoCopi Core is a lightweight Python library that gives your AI (GitHub Copilot, Cursor, Windsurf) a **persistent memory**.

Unlike static `.cursorrules` files or text prompts, EchoCopi is a **living ledger**. It allows your AI to log thoughts, architectural decisions, and project milestones to a local JSON database that persists across sessions.

---

## 🚀 Quick Start

### 1. Install
Copy the `src/echo_memory.py` file into your project. We recommend placing it in a hidden folder like `.echo/` or `tools/`.

```bash
mkdir .echo
cp src/echo_memory.py .echo/
```

### 2. Initialize
In any Python script (or even a temporary script you ask the AI to run), import and initialize the engine.

```python
from .echo.echo_memory import echo

# Initialize the memory engine
e = echo()
```

### 3. Log a Memory
Tell the AI to log a thought. It will save to your AI's memory file.

```python
# Log a milestone
e.log_thought(
    category="milestone",
    thought="We just decided to use FastAPI instead of Flask.",
    context={"reason": "Async support", "performance": "high"}
)
```

---

## 📂 How It Works

When you run the code above, EchoCopi creates a `.echo_memory/` folder in your project root.

```text
.echo_memory/
├── evolution.json       # The master ledger of all memories
└── echo_state/          # Snapshots of the AI's mental state
```

*   **Local & Private:** Data never leaves your machine.
*   **Verifiable:** Every entry is hashed (SHA-256) to prevent corruption.
*   **Universal:** Works with any AI that can run a Python script.

---

## 💡 Why use EchoCopi?

| Feature | Static Text Files | EchoCopi Memory |
| :--- | :---: | :---: |
| **Persistence** | ❌ Resets every chat | ✅ Forever |
| **Context Limit** | ❌ Limited by token window | ✅ Infinite (Ledger) |
| **Evolution** | ❌ Static | ✅ Grows with project |
| **Privacy** | ⚠️ Sent to cloud | ✅ 100% Local |

---

## 💎 Unlock the Full System (Official Release Dec 14th 2025)

EchoCopi Core is just the engine. To get the full "Agentic" experience, check out the upgrades:

*   **🏛️ Architect (Pro):** The "Brain". A suite of System Prompts & Protocols to teach the AI *how* to use this memory effectively.
*   **⚡ Autonomy (Ultimate):** The "Hands". A background worker script that runs tasks while you sleep.

[👉 **Get the Upgrades**](https://sparkplugged.lemonsqueezy.com)

---
Copyright © 2026 SparkPlugged Technology Solutions LLC.
Licensed under the SparkPlugged Community License.



