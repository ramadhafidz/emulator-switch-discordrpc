# AGENTS.md

## Project Overview

Pokémon Switch RPC is a modular Python application that provides Discord Rich Presence for Pokémon games running through the Eden Nintendo Switch emulator.

The application is designed to:

- Detect the Eden emulator process.
- Identify the currently running Pokémon game.
- Locate the corresponding local save file.
- Read supported Pokémon save data through PKHeX.Core.
- Convert save data into a common application state.
- Display relevant information through Discord Rich Presence.
- Clear the Rich Presence when the game closes.

The project currently uses:

- Python for the main application.
- C# / .NET for the PKHeX.Core bridge.
- PKHeX.Core for Pokémon save parsing.
- PyPresence for Discord Rich Presence.
- psutil and pywin32 for Windows process and window detection.

---

## Core Architecture

The intended application flow is:

```text
Eden
  ↓
Game Detector
  ↓
Game Registry
  ↓
Save Path Resolver
  ↓
Python Save Reader
  ↓
PokemonSaveReader (.NET / C#)
  ↓
PKHeX.Core
  ↓
JSON
  ↓
GameState
  ↓
Discord RPC
```

Keep these responsibilities separated.

### Python
Python is responsible for:
- Application lifecycle.
- Configuration.
- Eden process detection.
- Game detection.
- Game registry.
- Save path resolution.
- Calling the C# save reader.
- Parsing the returned JSON.
- Building `GameState`.
- Discord RPC integration.

### C# / .NET
C# is responsible for:
- Loading Pokémon save files through PKHeX.Core.
- Detecting the save format through PKHeX.
- Extracting verified save data.
- Returning structured JSON to the Python application.

Do not move Pokémon save parsing into Python unless there is a specific architectural reason to do so.

---

## General Rules

### 1. Preserve the Architecture
Do not unnecessarily merge modules or move responsibilities between components.

Prefer small, focused modules over large files containing unrelated logic.

Before introducing a new abstraction, check whether an existing class or module already provides the required responsibility.

### 2. Keep the Project Modular
Game-specific logic should remain isolated.

Adding a new Pokémon game should not require rewriting the core application loop.

Prefer:
```text
Game Definition
Game Detection
Save Reader
```

as independent concepts.

### 3. Do Not Hardcode User-Specific Paths
Never introduce paths such as:
```text
C:\Users\Ramadhafidz\...
D:\Games\Eden\...
```
into production code.

Use dynamic paths such as:
```text
Path.home()
```
and configuration where appropriate.

User-specific paths may only appear in temporary debugging scripts or documentation examples when explicitly necessary.

### 4. Keep Save Access Read-Only
The application is a save-data reader.

Never add functionality that:
- Modifies save files.
- Writes Pokémon data.
- Injects data into saves.
- Deletes save files.
- Automatically creates backups by modifying emulator data.
- Changes emulator save data.

Reading save data is allowed.

Writing save data is outside the scope of this project.

---

## Pokémon Save Data Rules

### Never Guess Save Offsets
This is one of the most important project rules.

Do not invent or estimate:
- Save offsets.
- Field locations.
- Block sizes.
- Pointer locations.
- Pokémon structure locations.
- Pokédex offsets.
- Location offsets.
- Playtime offsets.

Save structures must be based on:
1. Verified PKHeX implementations.
2. Official or reliable technical documentation.
3. Reproducible analysis of known save formats.

If the structure is unknown, leave the feature unimplemented rather than guessing.

### Prefer PKHeX Implementations
When PKHeX.Core already exposes the required data, use the existing PKHeX API instead of manually parsing the underlying bytes.

For example, prefer:
```text
save.MyStatus
save.Played
save.Zukan
```
over manually calculating offsets.

### Preserve Read-Only Behavior
Do not call APIs that modify save data.

Do not introduce write operations into the bridge.

---

## PKHeX Rules
PKHeX is a third-party dependency.

The PKHeX source tree must remain outside the tracked repository.

Expected local structure:
```text
bridge/
├── PKHeX/
└── PokemonSaveReader/
```

`bridge/PKHeX/` is intentionally ignored by Git.

