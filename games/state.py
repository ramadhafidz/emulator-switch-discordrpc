from dataclasses import dataclass


@dataclass
class GameState:
	game_id: str
	playtime_seconds: int | None = None
	pokedex_caught: int | None = None
	pokedex_total: int | None = None
	location: str | None = None