from .value_object import Face, Photo

class RecognizerInterface:
    def __init__(self) -> None:
        pass

    def get_face_list_from_photo(self, photo:Photo):
        pass

    def find_similar_face_list(self, face_list:list[Photo]) -> list[Face]:
        pass
