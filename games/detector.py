from typing import ClassVar

import psutil
import win32gui
import win32process


class EdenDetector:
	PROCESS_NAMES: ClassVar[set[str]] = {
		"eden.exe",
	}

	GAME_TITLE_MAP: ClassVar[dict[str, str]] = {
		"Pokémon Legends: Arceus": "pokemon_legends_arceus",
		"Pokémon Scarlet": "pokemon_scarlet",
		"Pokémon Violet": "pokemon_violet",
		"Pokémon Legends: Z-A": "pokemon_legends_za",
	}

	def find_process(self):
		for process in psutil.process_iter(["name"]):
			try:
				process_name = process.info["name"]

				if process_name is None:
					continue

				if process_name.lower() in self.PROCESS_NAMES:
					return process

			except (psutil.NoSuchProcess, psutil.AccessDenied):
				continue

		return None

	def is_running(self) -> bool:
		return self.find_process() is not None

	def get_window_title(self) -> str | None:
		eden_process = self.find_process()

		if eden_process is None:
			return None

		eden_pid = eden_process.pid
		result = []

		def callback(hwnd, _):
			_, pid = win32process.GetWindowThreadProcessId(hwnd)

			if pid != eden_pid:
				return True

			if not win32gui.IsWindowVisible(hwnd):
				return True

			title = win32gui.GetWindowText(hwnd)

			if title:
				result.append(title)

			return True

		win32gui.EnumWindows(callback, None)

		for title in result:
			if "Pokémon" in title:
				return title

		return None

	def detect_game(self) -> str | None:
		title = self.get_window_title()

		if title is None:
			return None

		for game_name, game_id in self.GAME_TITLE_MAP.items():
			if game_name in title:
				return game_id

		return None
