import json
import time
from pathlib import Path

from games.detector import EdenDetector
from games.registry import GameRegistry
from games.state import GameState
from rpc.discord_rpc import DiscordRPC


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


def load_config():
	with CONFIG_PATH.open("r", encoding="utf-8") as file:
		return json.load(file)


def main():
	config = load_config()

	client_id = config["discord"]["client_id"]
	update_interval = config["discord"]["update_interval"]

	registry = GameRegistry(config)
	detector = EdenDetector()
	rpc = DiscordRPC(client_id)

	current_game_id = None
	previous_eden_running = None

	print("Pokémon Switch RPC started.")

	try:
		print("Connecting to Discord...")

		if rpc.connect():
			print("Discord RPC connected.")
		else:
			print("Failed to connect to Discord.")

		while True:
			eden_running = detector.is_running()
			game_id = detector.detect_game()

			if eden_running != previous_eden_running:
				if eden_running:
					print("Eden: running")
				else:
					print("Eden: not running")

				previous_eden_running = eden_running

			if game_id != current_game_id:

				if game_id is None:
					if current_game_id is not None:
						print("Game: none")
						rpc.clear()

				else:
					game = registry.get(game_id)

					if game is None:
						print(f"No configuration found for: {game_id}")
						rpc.clear()

					else:
						print(f"Game detected: {game.name}")

						game_state = GameState(
							game_id=game.id
						)

						details = f"Exploring {game.region}"

						if game_state.pokedex_caught is not None:
							state = (
								f"Pokédex: "
								f"{game_state.pokedex_caught} / "
								f"{game_state.pokedex_total}"
							)
						else:
							state = "Pokédex: —"

						if not rpc.connected:
							print("Discord RPC disconnected. Reconnecting...")

							if not rpc.connect():
								print("Failed to reconnect to Discord.")
								time.sleep(update_interval)
								continue

						success = rpc.update(
							name=game.name,
							details=details,
							state=state,
							large_image=game.large_image,
							large_text=game.large_text
						)

						if success:
							print("Rich Presence updated.")
						else:
							print("Failed to update Rich Presence.")

				current_game_id = game_id

			time.sleep(update_interval)

	except KeyboardInterrupt:
		print("\nStopping Pokémon Switch RPC...")

	finally:
		rpc.clear()
		rpc.close()

		print("RPC cleared.")
		print("Goodbye.")


if __name__ == "__main__":
	main()