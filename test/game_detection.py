import time

from games.detector import EdenDetector


def main():
	detector = EdenDetector()

	print("Eden game detector started.")
	print("Start a Pokémon game in Eden.")
	print("Press CTRL+C to stop.")

	last_game = None

	try:
		while True:
			game = detector.detect_game()

			if game != last_game:
				if game:
					print(f"Detected game: {game}")
				else:
					print("No supported Pokémon game detected.")

				last_game = game

			time.sleep(2)

	except KeyboardInterrupt:
		print("\nDetector stopped.")


if __name__ == "__main__":
	main()
