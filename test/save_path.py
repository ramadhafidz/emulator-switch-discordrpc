import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from games.save_paths import EdenSavePathResolver


def main():
	resolver = EdenSavePathResolver()

	print("=== EDEN SAVE PATH ===")
	print(f"Root: {resolver.save_root}")

	print()
	print("=== ARCEUS ===")

	path = resolver.get_save_path("pokemon_legends_arceus")

	if path is None:
		print("Save not found.")
	else:
		print(f"Save: {path}")

	print()
	print("=== SCARLET ===")

	path = resolver.get_save_path("pokemon_scarlet")

	if path is None:
		print("Save not found.")
	else:
		print(f"Save: {path}")


if __name__ == "__main__":
	main()
