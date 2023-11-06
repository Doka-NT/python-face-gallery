from .entity import Face
from .value_object import Photo


class RecognizerInterface:
    def __init__(self) -> None:
        pass

    def get_face_list_from_photo(self, photo: Photo) -> list[str]:
        pass

    def find_similar_face_list(
        self, face_file_path, face_list_path_list: list[str]
    ) -> list[str]:
        pass
