import os
from sqlite3 import Connection
import uuid
import shutil

from ..domain.entity import Face, Photo as PhotoEntity

from ..domain.gallery import (
    FaceFileStorageInterface,
    FileScannerInterface,
    FaceRepositoryInterface,
    GalleryStorageInterface,
    PhotoRepositoryInterface,
    SimilarFaceRepositoryInterface,
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
                if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
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
        file_path = self.get_face_path(face)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        shutil.copyfile(face_file_path, file_path)

    def get_face(self, face_path: str) -> Face:
        id = os.path.basename(face_path).replace(".jpg", "")

        return Face(id=id)

    def get_face_path(self, face: Face) -> str:
        return os.path.join(self.__get_face_dir(), self.__get_face_filename(face))

    def __get_face_filename(self, face: Face) -> str:
        return f"{face.id}.jpg"

    def __get_face_dir(self) -> str:
        return os.path.join(self.output_dir, self.face_dir)


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

    def find_by_id_list(self, id_list: list[str]) -> list[Face]:
        return [Face(id=id) for id in id_list]


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


class SimilarFaceRepository(SimilarFaceRepositoryInterface):
    def __init__(self, db_connection: Connection) -> None:
        self.db_connection = db_connection

    def save(self, face: Face, similar_face_list: list[Face]) -> None:
        cursor = self.db_connection.cursor()

        for similar_face in similar_face_list:
            cursor.execute(
                """
                INSERT INTO similar_face (face_id, similar_face_id)
                VALUES (:face_id, :similar_face_id)
                """,
                {
                    "face_id": face.id,
                    "similar_face_id": similar_face.id,
                },
            )
        self.db_connection.commit()

    def is_related(self, face: Face, similar_face: Face) -> bool:
        cursor = self.db_connection.cursor()

        row = cursor.execute(
            """
                SELECT * FROM similar_face
                WHERE 
                    (face_id = :face_id AND similar_face_id = :similar_face_id)
                    OR (similar_face_id = :face_id AND face_id = :similar_face_id)
            """,
            {"face_id": face.id, "similar_face_id": similar_face.id},
        ).fetchone()

        return row is not None

    def find_face_id_list_by_face_id(self, face_id: str) -> list[str]:
        cursor = self.db_connection.cursor()

        rows = cursor.execute(
            """
                SELECT similar_face_id FROM similar_face
                WHERE face_id = :face_id
            """,
            {"face_id": face_id},
        ).fetchall()

        return [row[0] for row in rows]


class FileSystemGalleryStorage(GalleryStorageInterface):
    def __init__(self, output_dir: str, album_dir: str) -> None:
        super().__init__()
        self.output_dir = output_dir
        self.album_dir = album_dir

    def create_album(self, name: str) -> None:
        album_path = self.__get_album_path(name)
        os.makedirs(album_path, exist_ok=True)

    def add_photo_to_album(self, name: str, photo_path: str) -> None:
        album_path = self.__get_album_path(name)
        target_file_path = os.path.join(album_path, os.path.basename(photo_path))
        shutil.copyfile(photo_path, target_file_path)

    def __get_album_path(self, name: str) -> str:
        return os.path.join(self.output_dir, self.album_dir, name)
