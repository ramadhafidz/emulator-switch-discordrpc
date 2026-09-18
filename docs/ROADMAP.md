# ROADMAP.md

Development roadmap for **Pokémon Switch RPC**.

The project is a modular, read-only Discord Rich Presence application
for Pokémon games running through the Eden emulator.

------------------------------------------------------------------------

## 1. Project Vision

The long-term goal is to provide a lightweight Rich Presence application
that can automatically understand which supported Pokémon game is
running and expose useful, verified game state.

Target architecture:

``` text
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
GameState
  ↓
Discord RPC
```

Save reading uses a C# bridge and PKHeX.Core:

``` text
Eden
  ↓
Game Detector
  ↓
Game Definition / Registry
  ↓
Save Resolver
  ↓
PokemonSaveReader (.NET / C#)
  ↓
PKHeX.Core
  ↓
JSON
  ↓
GameState Parser
  ↓
GameState
  ↓
Discord RPC
```

The application is intentionally read-only.

------------------------------------------------------------------------

## 2. Current Status

### Foundation

-   [x] Python project structure
-   [x] Python virtual environment
-   [x] Runtime dependency configuration
-   [x] Development dependency configuration
-   [x] Discord Application
-   [x] Discord Client/Application ID configuration
-   [x] PyPresence integration
-   [x] Basic RPC wrapper
-   [x] Configurable save refresh interval
-   [x] Configurable Pokédex rotation interval
-   [x] Game-specific artwork configuration
-   [x] Session timer
-   [x] RPC cleanup
-   [x] Reconnection handling

### Eden Detection

-   [x] Eden process detection
-   [x] Eden window enumeration
-   [x] Window title inspection
-   [x] Pokémon Legends: Arceus detection mapping
-   [x] Pokémon Scarlet detection
-   [ ] Pokémon Violet detection mapping
-   [ ] Pokémon Legends: Z-A detection mapping
-   [ ] Verify Z-A detection against the actual release/runtime
    environment

### Architecture

-   [x] `GameDefinition`
-   [x] `GameRegistry`
-   [x] `GameState`
-   [x] `SaveReader`
-   [x] `GameSaveReader`
-   [x] Eden save path resolver
-   [x] Python → C# bridge
-   [x] JSON state parsing
-   [x] PKHeX.Core integration
-   [x] Game-specific C# readers

### PKHeX Save Reader

-   [x] Pokémon Legends: Arceus save detection
-   [x] Pokémon Legends: Arceus trainer data
-   [x] Pokémon Legends: Arceus playtime
-   [x] Pokémon Legends: Arceus Pokédex count
-   [x] Pokémon Scarlet save detection
-   [x] Pokémon Scarlet trainer data
-   [x] Pokémon Scarlet playtime
-   [x] Pokémon Scarlet Pokédex seen/caught counts
-   [x] Pokémon Scarlet party extraction
-   [x] Pokémon Scarlet box extraction
-   [x] Pokémon Scarlet location ID
-   [x] Pokémon Scarlet location name resolution
-   [x] Pokémon Scarlet coordinates
-   [ ] Refine Scarlet/Violet Pokédex total representation
-   [ ] Complete Pokémon Violet save verification
-   [ ] Verify Pokémon Legends: Z-A save format
-   [ ] Implement Z-A save reader after format verification

### Python Code Quality

-   [x] `pyproject.toml`
-   [x] Ruff formatter
-   [x] Ruff linting
-   [x] Ruff import sorting
-   [x] Pyright
-   [x] pytest dependency
-   [x] Python code passes Ruff
-   [x] Python code passes Pyright

### Documentation

-   [x] Existing README
-   [x] Existing AGENTS guidance
-   [x] Existing roadmap
-   [x] Documentation structure
-   [x] Synchronize README, AGENTS.md, and ROADMAP.md with current
    implementation
-   [ ] Audit detailed `docs/` pages against current implementation

------------------------------------------------------------------------

## 3. Milestone 1 --- Foundation

**Status: Complete**

### Objectives

-   Establish the Python project.
-   Configure Discord Rich Presence.
-   Create the initial modular structure.
-   Support configurable game definitions.
-   Provide basic runtime lifecycle.

### Completed

``` text
main.py
rpc/
games/base.py
games/registry.py
games/state.py
config.json
```

The session timer remains part of the Discord RPC behavior.

------------------------------------------------------------------------

## 4. Milestone 2 --- Eden & Game Detection

**Status: Complete for currently verified games**

### Objectives

