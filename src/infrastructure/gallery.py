import os
from sqlite3 import Connection
import uuid
import shutil

from ..domain.entity import Face, Photo as PhotoEntity

from ..domain.gallery import (
    FaceFileStorageInterface,
    FileScannerInterface,
    FaceRepositoryInterface,
    PhotoRepositoryInterface,
)
from ..domain.value_object import Photo
from dependency_injector.wiring import Provide, _is_marker

class FileSystemFileScanner(FileScannerInterface):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def find_photo_list(self) -> list[Photo]:
        photo_list = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                # Проверка наличия расширения файла .jpg или .jpeg
                if file.endswith(".jpg") or file.endswith(".jpeg"):
                    photo_list.append(self.__create_photo(os.path.join(root, file)))
        return photo_list

    def __create_photo(self, path: str) -> Photo:
        return Photo(path)


class FaceFileStorage(FaceFileStorageInterface):
    def __init__(self, output_dir: str, face_dir: str) -> None:
        super().__init__()
        self.output_dir = output_dir
        self.face_dir = face_dir

    def save(self, face: Face, face_file_path: str) -> None:
        file_name = f"{face.id}.jpg"
        file_path = os.path.join(self.output_dir, self.face_dir, file_name)

        shutil.copyfile(face_file_path, file_path)


class FaceRepository(FaceRepositoryInterface):
    def __init__(self, db_connection: Connection) -> None:
        super().__init__()
        self.db_connection = db_connection

    def save(self, face: Face) -> None:
        cursor = self.db_connection.cursor()

        is_insert = False
        if face.id is None:
            face.id = str(uuid.uuid4())
            is_insert = True

        if is_insert:
            cursor.execute(
                """
                INSERT INTO face (id)
                VALUES (:id)
                """,
                {
                    "id": face.id,
                },
            )
        else:
            cursor.execute(
                """
                UPDATE face
                SET id = :id
                WHERE id = :id
                """,
                {
                    "id": face.id,
                },
            )
        self.db_connection.commit()

class PhotoRepository(PhotoRepositoryInterface):
    def __init__(self, db_connection: Connection) -> None:
        self.db_connection = db_connection

    def save(self, photo: PhotoEntity) -> None:
        cursor = self.db_connection.cursor()

        is_insert = False
        if photo.id is None:
            photo.id = str(uuid.uuid4())
            is_insert = True

        if is_insert:
            cursor.execute(
                """
                INSERT INTO photo (id, file_path)
                VALUES (:id, :file_path)
                """,
                {
                    "id": photo.id,
                    "file_path": photo.file_path,
                },
            )
        else:
            cursor.execute(
                """
                UPDATE photo
                SET file_path = :file_path
                WHERE id = :id
                """,
                {
                    "id": photo.id,
                    "file_path": photo.file_path,
                },
            )
        self.db_connection.commit()
