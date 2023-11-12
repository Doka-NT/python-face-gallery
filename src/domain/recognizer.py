from .entity import Face, Photo


class RecognizerInterface:
    def __init__(self) -> None:
        pass

    def get_face_list_from_photo(self, photo: Photo) -> list[str]:
        raise Exception('Not implemented')

    def find_similar_face_list(
        self, face_file_path, face_list_path_list: list[str]
    ) -> list[str]:
        raise Exception('Not implemented')
