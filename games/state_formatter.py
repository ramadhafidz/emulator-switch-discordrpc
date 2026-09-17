from games.state import GameState


class GameStateFormatter:

	def format_pokedex_pages(self, state: GameState) -> list[str]:
		if not state.pokedex:
			return ["Pokédex: —"]

		pages = []

		for name, dex in state.pokedex.items():
			display_name = name.capitalize()

			pages.append(
				f"{display_name}: "
				f"{dex.caught}/{dex.total}"
			)

		return pages