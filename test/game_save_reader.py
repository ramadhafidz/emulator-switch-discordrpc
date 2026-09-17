import sys
from pathlib import Path

sys.path.insert(
	0,
	str(Path(__file__).resolve().parent.parent)
)

from games.game_save_reader import GameSaveReader


BRIDGE_PATH = (
	"bridge/PokemonSaveReader/bin/Debug/net10.0/"
	"PokemonSaveReader.dll"
)


def main():
	reader = GameSaveReader(BRIDGE_PATH)

	print("=== ARCEUS ===")

	result = reader.read_game(
		"pokemon_legends_arceus"
	)

	if result is None:
		print("Failed to read Arceus save.")
		return

	print(f"Success: {result['success']}")
	print(f"Game: {result['game']['version']}")

	print(
		f"Pokédex: "
		f"{result['pokedex']['caught']} / "
		f"{result['pokedex']['total']}"
	)

	print(
		f"Playtime: "
		f"{result['playtime']['hours']:02d}:"
		f"{result['playtime']['minutes']:02d}:"
		f"{result['playtime']['seconds']:02d}"
	)

	print()
	print("=== SCARLET ===")

	result = reader.read_game(
		"pokemon_scarlet"
	)

	if result is None:
		print("Failed to read Scarlet save.")
		return

	print(f"Success: {result['success']}")
	print(f"Game: {result['game']['version']}")

	print(
		f"Pokédex: "
		f"{result['pokedex']['caught']} / "
		f"{result['pokedex']['total']}"
	)


if __name__ == "__main__":
	main()