-   Detect Eden.
-   Identify the active Pokémon game.
-   Keep game IDs stable.
-   Separate detection from game configuration.

### Current approach

``` text
eden.exe
  ↓
Windows process detection
  ↓
Eden window title
  ↓
Game title mapping
  ↓
Stable game ID
```

### Current game IDs

``` text
pokemon_legends_arceus
pokemon_scarlet
pokemon_violet
pokemon_legends_za
```

Future detection improvements should only be added when the title-based
approach becomes insufficient.

------------------------------------------------------------------------

## 5. Milestone 3 --- PKHeX Save Bridge

**Status: Core implemented**

### Objectives

-   Resolve Eden save paths.
-   Invoke a dedicated C# bridge.
-   Use PKHeX.Core for save parsing.
-   Return structured JSON.
-   Keep all operations read-only.

### Completed

``` text
Python SaveReader
      ↓
PokemonSaveReader
      ↓
PKHeX.Core
      ↓
JSON
```

### Verified data

#### Pokémon Legends: Arceus

-   Save type.
-   Trainer data.
-   Playtime.
-   Hisui Pokédex count.
-   Party/box extraction through the common PKHeX abstractions where
    applicable.

#### Pokémon Scarlet

-   Save type.
-   Trainer data.
-   Playtime.
-   Pokédex seen/caught counts.
-   Party.
-   Boxes.
-   Location ID.
-   Human-readable location name.
-   Player coordinates.

A verified Scarlet save currently resolves `LocationID 86` to `Artazon`.

------------------------------------------------------------------------

## 6. Milestone 4 --- Python Code Quality & Developer Tooling

**Status: Complete**

### Completed

-   [x] `requirements.txt`
-   [x] `requirements-dev.txt`
-   [x] Ruff
-   [x] Ruff formatter
-   [x] Ruff linting
-   [x] Ruff import sorting
-   [x] Pyright
-   [x] pytest installed
-   [x] `pyproject.toml` tooling configuration

### Developer CLI

**Status: Implemented**

The project provides:

``` text
dev.py
```

Implemented commands:

``` text
check
format
lint
typecheck
test
build
run
save
clean
all
```

Goals:

-   [x] Provide one consistent developer interface.
-   [x] Run Python and C# tasks from the repository root.
-   [x] Preserve subprocess exit codes.
-   [x] Stop command groups at the first failing subprocess.
-   [x] Report missing executables and failed subprocesses clearly.
-   [x] Avoid hardcoded user paths.
-   [x] Keep the CLI dependency-light.

------------------------------------------------------------------------

## 7. Milestone 5 --- Automated Testing

**Status: In Progress**

Convert the current manual test scripts into proper automated tests
while retaining useful integration tests.

### Completed

-   [x] Initial pytest setup.
-   [x] Developer CLI tests (`test/test_dev.py`).

### Planned test areas

``` text
Unit Tests
├── Detector
├── Save Path Resolver
├── State Parser
├── State Formatter
└── Registry

Integration Tests
├── C# Bridge
├── Arceus save fixture
└── Scarlet/Violet save fixtures
```

### Goals

-   Test successful reads.
-   Test missing files.
-   Test unsupported saves.
-   Test malformed bridge output.
-   Test state parsing.
-   Test location parsing.
-   Test RPC formatting without requiring Discord where possible.

Real emulator save files must not be committed.

------------------------------------------------------------------------

## 8. Milestone 6 --- GameState & Dynamic RPC Integration

**Status: Partially implemented**

The common `GameState` and save-data parser already exist. The remaining
work is to connect the richer state to Discord Rich Presence cleanly.

### Current state

Available in `GameState`:

``` text
game_id
playtime_seconds
pokedex
location
party
boxes
```

### Remaining work

-   [ ] Decide the final RPC layout.
-   [ ] Display actual location.
-   [ ] Display actual Pokédex progress.
-   [ ] Use save-derived state without unnecessary updates.
-   [ ] Preserve the session timer.
-   [ ] Ensure RPC is cleared when the game closes.
-   [ ] Keep RPC-specific formatting outside save readers.

------------------------------------------------------------------------

## 9. Milestone 7 --- Pokédex Accuracy

**Status: In progress**

Pokédex support needs game-specific handling.

### Goals

-   [x] Seen count for currently supported data.
-   [x] Caught count for currently supported data.
-   [ ] Correct regional dex totals.
-   [ ] Correct DLC/local dex handling where applicable.
-   [ ] Avoid counting species that should not belong to the selected
    dex.
