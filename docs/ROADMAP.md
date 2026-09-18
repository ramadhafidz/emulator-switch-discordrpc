# ROADMAP.md

Development roadmap for **Pokémon Switch RPC**.

The project is a modular, read-only Discord Rich Presence application for Pokémon games running through the Eden emulator.

------------------------------------------------------------------------

## 1. Project Vision

The long-term goal is to provide a lightweight Rich Presence application that automatically detects which supported Pokémon game is running and exposes useful, verified game state to Discord.

Target flow:
`Eden -> Game Detector -> Save Resolver -> PKHeX Save Reader (.NET) -> GameState (Python) -> Discord RPC`

------------------------------------------------------------------------

## 2. Current Capabilities

The foundation of the project is solid and currently supports:

- **Eden Emulator Detection:** Automatically detects Eden and identifies the running Pokémon game via window enumeration.
- **Python / C# Architecture:** A clean bridge between the Python lifecycle manager and the C# PKHeX save reader.
- **Verified Save Reading:** Extracts trainer data, playtime, and specific game states for **Pokémon Legends: Arceus** and **Pokémon Scarlet**.
- **Developer Tooling:** Automated testing (pytest), strict formatting/linting (Ruff), static typing (Pyright), and a unified developer CLI (`dev.py`).

------------------------------------------------------------------------

## 3. Roadmap

We organize our planned work into **Now**, **Next**, and **Later** phases.

### 🏃 Now (In Progress)
Work currently being actively developed.

- **Dynamic RPC Integration:** Connect the newly expanded `GameState` (location, party, boxes) cleanly to Discord Rich Presence without unnecessary updates.
- **Pokédex Accuracy:** Implement game-specific Pokédex logic to accurately reflect regional, DLC, and total seen/caught counts without guessing.
- **Automated Testing Expansion:** Increase test coverage for the Python-C# integration and specific save-reading edge cases.

### 📅 Next (Short-term)
Up next after current priorities are stabilized.

- **Pokémon Violet Support:** Verify the save path, title ID, and PKHeX save detection to bring Violet up to parity with Scarlet.
- **Game Registry Refinement:** Move towards a central `GameDefinition` registry that handles detection rules, region variants, and save reader capabilities predictably.
- **Save Reader Refinements:** Extract more verified data from *Pokémon Scarlet* (e.g., party/box parsing to RPC) and *Arceus* (e.g., current location, active missions).
- **Runtime Optimization:** Optimize the application loop to reduce CPU/memory overhead while waiting for Eden or parsing saves.
- **Logging Improvements:** Implement a cleaner logging architecture that differentiates between debug tracing and user-facing status updates.

### 🔭 Later (Long-term)
Planned milestones for the future.

- **Pokémon Legends: Z-A:** Add support once the game is released, its runtime environment in Eden is verified, and PKHeX supports its save format.
- **Packaging:** Create standalone, zero-dependency executable builds (e.g., using PyInstaller) for end-users.
- **Release Readiness:** Polish documentation, improve crash handling, finalize configuration formats, and prepare for a stable v1.0.0 release.
- **Configuration Overhaul:** Provide a robust user-configuration system for customizing update intervals, toggleable RPC fields, and UI preferences.

------------------------------------------------------------------------

## 4. Future Ideas

Concepts that are interesting but not currently prioritized or scheduled:

- **Rich Presence Assets:** Hosting dynamic images for locations, Pokémon, and badges.
- **Multi-Emulator Support:** Abstracting process detection to support emulators other than Eden.
- **GUI Application:** Providing a minimal system tray icon or local web interface for configuration, rather than relying solely on `config.json` and the CLI.

------------------------------------------------------------------------

## 5. Guiding Principles

To keep the project stable and safe, all roadmap items are bound by these rules:

1. **Read-Only Access:** The application will **never** modify, write, or inject data into save files.
2. **No Guesswork:** Save offsets, block sizes, and data structures must be verified against official documentation, reproducible analysis, or PKHeX implementations. If a structure is unknown, the feature remains unimplemented.
3. **No Embedded PKHeX Source:** PKHeX is an external dependency. The repository will never track PKHeX source code or modified PKHeX forks.
4. **Architectural Purity:** Prioritize correctness, save-data safety, and existing architectural boundaries over convenience or over-engineering.