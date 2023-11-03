import os

from ..domain.gallery import FileScannerInterface


class FileSystemFileScanner(FileScannerInterface):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def find_photo_list(self) -> list:
        photo_list = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                # Проверка наличия расширения файла .jpg или .jpeg
                if file.endswith('.jpg') or file.endswith('.jpeg'):
                    photo_list.append(os.path.join(root, file))
        return photo_list
