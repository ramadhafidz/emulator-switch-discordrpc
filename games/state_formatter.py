from games.state import GameState


class GameStateFormatter:
	def format_pokedex_pages(self, state: GameState) -> list[str]:
		if not state.pokedex:
			return ["Pokédex: —"]

		pages = []

		for name, dex in state.pokedex.items():
			display_name = name.capitalize()

			pages.append(f"{display_name}: {dex.caught}/{dex.total}")

		return pages

	def format_location(self, state: GameState) -> str:
		if state.location is None:
			return "Lokasi: —"

		if state.location.name:
			return state.location.name

		if state.location.location_id is not None:
			return f"Location #{state.location.location_id}"

		return "Lokasi: —"
