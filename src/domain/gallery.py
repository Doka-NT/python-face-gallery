from .value_object import Photo

class FileScannerInterface:
    def find_photo_list(self) -> list:
        pass

class Gallery:
    def __init__(self, file_scanner: FileScannerInterface) -> None:
        self.file_scanner = file_scanner

    def find_photo_list(self) -> list[Photo]:
        return self.file_scanner.find_photo_list()
