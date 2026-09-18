import psutil


def main():
	for process in psutil.process_iter(["pid", "name", "cmdline"]):
		try:
			name = process.info["name"]

			if name and name.lower() == "eden.exe":
				pid = process.info["pid"]
				cmdline = process.info["cmdline"]

				print(f"PID: {pid}")
				print("Command line:")

				if cmdline:
					for argument in cmdline:
						print(f"  {argument}")
				else:
					print("  <empty>")

				return

		except (psutil.NoSuchProcess, psutil.AccessDenied):
			continue

	print("Eden is not running.")


if __name__ == "__main__":
	main()
