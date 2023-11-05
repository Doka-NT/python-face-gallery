from .entity import Face, Photo

class IndexerRepositoryInterface:
    def add_photo_to_face(self, face: Face, photo: Photo) -> None:
        pass

class Indexer:
    def __init__(self, indexer_repository: IndexerRepositoryInterface) -> None:
        self.indexer_storage = indexer_repository

    def add_photo_to_face(self, face: Face, photo: Photo) -> None:
        self.indexer_storage.add_photo_to_face(face, photo)
