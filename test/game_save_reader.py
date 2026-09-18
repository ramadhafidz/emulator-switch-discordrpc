import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from games.game_save_reader import GameSaveReader

BRIDGE_PATH = "bridge/PokemonSaveReader/bin/Debug/net10.0/PokemonSaveReader.dll"


def print_game_state(reader: GameSaveReader, game_id: str, label: str):
	print(f"=== {label} ===")

	result = reader.read_game(game_id)

	if result is None:
		print(f"Failed to read {label} save.")
		return

	print("Success: True")
	print(f"Game: {result.game_id}")

	if result.playtime_seconds is not None:
		hours = result.playtime_seconds // 3600
		minutes = (result.playtime_seconds % 3600) // 60
		seconds = result.playtime_seconds % 60

		print(f"Playtime: {hours:02d}:{minutes:02d}:{seconds:02d}")

	if result.location is not None:
		print(f"Location: {result.location.name or 'Unknown'}")

		print(f"Location ID: {result.location.location_id}")

		print(
			f"Coordinates: "
			f"{result.location.x}, "
			f"{result.location.y}, "
			f"{result.location.z}"
		)

	if result.pokedex:
		for name, dex in result.pokedex.items():
			print(f"Pokédex ({name}): {dex.caught} / {dex.total}")

	print()


def main():
	reader = GameSaveReader(BRIDGE_PATH)

	print_game_state(reader, "pokemon_legends_arceus", "ARCEUS")

	print_game_state(reader, "pokemon_scarlet", "SCARLET")


if __name__ == "__main__":
	main()
