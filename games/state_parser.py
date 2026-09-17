from games.state import GameState, PokedexStats


class GameStateParser:

	def parse(self, data: dict) -> GameState | None:
		if not data.get("Success"):
			return None

		game = data.get("Game", {})
		playtime = data.get("Playtime", {})
		pokedex_data = data.get("Pokedex", {})
		dexes = pokedex_data.get("Dexes", {})

		game_type = game.get("Type")

		if game_type == "legends_arceus":
			game_id = "pokemon_legends_arceus"

		elif game_type == "scarlet_violet":
			version = game.get("Version")

			if version == "SL":
				game_id = "pokemon_scarlet"

			elif version == "VL":
				game_id = "pokemon_violet"

			else:
				return None

		else:
			return None

		playtime_seconds = playtime.get(
			"TotalSeconds",
			(
				playtime.get("Hours", 0) * 3600
				+ playtime.get("Minutes", 0) * 60
				+ playtime.get("Seconds", 0)
			)
		)

		pokedex_stats = {}

		for dex_name, dex_data in dexes.items():
			pokedex_stats[dex_name] = PokedexStats(
				seen=dex_data.get("Seen", 0),
				caught=dex_data.get("Caught", 0),
				total=dex_data.get("Total", 0)
			)

		return GameState(
			game_id=game_id,
			playtime_seconds=playtime_seconds,
			pokedex=pokedex_stats
		)