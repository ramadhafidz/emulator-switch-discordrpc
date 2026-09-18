from dataclasses import dataclass


@dataclass
class PokedexStats:
	seen: int
	caught: int
	total: int


@dataclass
class PokemonState:
	species: int
	species_name: str
	form: int
	level: int
	is_shiny: bool
	is_alpha: bool
	nickname: str
	gender: int
	nature: str
	ability: int
	held_item: int


@dataclass
class PartyState:
	members: list[PokemonState]


@dataclass
class BoxSlotState:
	slot: int
	pokemon: PokemonState


@dataclass
class BoxState:
	number: int
	slots: list[BoxSlotState]


@dataclass
class BoxesState:
	boxes: list[BoxState]


@dataclass
class LocationState:
	name: str | None = None
	field_id: int | None = None
	location_id: int | None = None
	x: float | None = None
	y: float | None = None
	z: float | None = None


@dataclass
class GameState:
	game_id: str
	playtime_seconds: int | None = None
	location: LocationState | None = None
	pokedex: dict[str, PokedexStats] | None = None
	party: PartyState | None = None
	boxes: BoxesState | None = None
