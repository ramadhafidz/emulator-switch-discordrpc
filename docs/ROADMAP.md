# ROADMAP.md

Development roadmap for **Pokémon Switch RPC**.

The project is a modular, read-only Discord Rich Presence application for Pokémon games running through the Eden emulator.

---

## 1. Project Vision

The long-term goal is to provide a lightweight Rich Presence application that can automatically understand which supported Pokémon game is running and expose useful, verified game state.

Target architecture:

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
GameState
  ↓
Discord RPC
```

Save reading uses a C# bridge and PKHeX.Core:

```text
Eden
  ↓
Game Detector
  ↓
Game Definition
  ↓
Save Resolver
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

The application is intentionally read-only.

---

## 2. Current Status

### Foundation

- [x] Python project structure
- [x] Python virtual environment
- [x] Dependency configuration
- [x] Discord Application
- [x] Discord Client/Application ID configuration
- [x] PyPresence integration
- [x] Basic RPC wrapper
- [x] Configurable update interval
- [x] Game-specific artwork configuration
- [x] Elapsed session timestamp
- [x] RPC cleanup
- [x] Reconnection handling

### Eden Detection

- [x] Eden process detection
- [x] Eden window enumeration
- [x] Window title inspection
- [x] Pokémon Legends: Arceus detection
- [x] Pokémon Scarlet detection
- [x] Pokémon Violet mapping
- [x] Pokémon Legends: Z-A mapping
- [ ] Verify Z-A detection against the actual release/runtime environment

### Architecture

- [x] `GameDefinition`
- [x] `GameRegistry`
- [x] `GameState`
- [x] `SaveReader`
- [x] `GameSaveReader`
- [x] Eden save path resolver
- [x] Python → C# bridge
- [x] PKHeX.Core integration

### Save Reader

- [x] Pokémon Legends: Arceus save detection
- [x] Pokémon Legends: Arceus trainer data
- [x] Pokémon Legends: Arceus playtime
- [x] Pokémon Legends: Arceus Pokédex count
- [x] Pokémon Scarlet save detection
- [x] Pokémon Scarlet trainer data
- [x] Pokémon Scarlet playtime
- [x] Pokémon Scarlet Pokédex seen/caught count
- [ ] Refine Scarlet/Violet Pokédex total representation
- [ ] Complete Pokémon Violet save verification
- [ ] Verify Pokémon Legends: Z-A save format
- [ ] Implement Z-A save reader after format verification

### Documentation

- [x] README
- [x] Architecture documentation
- [x] Development documentation
- [x] Configuration documentation
- [x] Save reader documentation
- [x] Game support documentation
- [x] Discord RPC documentation
- [x] Troubleshooting documentation

---

## 3. Milestone 1 — Foundation

**Status: Complete**

Objectives:

- establish the Python project;
- configure Discord Rich Presence;
- create the initial modular structure;
- support configurable game definitions;
- provide basic runtime lifecycle.

Completed components:

```text
main.py
rpc/
games/base.py
games/registry.py
games/state.py
config.json
```

---

## 4. Milestone 2 — Eden & Game Detection

**Status: Complete for currently verified games**

Objectives:

- detect Eden;
- identify the active Pokémon game;
- keep game IDs stable;
- separate detection from game configuration.

Current approach:

```text
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

Future detection improvements should only be added when the existing title-based approach becomes insufficient.

---

## 5. Milestone 3 — Save Reader Foundation

**Status: In progress / core implemented**

Objectives:

- resolve Eden save paths;
- invoke a dedicated C# bridge;
- use PKHeX.Core for save parsing;
- return structured JSON;
- keep all operations read-only.

Completed:

```text
Python SaveReader
        ↓
PokemonSaveReader
        ↓
PKHeX.Core
        ↓
JSON
```

Next priorities:

1. improve data normalization;
2. refine Pokédex totals;
3. expose useful location data;
4. expose accurate playtime through `GameState`;
5. separate game-specific parsing cleanly.

---

## 6. Milestone 4 — GameState Integration

**Status: Next major integration stage**

The application currently has the `GameState` abstraction, but save-derived data needs to be integrated into the runtime flow more completely.

Target:

```text
Save Reader
    ↓
raw save data
    ↓