-   [ ] Audit Blueberry/revision behavior in Scarlet/Violet.

For each game:

``` text
Save
  ↓
Game-specific Pokédex abstraction
  ↓
Verified counts
  ↓
GameState
```

The implementation must follow the actual game/PKHeX data model.

------------------------------------------------------------------------

## 10. Milestone 8 --- Pokémon Legends: Arceus

**Status: Save reader implemented**

### Current verified data

-   Save type.
-   Trainer name.
-   Trainer ID.
-   Playtime.
-   Hisui Pokédex count.

### Future data

-   [ ] Current location.
-   [ ] Research level.
-   [ ] Perfect entries.
-   [ ] Party Pokémon.
-   [ ] Active mission/progression.
-   [ ] More detailed Pokédex statistics.

Each additional field requires verification against the save
abstraction.

------------------------------------------------------------------------

## 11. Milestone 9 --- Pokémon Scarlet

**Status: Save reader implemented**

### Current verified data

-   Save type.
-   Trainer name.
-   Trainer ID.
-   Playtime.
-   Pokédex seen count.
-   Pokédex caught count.
-   Party Pokémon.
-   Box Pokémon.
-   Location ID.
-   Location name.
-   Player coordinates.

### Remaining work

-   [ ] Refine total Pokédex representation.
-   [ ] Audit DLC/local dex behavior.
-   [ ] Integrate location into RPC.
-   [ ] Integrate party data into RPC.
-   [ ] Integrate richer state into RPC.

------------------------------------------------------------------------

## 12. Milestone 10 --- Pokémon Violet

**Status: Detection configured; save-reader verification pending**

### Planned work

1.  Obtain a valid Violet save.
2.  Verify Eden save path/title ID.
3.  Verify PKHeX save detection.
4.  Verify trainer data.
5.  Verify playtime.
6.  Verify Pokédex structure.
7.  Verify party/box data.
8.  Verify location data.
9.  Reuse or add game-specific parsing where necessary.
10. Test end-to-end state and RPC behavior.

Do not mark Violet save support complete until the save reader has been
tested.

------------------------------------------------------------------------

## 13. Milestone 11 --- Pokémon Legends: Z-A

**Status: Detection mapping exists; save support pending verification**

Z-A requires format-specific research.

Before implementation:

-   Verify release/runtime version.
-   Verify Eden support.
-   Verify title ID.
-   Identify save location.
-   Verify PKHeX support.
-   Inspect the actual save abstraction.
-   Test with a valid save.

If PKHeX does not expose the required data, do not invent a binary
parser.

------------------------------------------------------------------------

## 14. Milestone 12 --- Better Game Registry

**Status: Planned**

The registry should eventually become the central source of game
capabilities.

Potential model:

``` text
GameDefinition
├── id
├── name
├── region
├── artwork
├── detector rules
└── save reader capabilities
```

The goal is to make adding a new game predictable without modifying
unrelated modules.

------------------------------------------------------------------------

## 15. Milestone 13 --- Save Reader Abstraction Refinement

**Status: Partially implemented**

Current C# abstraction already supports game-specific readers.

Target structure:

``` text
ISaveReader
├── LegendsArceusReader
├── ScarletVioletReader
└── ZASaveReader
```

The Python layer should not need to know binary save structures.

Game-specific parsing belongs in the bridge / PKHeX layer where
appropriate.

------------------------------------------------------------------------

## 16. Milestone 14 --- Runtime Optimization

**Status: Planned**

Goals:

-   Reduce unnecessary save parsing.
-   Avoid unnecessary process launches.
-   Cache stable save paths where appropriate.
-   Avoid unnecessary RPC updates.
-   Keep CPU usage low.
-   Keep the application responsive.

Target pattern:

``` text
Fast polling
    ↓
Process / game detection
    ↓
State change check
    ↓
Save read only when required
    ↓
RPC update only when changed
```

Optimization should follow measurement rather than premature complexity.

------------------------------------------------------------------------

## 17. Milestone 15 --- Better Logging

**Status: Planned**

Potential improvements:

-   Structured logging.
-   Log levels.
-   Debug mode.
-   Concise normal output.
-   Useful error messages.
-   Optional log file.

Do not log save contents or unnecessary personal data.

------------------------------------------------------------------------

## 18. Milestone 16 --- Configuration Improvements

**Status: Planned**

Potential improvements:

-   Configuration validation.
-   Optional local configuration.
-   Clearer error messages.
-   Default values.
-   Schema validation.
-   Per-game capabilities.

