from .entity import Face, Photo as PhotoEntity
from .value_object import Photo


class FileScannerInterface:
    def find_photo_list(self) -> list[Photo]:
        pass


class FaceFileStorageInterface:
    def save(self, face: Face, face_file_path: str) -> None:
        pass

    def get_face_path(self, face: Face) -> str:
        pass


class FaceRepositoryInterface:
    def save(self, face: Face) -> None:
        pass

    def find_by_id_list(self, id_list: list[str]) -> list[Face]:
        pass


class PhotoRepositoryInterface:
    def save(self, photo: PhotoEntity) -> None:
        pass


class SimilarFaceRepositoryInterface:
    def save(self, face: Face, similar_face_list: list[Face]) -> None:
        pass

    def is_related(self, face: Face, similar_face: Face) -> bool:
        pass

    def find_face_id_list_by_face_id(self, face_id: str) -> list[str]:
        pass


class GalleryStorageInterface:
    def create_album(self, name: str) -> None:
        pass

    def add_photo_to_album(self, name: str, photo_path: str) -> None:
        pass


class Gallery:
    def __init__(
        self,
        file_scanner: FileScannerInterface,
        face_file_storage: FaceFileStorageInterface,
        face_repository: FaceRepositoryInterface,
        photo_repository: PhotoRepositoryInterface,
        similar_face_repository: SimilarFaceRepositoryInterface,
        gallery_storage: GalleryStorageInterface,
    ) -> None:
        self.file_scanner = file_scanner
        self.face_file_storage = face_file_storage
        self.face_repository = face_repository
        self.photo_repository = photo_repository
        self.similar_face_repository = similar_face_repository
        self.gallery_storage = gallery_storage

    def find_photo_list(self) -> list[Photo]:
        return self.file_scanner.find_photo_list()

    def save_face(self, face_file_path: str) -> Face:
        face = Face()

        self.face_repository.save(face)
        self.face_file_storage.save(face, face_file_path)

        return face

    def save_photo(self, photo: Photo) -> PhotoEntity:
        photo_entity = PhotoEntity(
            file_path=photo.file_path,
        )
        self.photo_repository.save(photo_entity)

        return photo_entity

    def get_face_file_path(self, face: Face) -> str:
        return self.face_file_storage.get_face_path(face)

    def save_similar_face_list(
        self, face: Face, similar_face_path_list: list[str]
    ) -> None:
        similar_face_id_list = [
            self.face_file_storage.get_face(face_path).id
            for face_path in similar_face_path_list
        ]

        similar_face_list = self.face_repository.find_by_id_list(similar_face_id_list)

        for similar_face in similar_face_list:
            is_already_related = self.similar_face_repository.is_related(
                face, similar_face
            )
            if is_already_related:
                continue

            self.similar_face_repository.save(face, [similar_face])

    def get_similar_face_list(self, face: Face) -> list[Face]:
        face_id_list = self.similar_face_repository.find_face_id_list_by_face_id(
            face.id
        )

        return self.face_repository.find_by_id_list(face_id_list)

    def create_album(self, face: Face, main_face_photo_file_path: str) -> None:
        self.gallery_storage.create_album(face.id)
        self.gallery_storage.add_photo_to_album(face.id, main_face_photo_file_path)

    def add_photo_list_to_album(
        self, face: Face, photo_list: list[PhotoEntity]
    ) -> None:
        processed_path_list = []
        for photo in photo_list:
            if photo.file_path in processed_path_list:
                continue
            self.gallery_storage.add_photo_to_album(face.id, photo.file_path)
            processed_path_list.append(photo.file_path)
