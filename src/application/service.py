from ..domain.gallery import FileScannerInterface, Gallery
from ..domain.value_object import Photo

class AppService:
    def __init__(self, file_scanner: FileScannerInterface, gallery: Gallery):
        self.file_scanner = file_scanner
        self.gallery = gallery

    def find_photo_list(self) -> list[Photo]:
        return self.gallery.find_photo_list()

    def detect_all_faces(self, photo_list: list[Photo]):
        pass

    def get_all_detected_faces(self) -> list:
        return []

    def detect_photo_list_with_similar_face(self, face):
        pass
