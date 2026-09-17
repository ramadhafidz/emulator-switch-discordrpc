from games.save_paths import EdenSavePathResolver
from games.save_reader import SaveReader


class GameSaveReader:

	def __init__(self, bridge_path: str):
		self.path_resolver = EdenSavePathResolver()
		self.save_reader = SaveReader(bridge_path)

	def read_game(self, game_id: str) -> dict | None:
		save_path = self.path_resolver.get_save_path(game_id)

		if save_path is None:
			print(f"Save not found for game: {game_id}")
			return None

		return self.save_reader.read(str(save_path))