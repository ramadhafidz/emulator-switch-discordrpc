from dataclasses import dataclass


@dataclass
class GameDefinition:
	id: str
	name: str
	region: str
	large_image: str
	large_text: str