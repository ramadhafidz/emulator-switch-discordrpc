from pathlib import Path


class EdenSavePathResolver:

	GAME_TITLE_IDS = {
		"pokemon_legends_arceus": "01001F5010DFA000",
		"pokemon_scarlet": "0100A3D008C5C000",
		"pokemon_violet": "01008F6008C5E000",
		"pokemon_legends_za": "0100F43008C44000",
	}

	def __init__(self):
		self.save_root = (
			Path.home()
			/ "AppData"
			/ "Roaming"
			/ "eden"
			/ "nand"
			/ "user"
			/ "save"
		)

	def get_game_directory(self, game_id: str) -> Path | None:
		title_id = self.GAME_TITLE_IDS.get(game_id)

		if title_id is None:
			return None

		if not self.save_root.is_dir():
			return None

		for path in self.save_root.rglob(title_id):
			if path.is_dir():
				return path

		return None

	def get_save_path(self, game_id: str) -> Path | None:
		game_directory = self.get_game_directory(game_id)

		if game_directory is None:
			return None

		save_path = game_directory / "main"

		if not save_path.is_file():
			return None

		return save_path