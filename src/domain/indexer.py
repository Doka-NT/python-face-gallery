from .entity import Face, Photo


class IndexerRepositoryInterface:
    def add_photo_to_face(self, face: Face, photo: Photo) -> None:
        pass

    def get_face_list(self) -> list[Face]:
        pass

    def delete_photo_without_face(self) -> None:
        pass

    def get_photo_list_by_face_id(self, face_id: str) -> list[Photo]:
        pass


class Indexer:
    def __init__(self, indexer_repository: IndexerRepositoryInterface) -> None:
        self.indexer_repository = indexer_repository

    def add_photo_to_face(self, face: Face, photo: Photo) -> None:
        self.indexer_repository.add_photo_to_face(face, photo)

    def get_face_list(self) -> list[Face]:
        return self.indexer_repository.get_face_list()

    def delete_photo_without_face(self):
        self.indexer_repository.delete_photo_without_face()

    def get_face_photo_list(self, face: Face) -> list[Photo]:
        return self.indexer_repository.get_photo_list_by_face_id(face.id)
