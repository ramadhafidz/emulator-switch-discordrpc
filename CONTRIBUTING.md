# Contributing

Thank you for your interest in contributing to Pokémon Switch RPC.

Pokémon Switch RPC is a modular, read-only Discord Rich Presence application for Pokémon games running through the Eden emulator. Contributions are welcome, especially improvements to game detection, save reading, Discord Rich Presence, documentation, testing, and project tooling.

## Project Goals

Before contributing, keep these goals in mind:

- Keep the application modular and easy to extend.
- Keep save parsing read-only.
- Prefer verified game/save formats over guessed offsets or undocumented assumptions.
- Keep game-specific logic isolated from the core runtime.
- Avoid unnecessary CPU, memory, and disk usage.
- Keep configuration separate from application logic where practical.
- Make it easy to add support for future Pokémon games.
- Keep documentation accurate and useful for both humans and AI-assisted development.

## Development Setup

### Requirements

The project currently uses:

- Windows
- Python 3.9 or newer
- Python virtual environment
- .NET 10 SDK
- Git
- Eden emulator
- Discord desktop application for Rich Presence testing

The Python application uses:

```text
pypresence
psutil
pywin32
```

The save-reading bridge uses C# and references `PKHeX.Core`.

### Clone the Repository

```powershell
git clone <repository-url>
cd pokemon-switch-rpc
```

### Create the Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### PKHeX Setup

PKHeX is used as the save-format implementation layer through `PKHeX.Core`.

The PKHeX source is intentionally kept outside the public repository. See [docs/PKHeX.md](docs/PKHeX.md) for the architecture, supported formats, and setup details.

The local bridge project is located at:

```text
bridge/PokemonSaveReader/
```

It references the local PKHeX Core project:

```text
bridge/PKHeX/PKHeX.Core/PKHeX.Core.csproj
```

Restore/build the bridge with:

```powershell
dotnet restore bridge/PokemonSaveReader/PokemonSaveReader.csproj --ignore-failed-sources
dotnet build bridge/PokemonSaveReader/PokemonSaveReader.csproj --no-restore
```

Do not commit the local `bridge/PKHeX/` source tree.

## Project Structure

```text
pokemon-switch-rpc/
├── main.py
├── config.json
├── requirements.txt
├── .gitignore
├── rpc/
│   ├── discord_rpc.py
│   └── __init__.py
├── games/
│   ├── base.py
│   ├── detector.py
│   ├── game_save_reader.py
│   ├── registry.py
│   ├── save_paths.py
│   ├── save_reader.py
│   ├── state.py
│   └── __init__.py
├── test/
├── bridge/
│   ├── PokemonSaveReader/
│   └── PKHeX/              # Local only, ignored by Git
└── docs/
```

The main responsibilities are:

- `main.py` — application loop and orchestration.
- `games/detector.py` — detects Eden and identifies the running game.
- `games/registry.py` — provides configured game definitions.
- `games/state.py` — represents normalized game state.
- `games/save_paths.py` — resolves emulator save locations.
- `games/save_reader.py` — invokes the C# save-reading bridge.
- `games/game_save_reader.py` — combines save-path resolution and save reading.
- `rpc/discord_rpc.py` — Discord Rich Presence integration.
- `bridge/PokemonSaveReader/` — C# bridge between Python and PKHeX.Core.
- `docs/` — project architecture and development documentation.

## Code Style

### Python

Use clear, small, focused modules and functions.

Follow the existing indentation style:

- **2 tabs for indentation**
- Keep imports organized.
- Use type hints where they improve clarity.
- Prefer explicit names over abbreviations.
- Avoid unnecessary abstractions.
- Handle expected runtime failures without crashing the main application.

Example:

```python
class Example:
	def run(self) -> bool:
		return True
```

### C#

Follow the existing PKHeX bridge style:

- Use standard C# formatting.
- Keep the bridge small.
- Keep Pokémon/game-format logic in PKHeX where possible.
- Do not duplicate PKHeX's format implementation in Python.
- Return stable JSON structures to the Python application.
- Keep the bridge read-only.

## Architecture Guidelines

The project follows this general flow:

```text
Eden
  ↓
Game Detector
  ↓
Game Definition / Registry
  ↓
Save Resolver
  ↓
Save Reader
  ↓
PokemonSaveReader (.NET/C#)
  ↓
PKHeX.Core
  ↓
JSON
  ↓
GameState
  ↓
Discord RPC
```

When adding functionality:

1. Determine which layer owns the responsibility.
2. Keep game-specific behavior in the game/save layer.
3. Keep Discord-specific behavior in the RPC layer.
4. Keep the application loop focused on orchestration.
5. Avoid coupling unrelated modules together.

## Adding a New Game

When adding support for a new Pokémon game:

1. Add the game definition to `config.json`.
2. Add game-title detection in `games/detector.py` if necessary.
3. Add the game's title ID to `games/save_paths.py` when verified.
4. Verify that PKHeX supports the corresponding save format.
5. Add or extend the C# bridge only when required.
6. Map the save data into the normalized `GameState`.
7. Add tests using a valid save file when possible.
8. Update [docs/GAME-SUPPORT.md](docs/GAME-SUPPORT.md).
9. Update [docs/SAVE-READER.md](docs/SAVE-READER.md) if save-reading behavior changes.
10. Update the relevant roadmap or documentation when appropriate.

Do not add guessed save offsets.

If a save format has not been verified, leave the implementation unsupported rather than returning potentially incorrect data.

