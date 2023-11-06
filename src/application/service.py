from logging import Logger

from ..domain.indexer import Indexer
from ..domain.gallery import FileScannerInterface, Gallery
from ..domain.recognizer import RecognizerInterface
from ..domain.value_object import Photo
from ..domain.entity import Face, Photo as PhotoEntity


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
        return self.indexer.get_face_list()

    def detect_photo_list_with_similar_face(
        self, face: Face, face_list: list[Face]
    ) -> None:
        # Находим пути файлов с лицами
        face_file_path = self.gallery.get_face_file_path(face)
        face_list_file_path_list = [
            self.gallery.get_face_file_path(face) for face in face_list
        ]

        # Находим список похожих лиц
        similar_face_list = self.recognizer.find_similar_face_list(
            face_file_path, face_list_file_path_list
        )
        self.logger.info(
            f"Лицо: {face.id}. Количество похожих: {len(similar_face_list)}"
        )

        self.gallery.save_similar_face_list(face, similar_face_list)
        similar_face_entity_list = self.gallery.get_similar_face_list(face)

        for similar_face in similar_face_entity_list:
            photo_list = self.indexer.get_face_photo_list(similar_face)

            for photo in photo_list:
                self.indexer.add_photo_to_face(similar_face, photo)

    def delete_photo_without_face(self):
        self.indexer.delete_photo_without_face()

    def create_album(self):
        processed_face_id_list = []

        for face in self.indexer.get_face_list():
            if face.id in processed_face_id_list:
                continue

            main_face_photo_file_path = self.gallery.get_face_file_path(face)
            self.gallery.create_album(face, main_face_photo_file_path)

            similar_face_list = self.gallery.get_similar_face_list(face)
            face_photo_list = self.indexer.get_face_photo_list(face)

            processed_face_id_list.append(face.id)
            for similar_face in similar_face_list:
                similar_face_photo_list = self.indexer.get_face_photo_list(similar_face)

                for similar_face_photo in similar_face_photo_list:
                    face_photo_list.append(similar_face_photo)
                processed_face_id_list.append(similar_face.id)

            self.gallery.add_photo_list_to_album(face, face_photo_list)