Do not:
- Commit PKHeX source.
- Copy PKHeX source into another project directory.
- Modify PKHeX source to implement project-specific features.
- Vendor PKHeX into this repository.

If PKHeX functionality is missing, implement the required logic in the project bridge when possible, or document the limitation.

---

## C# Bridge Rules
The C# project is located at:
```text
bridge/PokemonSaveReader/
```

The bridge should:
1. Receive a save file path.
2. Validate that the file exists.
3. Load the save using PKHeX.
4. Identify the supported save type.
5. Extract the required data.
6. Return structured JSON.
7. Return a non-zero exit code on failure.

The bridge should not:
- Modify the input save.
- Print non-JSON data to stdout when returning successful results.
- Depend on Python internals.
- Contain Discord RPC logic.

Use `stderr` for errors when appropriate so stdout remains machine-readable JSON.

---

## JSON Communication
Python and C# communicate through JSON.

The JSON output should be:
- Structured.
- Predictable.
- Machine-readable.
- Backward-compatible where practical.

Example:
```json
{
	"success": true,
	"game": {
		"version": "SL",
		"generation": 9,
		"type": "scarlet_violet"
	},
	"trainer": {
		"name": "Trainer",
		"id": 123456789
	},
	"playtime": {
		"hours": 10,
		"minutes": 51,
		"seconds": 28
	},
	"pokedex": {
		"seen": 41,
		"caught": 25,
		"total": 1025
	}
}
```
Do not silently change the JSON schema when existing consumers depend on it.

If a breaking change is necessary, update the Python consumer and documentation together.

---

## Game Support
Supported games currently include:
- Pokémon Legends: Arceus
- Pokémon Scarlet
- Pokémon Violet
- Pokémon Legends: Z-A

However, detection and save-reading support are independent.

Do not mark a feature as supported merely because the game is detectable.

When adding a game:
- Add its game definition.
- Add or update detection logic if required.
- Add its save path information.
- Implement a verified save reader if supported.
- Test the save reader independently.
- Connect the resulting data to `GameState`.
- Update the README and game support documentation.

---

## Game IDs
Use the existing internal game ID convention:
```text
pokemon_legends_arceus
pokemon_scarlet
pokemon_violet
pokemon_legends_za
```

Do not rename existing IDs without a clear migration reason.

Game IDs should be stable and machine-oriented.

Display names belong in the game configuration.

---

## Configuration
Game configuration belongs in `config.json`.

Do not hardcode:
- Discord Application IDs.
- Artwork names.
- Game display names.
- Regions.
- Update intervals.

Use configuration where the value is intended to be user-configurable.

Never commit secrets, authentication tokens, private keys, or credentials.

A Discord Application ID is not a secret, but use a placeholder in documentation examples:
```json
{
	"discord": {
		"client_id": "YOUR_DISCORD_APPLICATION_ID"
	}
}
```

---

## Discord RPC Rules
Discord RPC is handled by:
```text
rpc/discord_rpc.py
```

Keep Discord-specific behavior inside the RPC layer.

The rest of the application should not directly depend on PyPresence APIs when avoidable.

The RPC layer should handle:
- Connection.
- Reconnection.
- Presence updates.
- Clearing presence.
- Closing the connection.
- Connection failures.

When the detected game changes:
1. Clear the previous presence when necessary.
2. Load the new game definition.
3. Build the new state.
4. Update Discord.

When the game closes:
```text
Game detected
      ↓
Eden/game no longer running
      ↓
Clear RPC
```

Do not leave stale Rich Presence active after the game closes.

---

## GameState
`GameState` is the common state representation used by the application.

Current fields include:
```python
@dataclass
class GameState:
	game_id: str
	playtime_seconds: int | None = None
	pokedex_caught: int | None = None
	pokedex_total: int | None = None
	location: str | None = None
```

Keep `GameState` independent from PKHeX-specific classes.

Do not expose PKHeX objects directly to the Discord RPC layer.

The intended flow is:
```text
PKHeX
  ↓
JSON
  ↓
GameState
  ↓
Discord RPC
```

---

## Error Handling
The application should fail gracefully.

Do not crash the entire application because:
- Eden is not running.
- Discord is unavailable.
- A save file cannot be found.
- A save format is unsupported.
- PKHeX cannot identify a save.
- The C# bridge fails.
- Discord RPC disconnects.

