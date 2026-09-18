# TODO

This file tracks granular, actionable tasks for **Pokémon Switch RPC**.
For the high-level project vision and long-term milestones, see `docs/ROADMAP.md`.

## 🏃 Active Sprint

### Discord RPC & GameState
- [ ] Finalize the Discord RPC UI layout (decide which fields show where).
- [ ] Display real-time location data in RPC.
- [ ] Display actual Pokédex progress in RPC.
- [ ] Ensure Discord RPC is reliably cleared when the game/emulator closes.
- [ ] Integrate party and box data into the rich presence visually (if applicable).

### Pokédex Accuracy
- [ ] Implement correct regional dex totals for supported games.
- [ ] Handle DLC/local dex accurately (e.g., Kitakami, Blueberry in Scarlet).
- [ ] Prevent counting species that do not belong to the selected Pokédex.

---

## 🎮 Game Support

### Pokémon Violet
- [ ] Obtain and test with a valid Violet save file.
- [ ] Verify Eden save path and title ID for Violet.
- [ ] Verify trainer data, playtime, and location extraction via PKHeX.
- [ ] Test end-to-end state and RPC behavior.

### Pokémon Scarlet (Refinements)
- [ ] Refine total Pokédex representation (base vs DLC).
- [ ] Integrate party data into the Python GameState / RPC.
- [ ] Integrate rich location names into the RPC.

### Pokémon Legends: Arceus (Refinements)
- [ ] Extract current location/map.
- [ ] Extract research level and perfect Pokédex entries.
- [ ] Extract party Pokémon.
- [ ] Extract active mission/progression.

### Pokémon Legends: Z-A
- [ ] Verify Eden support and title ID upon game release.
- [ ] Verify PKHeX support for the new save format.
- [ ] Implement and verify the C# save reader.

---

## 🛠️ Architecture & Tech Debt

### Game Registry
- [ ] Move game detection rules into a centralized `GameDefinition` registry.
- [ ] Centralize artwork and region configurations per game.

### Performance & Logging
- [ ] Optimize the main application loop to reduce CPU overhead while waiting for Eden.
- [ ] Implement a clearer logging architecture (separate debug logs from user-facing info).
- [ ] Improve error recovery without crashing (e.g., when a save file is temporarily locked by the emulator).

### Testing
- [ ] Write pytest tests for Python-to-C# JSON parsing.
- [ ] Add unit tests for specific edge cases in `GameState`.
