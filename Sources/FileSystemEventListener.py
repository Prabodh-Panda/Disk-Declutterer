import os
import time
import ctypes
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

DIRECTORIES = {
	"HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "PYTHON": [".py"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}

FILE_FORMATS = {file_format:directory
				for directory, file_formats in DIRECTORIES.items()
				for file_format in file_formats}

class EventHandler(PatternMatchingEventHandler):
	patters = "*"

	def on_modified(self, event):
		time.sleep(5)
		organize()

	def on_created(self, event):
		time.sleep(5)
		organize()

	def on_moved(self, event):
		time.sleep(5)
		organize()

	def on_deleted(self, event):
		pass

def organize():
	for entry in os.scandir():
		if entry.is_dir():
			continue
		file_path = Path(entry)
		file_format = file_path.suffix.lower()
		if file_format in FILE_FORMATS:
			directory_path = Path(FILE_FORMATS[file_format])
			directory_path.mkdir(exist_ok=True)
			try:
				file_path.rename(directory_path.joinpath(file_path))
			except FileExistsError:
				# ctypes.windll.user32.MessageBoxW(0,"Cannot Copy; File Already Exist On Destination","Error: File Already Exist",1)
				basename, extension = os.path.splitext(file_path)
				ii = 1
				while True:
					new_name = os.path.join(basename + "_" + str(ii) + extension)
					if not os.path.exists(directory_path.joinpath(new_name)):
						file_path.rename(directory_path.joinpath(new_name))
						break
					ii += 1

		for dir in os.scandir():
			try:
				os.mkdir(dir)
			except:
				pass


if __name__ == "__main__":
	organize()
	observer = Observer()
	observer.schedule(EventHandler(),".",recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()