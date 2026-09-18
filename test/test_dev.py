import subprocess
import sys
from types import SimpleNamespace

import dev


def test_run_returns_subprocess_exit_code(monkeypatch, capsys):
	def fake_run(command, cwd):
		assert command == ["tool", "arg"]
		assert cwd == dev.ROOT

		return SimpleNamespace(returncode=7)

	monkeypatch.setattr(subprocess, "run", fake_run)

	assert dev.run(["tool", "arg"]) == 7

	output = capsys.readouterr().out

	assert "Command failed with exit code 7." in output
	assert "Failed command: tool arg" in output


def test_run_handles_missing_executable(monkeypatch, capsys):
	def fake_run(command, cwd):
		raise FileNotFoundError

	monkeypatch.setattr(subprocess, "run", fake_run)

	assert dev.run(["missing-tool"]) == 127

	output = capsys.readouterr().out

	assert "Executable not found: missing-tool" in output
	assert "available on PATH" in output


def test_run_prints_python_tool_hint(monkeypatch, capsys):
	def fake_run(command, cwd):
		return SimpleNamespace(returncode=1)

	monkeypatch.setattr(subprocess, "run", fake_run)

	assert dev.run([sys.executable, "-m", "missing_module"]) == 1

	output = capsys.readouterr().out

	assert "Python tool failed." in output
	assert "requirements-dev.txt" in output


def test_run_many_stops_on_first_failure(monkeypatch):
	calls = []

	def fake_run(command):
		calls.append(command)
		return 5

	monkeypatch.setattr(dev, "run", fake_run)

	exit_code = dev.run_many([["first"], ["second"]])

	assert exit_code == 5
	assert calls == [["first"]]


def test_main_help_returns_success(capsys):
	assert dev.main(["dev.py", "--help"]) == 0

	output = capsys.readouterr().out

	assert "Usage: python dev.py <command>" in output
	assert "typecheck" in output


def test_typecheck_is_registered():
	assert dev.COMMANDS["typecheck"] is dev.command_typecheck
