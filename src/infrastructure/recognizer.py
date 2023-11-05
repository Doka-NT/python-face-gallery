import os
from pprint import pprint
from PIL import Image
from ..domain.recognizer import RecognizerInterface
from ..domain.value_object import Face, Photo

import face_recognition

class FaceRecognitionRecognizer(RecognizerInterface):
    def __init__(self, output_dir: str, face_dir: str) -> None:
        self.output_dir = output_dir
        self.face_dir = face_dir

        self.__create_face_dir_if_not_exists()

    def get_face_list_from_photo(self, photo:Photo):
        image = face_recognition.load_image_file(photo.file_path)
        pil_image = Image.fromarray(image)
        face_locations = face_recognition.face_locations(image)

        face_list = []
        for index, face_location in enumerate(face_locations):
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]
            face_image = Image.fromarray(face_image)

            face_file_path = os.path.join(self.__get_face_dir(), f"{index}.jpg")
            face_image.save(face_file_path)

            face_list.append(
                Face(face_file_path)
            )

        return face_list

    def find_similar_face_list(self, face_list:list[Photo]) -> list[Face]:
        pass

    def __get_face_dir(self) -> str:
        return os.path.join(self.output_dir, self.face_dir)

    def __create_face_dir_if_not_exists(self) -> None:
        os.makedirs(self.__get_face_dir(), exist_ok=True)
