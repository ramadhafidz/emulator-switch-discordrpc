import time

from pypresence.presence import Presence


class DiscordRPC:
	def __init__(self, client_id: str):
		self.client_id = client_id
		self.rpc = None
		self.connected = False
		self.start_time = None

	def connect(self):
		if self.connected:
			return True

		try:
			self.rpc = Presence(self.client_id)
			self.rpc.connect()

			self.start_time = int(time.time())
			self.connected = True

			return True

		except Exception:
			self.rpc = None
			self.connected = False
			self.start_time = None

			return False

	def update(
		self,
		name: str,
		details: str,
		state: str,
		large_image: str,
		large_text: str,
	):
		if not self.connected or self.rpc is None:
			return False

		try:
			self.rpc.update(
				name=name,
				details=details,
				state=state,
				large_image=large_image,
				large_text=large_text,
				start=self.start_time,
			)

			return True

		except Exception as error:
			print(f"RPC update failed: {error}")

			self.connected = False

			try:
				self.rpc.close()
			except Exception:
				pass

			self.rpc = None

			return False

	def clear(self):
		if not self.connected or self.rpc is None:
			return

		try:
			self.rpc.clear()
		except Exception:
			pass

	def close(self):
		if self.rpc is None:
			return

		try:
			self.rpc.close()
		except Exception:
			pass

		self.rpc = None
		self.connected = False
		self.start_time = None