## Save Reader Rules

Save parsing is one of the most important parts of this project.

### Read-only

The application must never modify a user's save file.

Do not:

- write to save files;
- patch save data;
- alter Pokémon data;
- modify inventory or progression;
- modify Pokédex data;
- create or inject Pokémon;
- overwrite emulator saves.

### Prefer PKHeX.Core

When PKHeX already provides access to the required data, use PKHeX.Core rather than implementing raw binary parsing.

This keeps format-specific knowledge inside the established save implementation and reduces the risk of incorrect offsets.

### Verify Data

Before exposing a field through the application:

- verify that the field exists in the supported save format;
- verify its meaning;
- verify the relevant PKHeX API;
- test against a real compatible save when possible.

If the meaning of a field is uncertain, do not present it as authoritative.

### Avoid Hardcoded Offsets

Do not introduce raw offsets simply because a value can be found at a particular byte position in one save.

Game updates and save-format differences can invalidate offsets.

If direct binary access is genuinely required, document:

- the game/version;
- the save format;
- the source of the offset;
- the expected data type;
- known version limitations;
- validation performed against real saves.

## Testing

Tests should be added when behavior changes.

Useful areas to test include:

- Eden process detection.
- Game detection from the Eden window title.
- Save-path resolution.
- Save-format detection.
- Save parsing.
- JSON output.
- Game state normalization.
- Discord RPC behavior.

Do not commit real personal save files.

For local testing, keep emulator save data outside Git-tracked paths or use the ignored save patterns already defined in `.gitignore`.

## Discord RPC

Discord Rich Presence should remain isolated in `rpc/discord_rpc.py`.

When changing RPC behavior:

- preserve graceful reconnect behavior;
- clear the presence when the game closes;
- avoid updating more often than necessary;
- keep artwork identifiers configurable;
- do not make Discord credentials or client IDs part of source code unnecessarily.

If a change affects user-visible Rich Presence fields, update [docs/DISCORD-RPC.md](docs/DISCORD-RPC.md).

## Configuration

User-specific configuration should not be hardcoded into Python modules.

Use `config.json` for project configuration such as:

- Discord application settings;
- update interval;
- supported game definitions;
- artwork identifiers;
- displayed game/region information.

Do not commit private credentials, tokens, personal save files, or local machine-specific secrets.

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Documentation

All repository documentation should be written in **English**.

Documentation should explain not only what the code does, but also why the architecture works that way.

When changing a system component, check whether the following documents need updates:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- [docs/SAVE-READER.md](docs/SAVE-READER.md)
- [docs/GAME-SUPPORT.md](docs/GAME-SUPPORT.md)
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- [docs/DISCORD-RPC.md](docs/DISCORD-RPC.md)
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/PKHeX.md](docs/PKHeX.md)

## Git Guidelines

Keep commits focused on one logical change.

Recommended commit format:

```text
type(scope): short description
```

Examples:

```text
feat(save-reader): add Scarlet save support
fix(detector): handle missing Eden window
refactor(rpc): isolate reconnect handling
docs(pkhex): document supported save formats
test(detector): add game title detection cases
```

Avoid commits that combine unrelated features, refactors, and documentation changes unless they are part of the same logical change.

## Pull Requests

A pull request should explain:

1. What changed.
2. Why it changed.
3. Which games or components are affected.
4. How the change was tested.
5. Whether documentation was updated.
6. Whether the change depends on a specific PKHeX version or save format.

For save-reader changes, include enough technical information for another developer to reproduce and verify the behavior.

### Pull Request Checklist

Before submitting:

- [ ] The project builds successfully.
- [ ] Python dependencies are installed correctly.
- [ ] Relevant tests pass.
- [ ] Save-reader changes were tested against a compatible save when possible.
- [ ] No save files or personal data were committed.
- [ ] No guessed save offsets were introduced.
- [ ] Save parsing remains read-only.
- [ ] Discord RPC behavior was checked when relevant.
- [ ] Documentation was updated when needed.
- [ ] `bridge/PKHeX/` remains untracked/ignored.
- [ ] The change is focused and clearly described.

## Reporting Bugs

When reporting a bug, include:

- Operating system.
- Python version.
- .NET version when relevant.
- Eden version.
- Pokémon game and version/update.
- Relevant application logs.
- Steps to reproduce.
- Expected behavior.
- Actual behavior.

Do not upload or attach personal save files unless they have been sanitized and you have verified that they contain no sensitive information.

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common problems.

## Security and Privacy

This project interacts with local emulator processes and save files.

Contributors must not add functionality that:

- accesses Nintendo online services;
- bypasses DRM or platform security;
- circumvents emulator security mechanisms;
- uploads save files without explicit user action;
- collects unnecessary personal information;
- modifies user saves without explicit project requirements and review.

For security-sensitive issues, avoid publishing private data or credentials in public issues or pull requests.

## Scope of Contributions

Useful contributions include:

- New supported Pokémon games.
- Improved Eden detection.
- Better save-path resolution.
- Additional verified save data.
- Improved Discord Rich Presence.
- Tests.
- Documentation.
- Performance improvements.
- Error handling and reliability improvements.
- Packaging and developer tooling.

Large architectural changes should be discussed before implementation so they can be evaluated against the project's current design.

## License

By contributing, you agree that your contribution may be distributed under the project's license.

If the repository does not yet contain a finalized license, confirm the intended license before publishing contribution terms that depend on it.
