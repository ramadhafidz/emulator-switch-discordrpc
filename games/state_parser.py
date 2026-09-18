from games.state import (
	BoxesState,
	BoxSlotState,
	BoxState,
	GameState,
	LocationState,
	PartyState,
	PokedexStats,
	PokemonState,
)


class GameStateParser:
	def parse(self, data: dict) -> GameState | None:
		if not data.get("Success"):
			return None

		game = data.get("Game", {})
		playtime = data.get("Playtime", {})
		pokedex_data = data.get("Pokedex", {})
		dexes = pokedex_data.get("Dexes", {})
		location_data = data.get("Location", {})

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
			),
		)

		pokedex_stats = {}

		for dex_name, dex_data in dexes.items():
			pokedex_stats[dex_name] = PokedexStats(
				seen=dex_data.get("Seen", 0),
				caught=dex_data.get("Caught", 0),
				total=dex_data.get("Total", 0),
			)

		party = self._parse_party(data.get("Party", {}))

		boxes = self._parse_boxes(data.get("Boxes", {}))

		location = LocationState(
			name=location_data.get("Name"),
			field_id=location_data.get("FieldID"),
			location_id=location_data.get("LocationID"),
			x=location_data.get("X"),
			y=location_data.get("Y"),
			z=location_data.get("Z"),
		)

		return GameState(
			game_id=game_id,
			playtime_seconds=playtime_seconds,
			location=location,
			pokedex=pokedex_stats,
			party=party,
			boxes=boxes,
		)

	def _parse_pokemon(self, data: dict) -> PokemonState:
		return PokemonState(
			species=data.get("Species", 0),
			species_name=data.get("SpeciesName", ""),
			form=data.get("Form", 0),
			level=data.get("Level", 0),
			is_shiny=data.get("IsShiny", False),
			is_alpha=data.get("IsAlpha", False),
			nickname=data.get("Nickname", ""),
			gender=data.get("Gender", 0),
			nature=data.get("Nature", ""),
			ability=data.get("Ability", 0),
			held_item=data.get("HeldItem", 0),
		)

	def _parse_party(self, data: dict) -> PartyState:
		members = []

		for pokemon_data in data.get("Members", []):
			members.append(self._parse_pokemon(pokemon_data))

		return PartyState(members=members)

	def _parse_boxes(self, data: dict) -> BoxesState:
		boxes = []

		for box_data in data.get("Boxes", []):
			slots = []

			for slot_data in box_data.get("Slots", []):
				pokemon_data = slot_data.get("Pokemon")

				if pokemon_data is None:
					continue

				slots.append(
					BoxSlotState(
						slot=slot_data.get("Slot", 0),
						pokemon=self._parse_pokemon(pokemon_data),
					)
				)

			boxes.append(
				BoxState(number=box_data.get("Number", 0), slots=slots)
			)

		return BoxesState(boxes=boxes)
