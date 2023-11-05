from logging import Logger
from ..domain.gallery import FileScannerInterface, Gallery
from ..domain.recognizer import RecognizerInterface
from ..domain.value_object import Photo

class AppService:
    def __init__(
        self,
        file_scanner: FileScannerInterface,
        gallery: Gallery,
        recognizer: RecognizerInterface,
        logger: Logger,
    ) -> None:
        self.file_scanner = file_scanner
        self.gallery = gallery
        self.logger = logger
        self.recognizer = recognizer

    def find_photo_list(self) -> list[Photo]:
        return self.gallery.find_photo_list()

    def detect_all_faces(self, photo_list: list[Photo]):
        total_photos = len(photo_list)
        processed = 0

        for photo in photo_list:
            self.logger.info(f"Распознавание фото. {processed}/{total_photos}")
            
            face_list = self.recognizer.get_face_list_from_photo(photo)
            
            self.logger.info(f"Обнаружено лиц: {len(face_list)}")
            processed += 1
        pass

    def get_all_detected_faces(self) -> list:
        return []

    def detect_photo_list_with_similar_face(self, face):
        pass
