import psutil
import win32gui
import win32process


def main():
	eden_pids = []

	for process in psutil.process_iter(["pid", "name"]):
		try:
			name = process.info["name"]

			if name and name.lower() == "eden.exe":
				eden_pids.append(process.info["pid"])

		except (psutil.NoSuchProcess, psutil.AccessDenied):
			continue

	print(f"Eden PIDs: {eden_pids}")
	print()

	def callback(hwnd, _):
		_, pid = win32process.GetWindowThreadProcessId(hwnd)

		if pid not in eden_pids:
			return True

		title = win32gui.GetWindowText(hwnd)
		class_name = win32gui.GetClassName(hwnd)

		if title or class_name:
			print(
				f"PID={pid} | HWND={hwnd} | Class={class_name} | Title={title}"
			)

		return True

	win32gui.EnumWindows(callback, None)


if __name__ == "__main__":
	main()
