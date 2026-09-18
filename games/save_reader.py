import json
import subprocess
from pathlib import Path


class SaveReader:
	def __init__(self, bridge_path: str):
		self.bridge_path = Path(bridge_path)

	def read(self, save_path: str) -> dict | None:
		save_file = Path(save_path)

		if not save_file.exists():
			print(f"Save file not found: {save_file}")
			return None

		if not self.bridge_path.exists():
			print(f"Save reader bridge not found: {self.bridge_path}")
			return None

		try:
			result = subprocess.run(
				["dotnet", str(self.bridge_path), str(save_file)],
				capture_output=True,
				text=True,
				encoding="utf-8",
				errors="replace",
				timeout=10,
			)

		except subprocess.TimeoutExpired:
			print("Save reader timed out.")
			return None

		except Exception as error:
			print(f"Save reader failed to start: {error}")
			return None

		if result.returncode != 0:
			error = (result.stderr or "").strip()

			if error:
				print(f"Save reader error:\n{error}")
			else:
				print(f"Save reader exited with code {result.returncode}.")

			return None

		output = (result.stdout or "").strip()

		if not output:
			print("Save reader returned no output.")
			return None

		try:
			return json.loads(output)

		except json.JSONDecodeError as error:
			print(f"Invalid JSON from save reader: {error}")
			print(output)

			return None
