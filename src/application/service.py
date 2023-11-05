from logging import Logger

from ..domain.indexer import Indexer
from ..domain.gallery import FileScannerInterface, Gallery
from ..domain.recognizer import RecognizerInterface
from ..domain.value_object import Photo
from ..domain.entity import Photo as PhotoEntity

class AppService:
    def __init__(
        self,
        file_scanner: FileScannerInterface,
        gallery: Gallery,
        recognizer: RecognizerInterface,
        indexer: Indexer,
        logger: Logger,
    ) -> None:
        self.file_scanner = file_scanner
        self.gallery = gallery
        self.logger = logger
        self.indexer = indexer
        self.recognizer = recognizer

    def find_photo_list(self) -> list[Photo]:
        return self.gallery.find_photo_list()

    def detect_all_faces(self, photo_list: list[PhotoEntity]):
        total_photos = len(photo_list)
        processed = 0

        for photo in photo_list:
            self.logger.info(f"Распознавание фото. {processed}/{total_photos}")

            face_file_path_list = self.recognizer.get_face_list_from_photo(photo)
            self.logger.info(f"Обнаружено лиц: {len(face_file_path_list)}")

            for face_file_path in face_file_path_list:
                face = self.gallery.save_face(face_file_path)
                self.indexer.add_photo_to_face(face, photo)

            processed += 1
        pass

    def save_photo_list(self, photo_list: list[Photo]) -> list[PhotoEntity]:
        photo_entity_list = [self.gallery.save_photo(photo) for photo in photo_list]

        return photo_entity_list

    def get_all_detected_faces(self) -> list:
        return []

    def detect_photo_list_with_similar_face(self, face):
        pass
