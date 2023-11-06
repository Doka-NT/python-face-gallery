from pprint import pprint
from sqlite3 import Connection

from ..domain.entity import Face, Photo
from ..domain.indexer import IndexerRepositoryInterface


class DatabaseIndexerRepository(IndexerRepositoryInterface):
    def __init__(self, db_connection: Connection) -> None:
        self.db_connection = db_connection

    def add_photo_to_face(self, face: Face, photo: Photo) -> None:
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO face_photo (face_id, photo_id) VALUES (?,?)",
            (face.id, photo.id),
        )
        self.db_connection.commit()
        cursor.close()

    def get_face_list(self) -> list[Face]:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM face")
        rows = cursor.fetchall()
        cursor.close()

        face_list = []
        for row in rows:
            face_list.append(Face(row[0]))

        return face_list

    def delete_photo_without_face(self) -> None:
        cursor = self.db_connection.cursor()
        cursor.execute(
            """
            SELECT photo.id FROM photo
            LEFT JOIN face_photo ON face_photo.photo_id = photo.id
            WHERE face_photo.face_id IS NULL
        """
        )

        id_list = [row[0] for row in cursor.fetchall()]
        for id in id_list:
            cursor.execute(
                "DELETE FROM photo WHERE id = :id",
                {
                    "id": id,
                },
            )

        self.db_connection.commit()
        cursor.close()

    def get_photo_list_by_face_id(self, face_id: str) -> list[Photo]:
        cursor = self.db_connection.cursor()
        cursor.execute(
            """
            SELECT photo.id, photo.file_path FROM photo
            LEFT JOIN face_photo ON face_photo.photo_id = photo.id
            WHERE face_photo.face_id = :face_id
        """,
            {
                "face_id": face_id,
            },
        )

        photo_list = []
        for row in cursor.fetchall():
            photo_list.append(Photo(row[1], row[0]))

        return photo_list
