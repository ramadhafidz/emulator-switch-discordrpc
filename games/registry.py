from games.base import GameDefinition


class GameRegistry:

	def __init__(self, config: dict):
		self.games = {}

		for game_id, game_config in config["games"].items():
			self.games[game_id] = GameDefinition(
				id=game_id,
				name=game_config["name"],
				region=game_config["region"],
				large_image=game_config["large_image"],
				large_text=game_config["large_text"],
				details=game_config["details"],
				state=game_config["state"]
			)

	def get(self, game_id: str) -> GameDefinition | None:
		return self.games.get(game_id)

	def all(self) -> list[GameDefinition]:
		return list(self.games.values())