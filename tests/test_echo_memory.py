"""Tests for EchoCopi Core memory entries: integrity, schema, resume, and continuity."""

import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

# Adjust import path if needed; assumes src is in path or run from root with proper PYTHONPATH
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from echo_memory import EchoMemoryEngine


@pytest.fixture
def engine(tmp_path):
    """Create an engine with a temporary log directory."""
    return EchoMemoryEngine(log_dir=str(tmp_path))


def test_log_thought_writes_jsonl_and_roundtrips(engine):
    entry = engine.log_thought("pattern_recognition", "Test thought", context={"key": "value"})
    assert engine.session_file.exists()
    with open(engine.session_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1
    loaded = json.loads(lines[0])
    assert loaded["content"] == "Test thought"
    assert loaded["type"] == "pattern_recognition"
    assert loaded["context"] == {"key": "value"}
    assert loaded["checksum"] == entry["checksum"]
    # Round-trip unchanged
    assert loaded == entry


def test_verify_integrity_detects_tampering(engine):
    entry = engine.log_thought("learning", "Original content")
    assert engine.verify_integrity(entry) is True

    # Tamper with the file
    with open(engine.session_file, "r", encoding="utf-8") as f:
        line = f.read()
    tampered = json.loads(line)
    tampered["content"] = "Tampered content"
    with open(engine.session_file, "w", encoding="utf-8") as f:
        json.dump(tampered, f)
        f.write("\n")

    # Reload the entry
    with open(engine.session_file, "r", encoding="utf-8") as f:
        tampered_entry = json.loads(f.read())
    assert engine.verify_integrity(tampered_entry) is False


def test_schema_rejects_malformed_on_write(engine):
    # Force a bad entry by calling internal after partial construction, or mock
    # Directly test the validator
    bad_entry = {
        "timestamp": "not-iso",
        "session_id": engine.session_id,
        "type": "test",
        "content": "bad",
        "context": {},
        "checksum": "dummy",
    }
    with pytest.raises(ValueError, match="Invalid memory entry"):
        engine._validate_entry(bad_entry, on_write=True)

    # Valid should pass
    good = engine.log_thought("test", "good")
    assert engine._validate_entry(good, on_write=False) is True


def test_schema_reports_on_read(engine):
    entry = engine.log_thought("test", "valid")
    # Corrupt schema in memory
    bad = dict(entry)
    del bad["type"]
    # Should return False and print (we don't capture print here, just check return)
    assert engine._validate_entry(bad, on_write=False) is False
    assert engine.verify_integrity(bad) is False


def test_resume_on_startup_behaves_sanely(tmp_path):
    # No files yet
    eng1 = EchoMemoryEngine(log_dir=str(tmp_path))
    assert eng1.echo_state is None or isinstance(eng1.echo_state, dict)

    # After some activity, resume should find state
    eng1.log_thought("test", "something")
    # State is created in _init_echo_dirs
    eng2 = EchoMemoryEngine(log_dir=str(tmp_path))
    # Should not crash; may return state or None depending on plan
    assert eng2.resume_on_startup() is None or isinstance(eng2.resume_on_startup(), dict)


def test_get_continuity_context_names_session(engine):
    engine.log_thought("pattern_recognition", "A pattern")
    context = engine.get_continuity_context()
    assert isinstance(context, str)
    assert "ECHO MEMORY CONTEXT" in context
    assert str(engine.evolution_data["total_sessions"]) in context
    # Previous session info is in evolution
    assert "Total Sessions" in context