GameState
    ↓
RPC payload
```

Planned fields:

```text
game_id
playtime_seconds
pokedex_caught
pokedex_total
location
```

Potential future fields:

```text
pokedex_seen
trainer_name
current_map
party
progress
```

Only add fields when the source data is verified.

---

## 7. Milestone 5 — Dynamic Rich Presence

**Status: Planned**

Move from static game information toward dynamic game state.

Possible display:

```text
Pokémon Legends: Arceus
Exploring Hisui
Pokédex: 25 / 242
```

or:

```text
Pokémon Scarlet
Exploring Paldea
Pokédex: 25 / ...
```

Future state should be generated from actual save data rather than hardcoded values.

---

## 8. Milestone 6 — Location Support

**Status: Planned**

Add current player location where the save format exposes reliable location information.

Potential flow:

```text
Save
  ↓
Coordinates / Field ID / Location ID
  ↓
Game-specific resolver
  ↓
Human-readable location
  ↓
GameState.location
  ↓
Discord RPC
```

Location parsing must be game-specific.

Do not assume the same field structure exists across generations.

---

## 9. Milestone 7 — Pokédex Accuracy

**Status: In progress**

Pokédex support needs game-specific handling.

Goals:

- seen count;
- caught count;
- correct regional dex total;
- correct DLC dex handling where applicable;
- avoid counting species that should not belong to the selected dex.

For each game:

```text
Save
  ↓
Game-specific Pokédex abstraction
  ↓
Verified counts
  ↓
GameState
```

The implementation must follow the actual game/PKHeX data model.

---

## 10. Milestone 8 — Pokémon Legends: Arceus

**Status: Save reader implemented**

Current verified data:

- save type;
- trainer name;
- trainer ID;
- playtime;
- Hisui Pokédex count.

Potential future data:

- current location;
- research level;
- perfect entries;
- party Pokémon;
- active mission/progression;
- more detailed Pokédex statistics.

Each additional field requires verification against the save abstraction.

---

## 11. Milestone 9 — Pokémon Scarlet

**Status: Save reader implemented**

Current verified data:

- save type;
- trainer name;
- trainer ID;
- playtime;
- Pokédex seen count;
- Pokédex caught count.

Next:

- refine total Pokédex representation;
- verify DLC/local dex behavior;
- add location;
- integrate state into RPC.

---

## 12. Milestone 10 — Pokémon Violet

**Status: Detection configured; save reader verification pending**

Planned work:

1. obtain a valid Violet save;
2. verify Eden save path/title ID;
3. verify PKHeX save detection;
4. verify trainer data;
5. verify playtime;
6. verify Pokédex structure;
7. add or reuse game-specific parsing;
8. test end-to-end RPC.

Do not mark Violet save support complete until the save reader has been tested.

---

## 13. Milestone 11 — Pokémon Legends: Z-A

**Status: Detection mapping exists; save support pending verification**

Z-A requires format-specific research.

Before implementation:

- verify release/runtime version;
- verify Eden support;
- verify title ID;
- identify save location;
- verify PKHeX support;
- inspect the actual save abstraction;
- test with a valid save.

If PKHeX does not yet expose the required data, do not invent a binary parser.

---

## 14. Milestone 12 — Better Game Registry

**Status: Planned**

The registry should eventually become the central source of game capabilities.

Potential model:

```text
GameDefinition
├── id
├── name
├── region
├── artwork
├── detector rules
└── save reader capabilities
```

The goal is to make adding a new game predictable without modifying unrelated modules.

---

## 15. Milestone 13 — Save Reader Abstraction

**Status: Partially implemented**

Target architecture:

```text
SaveReader
├── ArceusSaveReader
├── ScarletSaveReader
├── VioletSaveReader
└── ZASaveReader
```

The Python layer should not need to know binary save structures.

Game-specific parsing belongs in the bridge / PKHeX layer where appropriate.

---

## 16. Milestone 14 — Runtime Optimization

**Status: Planned**

Goals:

- reduce unnecessary save parsing;
- avoid unnecessary process launches;
- cache stable paths;
- avoid unnecessary RPC updates;
- keep CPU usage low;
- keep the application responsive.

Potential architecture:

```text
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

---

## 17. Milestone 15 — Better Logging