Prefer:
```text
Log error
↓
Return None / failure state
↓
Continue monitoring
```

Use exceptions for genuinely unexpected failures.

Do not use broad exception handling to silently hide programming errors.

---

## Logging
Keep console output useful and concise.

Good:
```text
Eden: running
Game detected: Pokémon Scarlet
Rich Presence updated.
```

For errors, provide enough information to diagnose the issue.

Avoid logging:
- Save file contents.
- Sensitive information.
- Large binary dumps.
- Credentials.
- Authentication tokens.

---

## Testing
Test individual components independently when possible.

Current test scripts include:
```text
test/game_detection.py
test/save_path.py
test/game_save_reader.py
```

When modifying a component, run the relevant test before considering the change complete.

For save-reader changes, test with actual supported save files when available.

Do not commit real emulator save files to the repository.

---

## Code Style

### Python
Use:
- Type hints where practical.
- `pathlib.Path` for filesystem paths.
- Small focused functions.
- Clear class and variable names.
- Explicit error handling.

Use 2 tabs for indentation.

Example:
```python
class Example:

	def method(self):
		if condition:
			return True

		return False
```

Do not replace the project's indentation style with 4 spaces.

### C#
Follow standard C# conventions.

Use:
- PascalCase for classes and public members.
- camelCase for local variables and parameters.
- Explicit types when they improve readability.
- Modern C# features when appropriate.

The Python project's 2-tab indentation rule does not need to be forced onto C# code.

---

## Dependencies
Avoid adding dependencies without a clear reason.

Before adding a dependency:
1. Check whether the standard library can solve the problem.
2. Check whether an existing dependency already provides the functionality.
3. Consider maintenance and compatibility.
4. Update `requirements.txt` or the relevant .NET project file.
5. Update documentation if the dependency affects setup.

Do not introduce large frameworks for small problems.

---

## File Organization
Keep the existing structure unless there is a strong reason to change it:
```text
games/
rpc/
test/
bridge/
docs/
```

Do not create random utility directories.

If a new module has a clear responsibility, place it in the appropriate existing package.

---

## Git Rules
Never commit:
```text
.venv/
__pycache__/
*.pyc
bridge/PKHeX/
bridge/PokemonSaveReader/bin/
bridge/PokemonSaveReader/obj/
config.local.json
.env
eden/
main
main2
backup
poke_trade
*.sav
*.dsv
*.dat
*.bin
```

Do not commit:
- Emulator save files.
- Local emulator data.
- Personal configuration.
- Secrets.
- PKHeX source.
- Build artifacts.

Before committing, check:
```bash
git status
git status --ignored
```

---

## Documentation Rules
When behavior changes, update the relevant documentation.

Important documentation files:
```text
README.md
AGENTS.md

docs/
├── ARCHITECTURE.md
├── DEVELOPMENT.md
├── CONFIGURATION.md
├── SAVE-READER.md
├── DISCORD-RPC.md
├── GAME-SUPPORT.md
├── TROUBLESHOOTING.md
└── ROADMAP.md
```

Do not document planned functionality as if it already exists.

Clearly distinguish:
```text
Implemented
In Progress
Planned
Unsupported
```

---

## Adding a New Pokémon Game
When adding a new game, follow this general process:

1. **Game Definition**

Add the game to `config.json`.

2. **Detection**

Add the required identifier to the Eden detector.

3. **Save Path**

Add the game's title ID or save resolution mechanism.

4. **Save Reader**

Implement save parsing only after the format is verified.

5. **JSON**

Return a consistent JSON structure.

6. **GameState**

Map the returned data into the common `GameState`.

7. **Discord RPC**

Add appropriate Rich Presence behavior.

8. **Tests**

Create or update tests for the new game.

9. **Documentation**

Update:
- `README.md`
- `docs/GAME-SUPPORT.md`
- `docs/SAVE-READER.md`
- `docs/ROADMAP.md`

---

