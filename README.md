# Pokémon Switch RPC

> Discord Rich Presence for Pokémon games running through the Eden emulator.

Pokémon Switch RPC is a modular Discord Rich Presence application that detects Pokémon games running through the **Eden Nintendo Switch emulator** and displays game information on Discord.

The project is designed to read supported Pokémon save files through **PKHeX.Core**, allowing the Rich Presence to display information such as playtime and Pokédex progress without modifying the save data.

<!-- IMAGE: Add a project banner / hero image here -->
<!-- Suggested: 1280×640 PNG showing Pokémon Switch RPC + Discord Rich Presence -->

## ✨ Features

- 🎮 Automatically detect Pokémon games running through Eden
- 🎯 Identify the currently running game from the Eden window
- 💬 Discord Rich Presence integration
- ⏱️ Session elapsed time
- 💾 Read Pokémon save data through PKHeX.Core
- 📖 Read Pokédex progress from supported save files
- 🕐 Read playtime from save data
- 👤 Read trainer information
- 🧩 Modular game definitions and save readers
- 🔒 Read-only save access — save files are never modified
- ⚙️ JSON-based configuration
- 🔌 Designed to support additional Pokémon games in the future

---

## 🎮 Supported Games

| Game | Eden Detection | Save Reader | Pokédex | Playtime |
|---|:---:|:---:|:---:|:---:|
| Pokémon Legends: Arceus | ✅ | ✅ | ✅ | ✅ |
| Pokémon Scarlet | ✅ | ✅ | ✅ | ✅ |
| Pokémon Violet | ✅ | 🚧 | 🚧 | 🚧 |
| Pokémon Legends: Z-A | 🚧 | 🚧 | 🚧 | 🚧 |

> Support for a game is implemented independently. A game may be detectable by Eden before its save data reader is available.

---

## 📸 Preview

<!-- IMAGE: Discord Rich Presence screenshot -->
<!-- Suggested: Screenshot showing Pokémon Legends: Arceus / Pokémon Scarlet Rich Presence -->

### Pokémon Legends: Arceus

<!-- IMAGE: Add screenshot here -->

### Pokémon Scarlet

<!-- IMAGE: Add screenshot here -->

---

## 🏗️ Architecture

The project separates game detection, save reading, game state, and Discord RPC into independent components.

```text
                         Eden Emulator
                               │
                               ▼
                       ┌────────────────┐
                       │ Game Detector  │
                       └───────┬────────┘
                               │
                               ▼
                       ┌────────────────┐
                       │ Game Registry  │
                       └───────┬────────┘
                               │
                               ▼
                       ┌────────────────┐
                       │ Save Path      │
                       │ Resolver       │
                       └───────┬────────┘
                               │
                               ▼
                       ┌────────────────┐
                       │ Python Save    │
                       │ Reader         │
                       └───────┬────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ PokemonSaveReader     │
                    │ (.NET / C#)           │
                    └──────────┬───────────┘
                               │
                               ▼
                         ┌─────────────┐
                         │ PKHeX.Core  │
                         └──────┬──────┘
                                │
                                ▼
                              JSON
                                │
                                ▼
                         ┌─────────────┐
                         │  GameState  │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Discord RPC │
                         └─────────────┘
```

## Project Structure

```text
pokemon-switch-rpc/
│
├── main.py
├── config.json
├── requirements.txt
├── .gitignore
│
├── games/
│   ├── base.py
│   ├── registry.py
│   ├── detector.py
│   ├── state.py
│   ├── save_paths.py
│   ├── save_reader.py
│   └── game_save_reader.py
│
├── rpc/
│   └── discord_rpc.py
│
├── bridge/
│   └── PokemonSaveReader/
│       ├── PokemonSaveReader.csproj
│       └── Program.cs
│
├── test/
│   ├── game_detection.py
│   ├── game_save_reader.py
│   └── save_path.py
│
└── docs/
    └── ...
```

## 🔧 Requirements

**Software**
- Windows 11
- Python 3.9+
- .NET SDK 10+
- Discord desktop application
- Eden emulator
- A supported Pokémon game

**Python Dependencies**