Configuration should remain separate from implementation logic.

------------------------------------------------------------------------

## 19. Milestone 17 --- Packaging

**Status: Planned**

Possible distribution formats:

-   Standalone Windows executable.
-   Packaged Python application.
-   Installer.
-   Portable release.

Packaging must account for:

-   Python runtime.
-   .NET bridge.
-   PKHeX dependency/licensing requirements.
-   Configuration.
-   Discord Application ID.
-   Required Windows components.

Do not package local development artifacts.

------------------------------------------------------------------------

## 20. Milestone 18 --- Release Readiness

**Status: Planned**

Before a public release:

### Functionality

-   [ ] Eden detection stable.
-   [ ] Supported game detection verified.
-   [ ] Supported save readers verified.
-   [ ] GameState integration complete.
-   [ ] RPC lifecycle stable.
-   [ ] Reconnection tested.
-   [ ] Shutdown cleanup tested.

### Reliability

-   [ ] Invalid save handled safely.
-   [ ] Missing save handled safely.
-   [ ] Discord unavailable handled safely.
-   [ ] Eden unavailable handled safely.
-   [ ] Bridge failure handled safely.

### Testing

-   [ ] Automated tests pass.
-   [ ] Integration tests pass on supported fixtures.
-   [ ] Release build verified.

### Documentation

-   [ ] README accurate.
-   [ ] Setup instructions tested.
-   [ ] Configuration documented.
-   [ ] Supported games documented.
-   [ ] Troubleshooting documented.
-   [ ] Licensing reviewed.
-   [ ] Third-party dependencies documented.

### Repository

-   [ ] No save files.
-   [ ] No emulator data.
-   [ ] No credentials.
-   [ ] No build artifacts.
-   [ ] No local PKHeX source.
-   [ ] `.gitignore` verified.

------------------------------------------------------------------------

## 21. Future Feature Ideas

These are ideas, not committed requirements.

### Rich Presence

-   Dynamic location.
-   Dynamic Pokédex.
-   Trainer name.
-   Save playtime.
-   Party information.
-   Current objective.
-   Progression.
-   Game-specific details.

### Artwork

-   Game-specific artwork.
-   Regional artwork.
-   Dynamic Pokémon artwork.
-   Party Pokémon icons.

### Application

-   Tray application.
-   GUI configuration.
-   Auto-start.
-   Logging panel.
-   Diagnostics page.
-   Configurable polling interval.

### Multi-Game

-   Additional Pokémon Switch titles.
-   Future game definitions.
-   Automatic capability detection.

Every new feature must preserve the project's read-only design.

------------------------------------------------------------------------

## 22. Non-Goals

The project does not intend to:

-   Modify Pokémon saves.
-   Write save files.
-   Bypass Nintendo security.
-   Access Nintendo Online services.
-   Bypass DRM.
-   Manipulate HOME/security systems.
-   Automate gameplay.
-   Provide cheating functionality.

The application is intended to observe local game state and expose it
through Discord Rich Presence.

------------------------------------------------------------------------

## 23. Development Priorities

When deciding what to implement next, prioritize:

1.  Correctness.
2.  Read-only safety.
3.  Verified save data.
4.  Stable game detection.
5.  Maintainable architecture.
6.  Reliable RPC behavior.
7.  Performance.
8.  Visual polish.

A missing feature is preferable to an inaccurate feature.

------------------------------------------------------------------------

## 24. Research Policy

Before implementing undocumented game data:

``` text
Question
  ↓
Check current documentation
  ↓
Check official documentation/source
  ↓
Inspect local PKHeX source
  ↓
Verify game/save version
  ↓
Test with real save
  ↓
Implement
```

Never convert an assumption into production behavior without
verification.

------------------------------------------------------------------------

## 25. Roadmap Status Legend

Use:

``` text
[x] Complete
[ ] Planned / incomplete
```

For game support, distinguish:

``` text
Detection
Save Reader
Runtime Integration
```

A game should not be described as fully supported when only detection
has been implemented.

------------------------------------------------------------------------

## 26. Related Documentation

-   `README.md`
-   `AGENTS.md`
-   `docs/ARCHITECTURE.md`
-   `docs/DEVELOPMENT.md`
-   `docs/CONFIGURATION.md`
-   `docs/SAVE-READER.md`
-   `docs/GAME-SUPPORT.md`
-   `docs/DISCORD-RPC.md`
-   `docs/TROUBLESHOOTING.md`