## What Not To Do
Do not:
- Guess Pokémon save offsets.
- Modify save files.
- Commit emulator saves.
- Commit PKHeX source.
- Hardcode personal filesystem paths.
- Put Discord RPC logic into save readers.
- Put PKHeX-specific objects into `GameState`.
- Add unnecessary dependencies.
- Claim unsupported features are implemented.
- Remove existing functionality without checking its consumers.
- Rewrite working modules without a concrete reason.
- Change project architecture merely for stylistic preference.

---

## Development Philosophy
Prefer:
```text
Simple
Modular
Verifiable
Read-only
Testable
Maintainable
```

over:
```text
Complex
Monolithic
Guess-based
Write-capable
Hardcoded
Over-engineered
```

When uncertain about a Pokémon save structure, **do not guess**.

When uncertain about an architectural change, inspect the existing implementation and its consumers before changing it.

When a feature cannot be safely verified, leave it unimplemented and document the limitation.

---

## Priority Order
When making implementation decisions, prioritize:
1. Correctness
2. Save-data safety
3. Existing architecture
4. Maintainability
5. Testability
6. User experience
7. Performance
8. Convenience

Never sacrifice save-data safety or correctness for convenience.

---

## Final Checklist
Before considering a change complete:
- [ ] Existing functionality still works.
- [ ] Relevant tests pass.
- [ ] No user-specific paths were introduced.
- [ ] No save files were added to Git.
- [ ] No PKHeX source was added to Git.
- [ ] No secrets were added.
- [ ] Save access remains read-only.
- [ ] Save structures are based on verified information.
- [ ] Documentation reflects the actual implementation.
- [ ] Python code follows the 2-tab indentation convention.
- [ ] New functionality is placed in the appropriate module.

---

## Documentation and Context7

Use **Context7** as the primary source for up-to-date and relevant documentation when working with external libraries, frameworks, SDKs, APIs, or developer tools.

### When to Use Context7

AI agents should use Context7 when:

- Implementing functionality that depends on an external library.
- Using an API or SDK.
- Unsure about the current API of a dependency.
- Checking method signatures, parameters, return values, or configuration.
- Investigating breaking changes between library versions.
- Debugging behavior that may be version-dependent.
- Adding or updating dependencies.
- Working with Python packages such as PyPresence, psutil, or pywin32.
- Working with .NET or C# APIs.
- Working with PKHeX.Core APIs.
- Working with Discord Rich Presence or Discord RPC APIs.
- Working with Eden APIs or documentation when official documentation is available.
- Verifying recommended usage patterns before implementing a non-trivial integration.

### Documentation Priority

When external documentation is needed, prefer sources in this order:

1. Context7 documentation for the relevant library or project.
2. Official documentation or official source repository.
3. Version-specific API documentation.
4. Reliable technical documentation.
5. Other sources only when the above are insufficient.

Do not rely on outdated examples when current documentation is available.

### Version Awareness

Always consider the version actually used by the project.

Before implementing an API-dependent feature:

1. Check the dependency version in the project.
2. Use Context7 to retrieve documentation relevant to that version when available.
3. Verify that the API being used exists in that version.
4. Only then implement the feature.

Do not blindly copy examples written for a different major version.

### PKHeX-Specific Rule

PKHeX changes over time and its internal APIs may change.

When working with PKHeX.Core:

1. Check the local PKHeX source first when it is available.
2. Use Context7 or official PKHeX documentation/source information to verify the relevant API.
3. Prefer existing PKHeX abstractions over manual binary parsing.
4. Verify the implementation against the actual PKHeX version being used.
5. Never invent APIs, offsets, block layouts, or field locations.

If Context7 and the local source disagree, treat the **actual local source version** as authoritative for the code being built and investigate the discrepancy before proceeding.

### Do Not Hallucinate APIs

Never assume that a class, method, property, parameter, or API exists.

If an API cannot be verified:

- Search the relevant documentation.
- Inspect the installed/local source when available.
- Clearly state the uncertainty.
- Do not fabricate an implementation.

A missing or uncertain API should be treated as an investigation task, not an invitation to guess.

### Documentation in Code Changes

When a feature is implemented based on external documentation:

- Use the documented API correctly.
- Prefer stable public APIs over undocumented internals.
- Avoid unnecessary compatibility workarounds.
- Document important version-specific behavior when it affects future maintenance.

The goal is to keep the implementation aligned with current, verifiable documentation rather than relying on model memory.