**Status: Planned**

Current development uses console output.

Potential improvements:

- structured logging;
- log levels;
- debug mode;
- concise normal output;
- useful error messages;
- optional log file.

Do not log save contents or unnecessary personal data.

---

## 18. Milestone 16 — Configuration Improvements

**Status: Planned**

Potential improvements:

- configuration validation;
- optional local configuration;
- clearer error messages;
- default values;
- schema validation;
- per-game capabilities.

Configuration should remain separate from implementation logic.

---

## 19. Milestone 17 — Packaging

**Status: Planned**

Possible distribution formats:

- standalone Windows executable;
- packaged Python application;
- installer;
- portable release.

Packaging must account for:

- Python runtime;
- .NET bridge;
- PKHeX dependency/licensing requirements;
- configuration;
- Discord Application ID;
- required Windows components.

Do not package local development artifacts.

---

## 20. Milestone 18 — Automated Testing

**Status: Planned**

Current testing is primarily manual and focused scripts.

Future testing:

```text
Unit tests
    ↓
Mocked detector tests
    ↓
Save reader fixture tests
    ↓
Bridge tests
    ↓
Integration tests
```

Save fixtures must not contain unnecessary private data.

Tests should verify both successful reads and failure handling.

---

## 21. Milestone 19 — Release Readiness

Before a public release:

### Functionality

- [ ] Eden detection stable
- [ ] Supported game detection verified
- [ ] Save readers verified
- [ ] GameState integration complete
- [ ] RPC lifecycle stable
- [ ] Reconnection tested
- [ ] Shutdown cleanup tested

### Reliability

- [ ] Invalid save handled safely
- [ ] Missing save handled safely
- [ ] Discord unavailable handled safely
- [ ] Eden unavailable handled safely
- [ ] Bridge failure handled safely

### Documentation

- [ ] README accurate
- [ ] Setup instructions tested
- [ ] Configuration documented
- [ ] Supported games documented
- [ ] Troubleshooting documented
- [ ] Licensing reviewed
- [ ] Third-party dependencies documented

### Repository

- [ ] No save files
- [ ] No emulator data
- [ ] No credentials
- [ ] No build artifacts
- [ ] No local PKHeX source
- [ ] `.gitignore` verified

---

## 22. Future Feature Ideas

These are ideas, not committed requirements.

### Rich Presence

- dynamic location;
- dynamic Pokédex;
- trainer name;
- playtime;
- party information;
- current objective;
- progression;
- game-specific details.

### Artwork

- game-specific artwork;
- regional artwork;
- dynamic Pokémon artwork;
- party Pokémon icons.

### Application

- tray application;
- GUI configuration;
- auto-start;
- logging panel;
- diagnostics page;
- configurable polling interval.

### Multi-Game

- additional Pokémon Switch titles;
- future game definitions;
- automatic capability detection.

Every new feature must preserve the project's read-only design.

---

## 23. Non-Goals

The project does not intend to:

- modify Pokémon saves;
- write save files;
- bypass Nintendo security;
- access Nintendo Online services;
- bypass DRM;
- manipulate HOME/security systems;
- automate gameplay;
- provide cheating functionality.

The application is intended to observe local game state and expose it through Discord Rich Presence.

---

## 24. Development Priorities

When deciding what to implement next, prioritize:

1. correctness;
2. read-only safety;
3. verified save data;
4. stable game detection;
5. maintainable architecture;
6. reliable RPC behavior;
7. performance;
8. visual polish.

A missing feature is preferable to an inaccurate feature.

---

## 25. Research Policy

Before implementing undocumented game data:

```text
Question
  ↓
Check Context7
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

Never convert an assumption into production behavior without verification.

---

## 26. Roadmap Status Legend

Use:

```text
[x] Complete
[ ] Planned / incomplete
```

For game support, distinguish:

```text
Detection
Save Reader
Runtime Integration
```

A game should not be described as fully supported when only detection has been implemented.

---

## 27. Related Documentation

- `README.md`
- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/CONFIGURATION.md`
- `docs/SAVE-READER.md`
- `docs/GAME-SUPPORT.md`
- `docs/DISCORD-RPC.md`
- `docs/TROUBLESHOOTING.md`
