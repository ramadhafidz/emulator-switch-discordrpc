from games.save_paths import EdenSavePathResolver
from games.save_reader import SaveReader
from games.state import GameState
from games.state_parser import GameStateParser


class GameSaveReader:
	def __init__(self, bridge_path: str):
		self.path_resolver = EdenSavePathResolver()
		self.save_reader = SaveReader(bridge_path)
		self.state_parser = GameStateParser()

	def read_game(self, game_id: str) -> GameState | None:
		save_path = self.path_resolver.get_save_path(game_id)

		if save_path is None:
			print(f"Save not found for game: {game_id}")
			return None

		data = self.save_reader.read(str(save_path))

		if data is None:
			return None

		return self.state_parser.parse(data)
