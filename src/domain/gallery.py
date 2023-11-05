from .entity import Face, Photo as PhotoEntity
from .value_object import Photo


class FileScannerInterface:
    def find_photo_list(self) -> list[Photo]:
        pass


class FaceFileStorageInterface:
    def save(self, face: Face, face_file_path: str) -> None:
        pass


class FaceRepositoryInterface:
    def save(self, face: Face) -> None:
        pass

class PhotoRepositoryInterface:
    def save(self, photo: PhotoEntity) -> None:
        pass

class Gallery:
    def __init__(
        self,
        file_scanner: FileScannerInterface,
        face_file_storage: FaceFileStorageInterface,
        face_repository: FaceRepositoryInterface,
        photo_repository: PhotoRepositoryInterface,
    ) -> None:
        self.file_scanner = file_scanner
        self.face_file_storage = face_file_storage
        self.face_repository = face_repository
        self.photo_repository = photo_repository

    def find_photo_list(self) -> list[Photo]:
        return self.file_scanner.find_photo_list()

    def save_face(self, face_file_path: str) -> Face:
        face = Face(file_path=face_file_path)
        
        self.face_repository.save(face)
        self.face_file_storage.save(face, face_file_path)

        return face

    def save_photo(self, photo: Photo) -> PhotoEntity:
        photo_entity = PhotoEntity(
            file_path=photo.file_path,
        )
        self.photo_repository.save(photo_entity)

        return photo_entity
