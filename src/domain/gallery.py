class FileScannerInterface:
    def find_photo_list(self) -> list:
        pass

class Gallery:
    def find_photo_list(self, file_scanner:FileScannerInterface) -> list:
        return file_scanner.find_photo_list()
