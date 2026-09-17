from dataclasses import dataclass


@dataclass
class PokedexStats:
	seen: int
	caught: int
	total: int


@dataclass
class GameState:
	game_id: str
	playtime_seconds: int | None = None
	location: str | None = None
	pokedex: dict[str, PokedexStats] | None = None