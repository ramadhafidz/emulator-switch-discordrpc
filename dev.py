import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BRIDGE_PROJECT = (
	ROOT / "bridge" / "PokemonSaveReader" / "PokemonSaveReader.csproj"
)


def run(command: Sequence[str]) -> int:
	print(f"> {' '.join(command)}")

	try:
		result = subprocess.run(
			command,
			cwd=ROOT,
		)

	except FileNotFoundError:
		print(f"Executable not found: {command[0]}")
		print("Make sure the required tool is installed and available on PATH.")

		return 127

	except OSError as error:
		print(f"Failed to start command: {error}")
		return 1

	if result.returncode != 0:
		print(f"Command failed with exit code {result.returncode}.")
		print(f"Failed command: {' '.join(command)}")

		if is_python_tool(command):
			print("Python tool failed.")
			print(
				"Make sure development dependencies are "
				"installed: pip install -r requirements-dev.txt"
			)

	return result.returncode


def run_many(commands: Sequence[Sequence[str]]) -> int:
	for command in commands:
		exit_code = run(command)

		if exit_code != 0:
			return exit_code

	return 0


def is_python_tool(command: Sequence[str]) -> bool:
	return (
		len(command) >= 2
		and command[0] == sys.executable
		and command[1] == "-m"
	)


def command_lint() -> int:
	return run([sys.executable, "-m", "ruff", "check", "."])


def command_format() -> int:
	return run_many(
		[
			[
				sys.executable,
				"-m",
				"ruff",
				"check",
				"--fix",
				".",
			],
			[
				sys.executable,
				"-m",
				"ruff",
				"format",
				".",
			],
		]
	)


def command_typecheck() -> int:
	return run([sys.executable, "-m", "pyright"])


def command_test() -> int:
	return run([sys.executable, "-m", "pytest"])


def command_build() -> int:
	return run_many(
		[
			[
				"dotnet",
				"restore",
				str(BRIDGE_PROJECT),
				"--ignore-failed-sources",
			],
			[
				"dotnet",
				"build",
				str(BRIDGE_PROJECT),
				"--no-restore",
			],
		]
	)


def command_check() -> int:
	return run_many(
		[
			[sys.executable, "-m", "ruff", "check", "."],
			[sys.executable, "-m", "pyright"],
			[sys.executable, "-m", "pytest"],
		]
	)


def command_run() -> int:
	return run([sys.executable, "main.py"])


def command_save() -> int:
	return run([sys.executable, "test/game_save_reader.py"])


def command_verify() -> int:
	return run_many(
		[
			[
				"dotnet",
				"restore",
				str(BRIDGE_PROJECT),
				"--ignore-failed-sources",
			],
			[
				"dotnet",
				"build",
				str(BRIDGE_PROJECT),
				"--no-restore",
			],
			[
				sys.executable,
				"test/game_save_reader.py",
			],
		]
	)


def command_clean() -> int:
	targets = [
		ROOT / ".ruff_cache",
		ROOT / ".pytest_cache",
		ROOT / ".pyright",
		ROOT / "__pycache__",
		ROOT / "games" / "__pycache__",
		ROOT / "rpc" / "__pycache__",
		ROOT / "test" / "__pycache__",
		ROOT / "bridge" / "PokemonSaveReader" / "bin",
		ROOT / "bridge" / "PokemonSaveReader" / "obj",
	]

	for target in targets:
		if not target.exists():
			continue

		print(f"Removing {target.relative_to(ROOT)}")

		if target.is_dir():
			shutil.rmtree(target)
		else:
			target.unlink()

	return 0


def command_all() -> int:
	return run_many(
		[
			[sys.executable, "-m", "ruff", "check", "."],
			[
				sys.executable,
				"-m",
				"ruff",
				"format",
				"--check",
				".",
			],
			[sys.executable, "-m", "pyright"],
			[sys.executable, "-m", "pytest"],
			[
				"dotnet",
				"restore",
				str(BRIDGE_PROJECT),
				"--ignore-failed-sources",
			],
			[
				"dotnet",
				"build",
				str(BRIDGE_PROJECT),
				"--no-restore",
			],
		]
	)


COMMANDS = {
	"all": command_all,
	"build": command_build,
	"check": command_check,
	"clean": command_clean,
	"format": command_format,
	"lint": command_lint,
	"run": command_run,
	"save": command_save,
	"test": command_test,
	"typecheck": command_typecheck,
	"verify": command_verify,
}


def print_usage() -> None:
	commands = ", ".join(sorted(COMMANDS))

	print("Usage: python dev.py <command>")
	print(f"Commands: {commands}")
	print()
	print("Common commands:")
	print("  python dev.py check      Run lint, typecheck, and tests")
	print("  python dev.py format     Fix lint issues and format Python code")
	print("  python dev.py build      Restore and build the C# save reader")
	print("  python dev.py save       Run the save-reader integration test")
	print(
		"  python dev.py verify     "
		"Build the bridge and verify local save readers"
	)
	print("  python dev.py all        Run full validation and bridge build")


def main(argv: Sequence[str]) -> int:
	if len(argv) != 2 or argv[1] in {
		"-h",
		"--help",
		"help",
	}:
		print_usage()
		return 0 if len(argv) == 2 else 2

	command_name = argv[1]
	command = COMMANDS.get(command_name)

	if command is None:
		print(f"Unknown command: {command_name}")
		print_usage()
		return 2

	return command()


if __name__ == "__main__":
	raise SystemExit(main(sys.argv))
