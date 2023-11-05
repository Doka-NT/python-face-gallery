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