The Python application uses:
- [PyPresence](https://github.com/qwertyquerty/pypresence) — Discord Rich Presence
- `psutil` — process detection
- `pywin32` — Windows window/process information
Install them with:
```bash
pip install -r requirements.txt
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ramadhafidz/emulator-switch-discordrpc.git pokemon-switch-rpc
cd pokemon-switch-rpc
```

2. **Create a Python virtual environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PKHeX.Core**
This project uses **PKHeX.Core** as an external dependency for Pokémon save parsing.
PKHeX source is intentionally **not included in this repository.**
The expected local structure is:
```text
pokemon-switch-rpc/
└── bridge/
    ├── PKHeX/
    │   └── PKHeX.Core/
    │
    └── PokemonSaveReader/
        ├── PokemonSaveReader.csproj
        └── Program.cs
```
Obtain PKHeX separately and place the source at:
```text
bridge/PKHeX/
```
> PKHeX is a third-party project and is not distributed as part of this repository.

5. **Build the save reader bridge**
Restore dependencies:
```bash
dotnet restore bridge/PokemonSaveReader/PokemonSaveReader.csproj
```

Build:
```bash
dotnet build bridge/PokemonSaveReader/PokemonSaveReader.csproj
```

6. **Configure Discord**
Create a Discord application and obtain its Application ID.

Then configure:
```json
{
	"discord": {
		"client_id": "YOUR_DISCORD_APPLICATION_ID",
		"update_interval": 15
	}
}
```
See [Configuration](docs/CONFIGURATION.md) for more information.

## ▶️ Usage
Start Discord first, then launch Eden and a supported Pokémon game.

Run:
```bash
python main.py
```

The application will:
1. Detect the Eden process.
2. Detect the currently running Pokémon game.
3. Locate the game's save file.
4. Read supported save data.
5. Build the current `GameState`.
6. Update Discord Rich Presence.
7. Clear the Rich Presence when the game closes.

Example:
```text
Pokémon Switch RPC started.
Connecting to Discord...
Discord RPC connected.
Eden: running
Game detected: Pokémon Legends: Arceus
Rich Presence updated.
```

## 💾 Save Data
Save files are accessed in read-only mode.

The project does not:
- Modify save files
- Write Pokémon data
- Inject data into the game
- Bypass Nintendo online services
- Modify emulator security mechanisms
- Upload save data to external services

Save parsing is performed locally through PKHeX.Core.

The project intentionally avoids manually guessing save offsets. Game-specific save structures should be based on verified implementations from PKHeX or other reliable documentation.

## 🧩 Game-Specific Save Readers
Different Pokémon games use different save formats.

The bridge currently identifies supported save formats through PKHeX:
```text
SaveUtil.GetSaveFile()
        │
        ├── SAV8LA
        │     └── Pokémon Legends: Arceus
        │
        └── SAV9SV
              └── Pokémon Scarlet / Violet
```

The resulting data is converted into a common JSON structure before being consumed by the Python application.

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

> The exact fields may evolve as support for additional games and save data is implemented.

## ⚙️ Configuration
Game-specific Rich Presence settings are stored in `config.json`.

Example:
```json
{
	"games": {
		"pokemon_scarlet": {
			"name": "Pokémon Scarlet",
			"region": "Paldea",
			"large_image": "scarlet",
			"large_text": "Pokémon Scarlet"
		}
	}
}
```

Each game can define its:
- Display name
- Region
- Discord artwork
- Artwork tooltip

More configuration options may be added as the project develops.

## 🧪 Testing
Individual components can be tested independently.

Game detection:
```bash
python test/game_detection.py
```

Save path resolution:
```bash
python test/save_path.py
```

Game save reading:
```bash
python test/game_save_reader.py
```

The C# bridge can also be tested directly:
```bash
dotnet run --project bridge/PokemonSaveReader -- "<path-to-save>"
```

## 🗺️ Roadmap
Foundation
- [x] Discord Rich Presence
- [x] Discord Application configuration
- [x] Custom Discord artwork
- [x] Elapsed session timer
- [x] Modular game configuration

Eden Integration
- [x] Eden process detection
- [x] Eden window detection
- [x] Pokémon game detection
- [x] Multiple game definitions

Save Reader
- [x] PKHeX.Core integration
- [x] Pokémon Legends: Arceus save detection
- [x] Pokémon Scarlet save detection
- [x] PLA playtime
- [x] SV playtime
- [x] PLA Pokédex
- [x] SV Pokédex
- [x] Trainer information

Discord Integration
- [ ] Connect save data to GameState
- [ ] Display actual Pokédex progress
- [ ] Display save playtime
- [ ] Display location
- [ ] Display current party Pokémon
- [ ] Improve game-specific Rich Presence

Additional Games
- [ ] Pokémon Violet
- [ ] Pokémon Legends: Z-A
- [ ] Additional Pokémon games where technically feasible

## 📚 Documentation
Detailed documentation is available in the `docs/` directory.
- [Architecture](docs/ARCHITECTURE.md)
- [Development Setup](docs/DEVELOPMENT.md)
- [Configuration](docs/CONFIGURATION.md)
- [Save Reader](docs/SAVE-READER.md)
- [Game Support](docs/GAME-SUPPORT.md)
- [Discord RPC](docs/DISCORD-RPC.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Roadmap](docs/ROADMAP.md)

> Documentation pages are being developed alongside the project.

## 🤝 Contributing
Contributions, bug reports, and suggestions are welcome.

Before contributing, please read:

[CONTRIBUTING.md](CONTRIBUTING.md)

When working with Pokémon save formats:
- Use verified save structure information.
- Do not guess offsets.
- Keep save access read-only.
- Keep game-specific logic modular.
- Avoid introducing user-specific absolute paths.
- Do not commit emulator save files.
- Do not commit third-party PKHeX source.

## ⚖️ Third-Party Software
This project uses third-party software and libraries, including:

**PKHeX**
PKHeX is used for Pokémon save file parsing.
PKHeX is developed by the PKHeX contributors and is licensed under the GNU General Public License v3.0.
PKHeX source is not included in this repository and must be obtained separately.

**PyPresence**
Used for Discord Rich Presence communication.
See the project's repository for its license and terms.

**Eden Emulator**
Used as the Nintendo Switch emulator whose process and window are detected by this application.
This project is not affiliated with or endorsed by Eden or The Pokémon Company.

## ⚠️ Disclaimer
Pokémon and related names, characters, and assets are trademarks of their respective owners.

This project is a fan-made, independent software project and is not affiliated with, endorsed by, or sponsored by:
- Nintendo
- The Pokémon Company
- Game Freak
- Eden

Use of this project is at your own discretion.

## 📄 License
The licensing terms for this project are currently being determined.

Third-party dependencies retain their respective licenses.

See the documentation for information about third-party software and dependencies.