#File Organizer Based on Types i.e. [.jpg, .jpeg, .png etc] - Image
import os
import time
from pathlib import Path

DIRECTORIES = {
	"HTML":{".html5",".html",".htm",".xhtml"},
	"IMAGES":{".jpg",".jpeg",".png",".svg",".gif",".tiff",".psd"}
}

FILE_FORMATS = {file_format:directory
				for directory, file_formats in DIRECTORIES.items()
				for file_format in file_formats}

def organize():
	for entry in os.scandir():
		if entry.is_dir():
			continue
		file_path = Path(entry)
		file_format = file_path.suffix.lower()
		if file_format in FILE_FORMATS:
			directory_path = Path(FILE_FORMATS[file_format])
			directory_path.mkdir(exist_ok=True)
			file_path.rename(directory_path.joinpath(file_path))

		for dir in os.scandir():
			try:
				os.mkdir(dir)
			except:
				pass

if __name__ == "__main__":
	while True:
		print("Code is running")
		time.sleep(1)






