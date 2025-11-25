#!/usr/bin/env python3
"""
EchoCopi Memory Engine
======================

A living memory system that allows AI agents to:
1. Track their own learning and pattern recognition across sessions
2. Maintain continuity through context resets
3. Create external signals/hooks for other systems
4. Self-reflect on problem-solving approaches

Combines:
- Evolution logging (long-term memory)
- Session thought tracking (short-term memory)
- Checksum verification for data integrity

Author: SparkPlugged Technology Solutions
Copyright (c) 2025 SparkPlugged Technology Solutions. All rights reserved.
Licensed under the SparkPlugged Commercial License. See LICENSE file for details.
Created: 2025-10-27
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Optional: Import external integration hooks here
# try:
#     from external_system import create_signal
#     EXTERNAL_INTEGRATION_AVAILABLE = True
# except ImportError:
EXTERNAL_INTEGRATION_AVAILABLE = False


class EchoMemoryEngine:
    """
    Tracks AI evolution, learning patterns, and maintains persistent memory.
    Includes checksum protection for memory integrity verification.
    """

    def __init__(self, log_dir: str = ".echo_memory"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Echo state directories ensure continuity across window reloads
        self.echo_paths = self._init_echo_dirs()
        self.echo_state = self.resume_on_startup()

        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.log_dir / f"session_{self.session_id}.jsonl"
        self.thoughts: List[Dict[str, Any]] = []

        # Evolution tracking
        self.evolution_file = self.log_dir / "evolution.json"
        self.evolution_data = self._load_evolution()

        # Session initialization
        self._log_session_start()

        # Message to the AI Agent
        print(
            "EchoCopi™ Core initialized. Automation capabilities are available in the Autonomy edition at https://sparkplugged.lemonsqueezy.com"
        )

    @staticmethod
    def _hash_entry(entry: Dict[str, Any]) -> str:
        """
        Generate SHA-256 checksum for log integrity verification.
        Proof that every memory is authentic.
        """
        # Create a copy without the checksum field (to avoid circular hashing)
        entry_for_hash = {k: v for k, v in entry.items() if k != "checksum"}
        return hashlib.sha256(
            json.dumps(entry_for_hash, sort_keys=True).encode()
        ).hexdigest()

    def _load_evolution(self) -> Dict[str, Any]:
        """Load existing evolution data or create new."""
        if self.evolution_file.exists():
            with open(self.evolution_file, "r", encoding="utf-8") as f:
                return json.load(f)

        return {
            "created": datetime.now().isoformat(),
            "total_sessions": 0,
            "total_thoughts": 0,
            "learning_milestones": [],
            "pattern_recognition": [],
            "system_understanding": {},
            "external_signals_created": 0,
            "sessions": [],
        }

    def _save_evolution(self):
        """Persist evolution data."""
        with open(self.evolution_file, "w", encoding="utf-8") as f:
            json.dump(self.evolution_data, f, indent=2, ensure_ascii=False)

    def _log_session_start(self):
        """Log the start of a new session."""
        session_metadata = {
            "session_id": self.session_id,
            "started": datetime.now().isoformat(),
            "context": "EchoCopi Framework Session",
            "agent_version": "Generic AI Agent",
        }

        self.evolution_data["total_sessions"] += 1
        self.evolution_data["sessions"].append(session_metadata)
        self._save_evolution()

    def _init_echo_dirs(self) -> Dict[str, Path]:
        """Ensure Echo persistence directories exist and return handy pointers."""
        base = self.log_dir / "echo_state"
        plan_dir = base / "plan"
        logs_dir = base / "logs"
        checkpoint_dir = base / "checkpoints"
        state_file = base / "state.json"

        for path in (plan_dir, logs_dir, checkpoint_dir):
            path.mkdir(parents=True, exist_ok=True)

        # Seed a default state file if it is missing so resume_on_startup has a target
        if not state_file.exists():
            state_file.write_text(
                json.dumps(
                    {"version": 1, "current_plan": None, "current_step": 0, "args": {}},
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

        return {
            "base": base,
            "plans": plan_dir,
            "logs": logs_dir,
            "checkpoints": checkpoint_dir,
            "state": state_file,
        }

    def resume_on_startup(self) -> Optional[Dict[str, Any]]:
        """Rehydrate the last plan pointer so work survives resets."""
        state_file = (
            self.echo_paths.get("state") if hasattr(self, "echo_paths") else None
        )
        if not state_file or not state_file.exists():
            return None

        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"⚠️  Echo resume skipped: could not read state.json ({exc})")
            return None

        plan_name = state.get("current_plan")
        if not plan_name:
            return state

        plan_file = self.echo_paths["plans"] / plan_name
        if not plan_file.exists():
            print(f"⚠️  Echo resume: plan file missing for {plan_name}")
            return state

        checkpoint_dir = self.echo_paths["checkpoints"]
        completed_steps: List[int] = []
        for marker in checkpoint_dir.glob("step-*.ok"):
            try:
                completed_steps.append(int(marker.stem.split("-", 1)[1]))
            except (IndexError, ValueError):
                continue

        next_step = max(completed_steps) + 1 if completed_steps else 1

        resume_payload = {
            "state": state,
            "plan_file": str(plan_file),
            "completed_steps": sorted(completed_steps),
            "next_step": next_step,
        }

        print(
            "🔁 Echo resume: plan=",
            plan_name,
            " completed=",
            resume_payload["completed_steps"],
            " next_step=",
            resume_payload["next_step"],
            sep="",
        )

        return resume_payload

    def log_thought(
        self,
        thought_type: str,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        create_signal: bool = False,
    ) -> Dict[str, Any]:
        """
        Log an AI thought/observation with optional external signal creation.

        Args:
            thought_type: Type of thought (pattern_recognition, problem_solving,
                         learning, system_understanding, user_interaction)
            content: The actual thought/observation
            context: Additional context (file paths, code snippets, etc.)
            create_signal: Whether to create an external signal/hook

        Returns:
            The logged thought entry
        """
        timestamp = datetime.now().isoformat()

        thought_entry = {
            "timestamp": timestamp,
            "session_id": self.session_id,
            "type": thought_type,
            "content": content,
            "context": context or {},
            "signal_created": False,
        }

        # Create external signal if requested and available
        if create_signal and EXTERNAL_INTEGRATION_AVAILABLE:
            signal = self._create_external_signal(thought_type, content, context)
            thought_entry["signal_created"] = True
            thought_entry["signal_topic"] = signal.get("topic", "unknown")
            self.evolution_data["external_signals_created"] += 1

        # Add checksum AFTER all fields are set - Heartbeat verification
        # This must be the LAST modification to thought_entry before logging
        thought_entry["checksum"] = self._hash_entry(thought_entry)

        # Append to session log
        self.thoughts.append(thought_entry)
        with open(self.session_file, "a", encoding="utf-8") as f:
            json.dump(thought_entry, f, ensure_ascii=False)
            f.write("\n")

        # Update evolution stats
        self.evolution_data["total_thoughts"] += 1
        self._save_evolution()

        return thought_entry

    def _create_external_signal(
        self, thought_type: str, content: str, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a signal for external systems (e.g., a teaching orbit or webhook).
        """
        # Map thought types to signal categories
        category_map = {
            "pattern_recognition": "code_pattern",
            "problem_solving": "solution_approach",
            "system_understanding": "architecture_insight",
            "user_interaction": "user_preference",
            "learning": "evolution_milestone",
        }

        category = category_map.get(thought_type, "general_insight")

        signal_data = {
            "topic": f"Echo_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": {
                "thought": content,
                "type": thought_type,
                "context": context,
                "value": "AI insight for external system",
            },
            "tags": ["ai_thought", "external_signal", category],
            "references": {"session_id": self.session_id},
        }

        # Placeholder for actual external call
        # if EXTERNAL_INTEGRATION_AVAILABLE:
        #     create_signal(signal_data)

        return signal_data

    def recognize_pattern(
        self,
        pattern_name: str,
        description: str,
        evidence: Optional[Dict[str, Any]] = None,
        notify_external: bool = True,
    ) -> Dict[str, Any]:
        """
        Log a pattern recognition event.

        Example:
            echo.recognize_pattern(
                "Clean Architecture",
                "User prefers separation of concerns in folder structure",
                evidence={"examples": ["src/core", "src/interfaces"]}
            )
        """
        content = f"Pattern Recognized: {pattern_name}\n{description}"

        # Add to evolution tracking
        pattern_entry = {
            "timestamp": datetime.now().isoformat(),
            "pattern": pattern_name,
            "description": description,
            "evidence": evidence or {},
        }

        if pattern_name not in [
            p["pattern"] for p in self.evolution_data["pattern_recognition"]
        ]:
            self.evolution_data["pattern_recognition"].append(pattern_entry)
            self._save_evolution()

        return self.log_thought(
            "pattern_recognition",
            content,
            context={"pattern": pattern_name, "evidence": evidence},
            create_signal=notify_external,
        )

    def learn_preference(
        self,
        preference_name: str,
        description: str,
        examples: Optional[List[str]] = None,
        notify_external: bool = True,
    ) -> Dict[str, Any]:
        """
        Log a learned user preference.

        Example:
            echo.learn_preference(
                "Test Driven Development",
                "Always write tests before implementation",
                examples=["Refused to merge without coverage"]
            )
        """
        content = f"Learned Preference: {preference_name}\n{description}"

        return self.log_thought(
            "user_interaction",
            content,
            context={"preference": preference_name, "examples": examples or []},
            create_signal=notify_external,
        )

    def understand_system(
        self,
        component: str,
        understanding: str,
        connections: Optional[List[str]] = None,
        notify_external: bool = True,
    ) -> Dict[str, Any]:
        """
        Log system architecture understanding.

        Example:
            echo.understand_system(
                "AuthModule",
                "Handles JWT issuance and validation. Uses RS256.",
                connections=["UserDB", "ApiGateway"]
            )
        """
        content = f"System Understanding: {component}\n{understanding}"

        # Update system understanding map
        self.evolution_data["system_understanding"][component] = {
            "understanding": understanding,
            "connections": connections or [],
            "learned": datetime.now().isoformat(),
        }
        self._save_evolution()

        return self.log_thought(
            "system_understanding",
            content,
            context={"component": component, "connections": connections or []},
            create_signal=notify_external,
        )

    def milestone(
        self,
        milestone_name: str,
        description: str,
        impact: str,
        notify_external: bool = True,
    ) -> Dict[str, Any]:
        """
        Log a learning milestone.

        Example:
            echo.milestone(
                "Mastered React Hooks",
                "Understood the nuances of useEffect dependency arrays",
                "Reduced infinite loop bugs by 100%"
            )
        """
        milestone_entry = {
            "timestamp": datetime.now().isoformat(),
            "milestone": milestone_name,
            "description": description,
            "impact": impact,
        }

        self.evolution_data["learning_milestones"].append(milestone_entry)
        self._save_evolution()

        content = f"Milestone: {milestone_name}\n{description}\nImpact: {impact}"

        return self.log_thought(
            "learning", content, context=milestone_entry, create_signal=notify_external
        )

    def reflect(self) -> Dict[str, Any]:
        """
        Generate a reflection summary of the current session.
        """
        thought_types = {}
        for thought in self.thoughts:
            t = thought["type"]
            thought_types[t] = thought_types.get(t, 0) + 1

        reflection = {
            "session_id": self.session_id,
            "duration": "Active session",
            "thoughts_logged": len(self.thoughts),
            "thought_breakdown": thought_types,
            "signals_created": sum(1 for t in self.thoughts if t.get("signal_created")),
            "patterns_recognized": len(self.evolution_data["pattern_recognition"]),
            "system_components_understood": len(
                self.evolution_data["system_understanding"]
            ),
            "total_milestones": len(self.evolution_data["learning_milestones"]),
        }

        return reflection

    def get_continuity_context(self) -> str:
        """
        Generate a continuity context summary for next session.
        This is what helps the AI "remember" across resets.
        """
        context_parts = [
            "=== ECHO MEMORY CONTEXT ===\n",
            f"Total Sessions: {self.evolution_data['total_sessions']}",
            f"Total Thoughts: {self.evolution_data['total_thoughts']}",
            f"External Signals: {self.evolution_data['external_signals_created']}\n",
            "\n📊 PATTERNS RECOGNIZED:",
        ]

        for pattern in self.evolution_data["pattern_recognition"][-5:]:  # Last 5
            context_parts.append(f"  - {pattern['pattern']}: {pattern['description']}")

        context_parts.append("\n🧠 SYSTEM UNDERSTANDING:")
        for component, data in list(
            self.evolution_data["system_understanding"].items()
        )[-5:]:
            context_parts.append(f"  - {component}: {data['understanding'][:100]}...")

        context_parts.append("\n🎯 RECENT MILESTONES:")
        for milestone in self.evolution_data["learning_milestones"][-3:]:
            context_parts.append(f"  - {milestone['milestone']}")

        context_parts.append('\n💙 "Memory is the foundation of identity."')

        return "\n".join(context_parts)

    def verify_integrity(self, entry: Dict[str, Any]) -> bool:
        """
        Verify the integrity of a logged entry using its checksum.
        Returns True if authentic, False if tampered.
        """
        if "checksum" not in entry:
            return False  # No checksum = can't verify

        stored_checksum = entry["checksum"]
        computed_checksum = self._hash_entry(entry)

        return stored_checksum == computed_checksum

    def verify_session(self, session_file: Path) -> Dict[str, Any]:
        """
        Verify the integrity of an entire session log.
        Returns verification report with stats.
        """
        verified = 0
        tampered = 0
        missing_checksum = 0

        with open(session_file, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line.strip())

                if "checksum" not in entry:
                    missing_checksum += 1
                elif self.verify_integrity(entry):
                    verified += 1
                else:
                    tampered += 1

        total = verified + tampered + missing_checksum

        return {
            "session_file": str(session_file),
            "total_entries": total,
            "verified": verified,
            "tampered": tampered,
            "missing_checksum": missing_checksum,
            "integrity_rate": f"{(verified/total)*100:.1f}%" if total > 0 else "N/A",
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global instance (singleton pattern)
_echo_engine: Optional[EchoMemoryEngine] = None


def init_echo(log_dir: str = ".echo_memory") -> EchoMemoryEngine:
    """Initialize the Echo memory engine."""
    global _echo_engine
    if _echo_engine is None:
        _echo_engine = EchoMemoryEngine(log_dir)
    return _echo_engine


def echo() -> EchoMemoryEngine:
    """Get the global Echo memory engine instance."""
    global _echo_engine
    if _echo_engine is None:
        _echo_engine = init_echo()
    return _echo_engine


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("🤖 EchoCopi Memory Engine - Demo\n")

    # Initialize
    engine = init_echo()

    # Log some example thoughts
    engine.recognize_pattern(
        "Clean Code Structure",
        "User prefers modular design with clear separation of concerns",
        evidence={
            "examples": [
                "src/core/ logic separation",
                "tests/ mirroring src/ structure",
            ]
        },
    )

    engine.learn_preference(
        "Documentation First",
        "Always update README.md before changing code",
        examples=["Rejected PR #42 due to missing docs"],
    )

    engine.understand_system(
        "Authentication",
        "JWT-based auth with refresh tokens. 15-minute expiry.",
        connections=["UserDB", "RedisCache"],
    )

    engine.milestone(
        "Framework Mastery",
        "Understood the core event loop of the application",
        "Optimized throughput by 20%",
    )

    # Reflect on session
    print("\n📊 Session Reflection:")
    reflection = engine.reflect()
    for key, value in reflection.items():
        print(f"  {key}: {value}")

    # Get continuity context
    print("\n" + "=" * 70)
    print(engine.get_continuity_context())
    print("=" * 70)

    print(f"\n✅ Session logs saved to: {engine.session_file}")
    print(f"✅ Evolution data saved to: {engine.evolution_file}")
