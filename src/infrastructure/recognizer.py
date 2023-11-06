import hashlib
import os
from pprint import pp, pprint
import tempfile
from PIL import Image

from ..domain.entity import Face
from ..domain.recognizer import RecognizerInterface
from ..domain.value_object import Photo

import face_recognition


class FaceRecognitionRecognizer(RecognizerInterface):
    def __init__(self, face_dir: str) -> None:
        self.face_dir = face_dir

        self.__create_face_dir_if_not_exists()

    def get_face_list_from_photo(self, photo: Photo) -> list[str]:
        face_prefix = hashlib.md5(photo.file_path.encode("utf-8")).hexdigest()

        image = face_recognition.load_image_file(photo.file_path)
        face_locations = face_recognition.face_locations(image)

        face_list = []
        for index, face_location in enumerate(face_locations):
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]
            face_image = Image.fromarray(face_image)

            face_file_path = os.path.join(
                self.__get_face_dir(), f"{face_prefix}-{index}.jpg"
            )
            face_image.save(face_file_path)

            face_list.append(face_file_path)

        return face_list

    def find_similar_face_list(
        self, face_file_path, face_list_path_list: list[str]
    ) -> list[str]:
        similar_list = []
        face_image = face_recognition.load_image_file(face_file_path)
        face_image_encoding = face_recognition.face_encodings(face_image)

        if len(face_image_encoding) == 0:
            return similar_list

        for face_to_compare in face_list_path_list:
            face_to_compare_image = face_recognition.load_image_file(face_to_compare)
            face_to_compare_image_encoding = face_recognition.face_encodings(
                face_to_compare_image
            )

            if len(face_to_compare_image_encoding) == 0:
                continue

            results = face_recognition.compare_faces(
                [face_image_encoding[0]], face_to_compare_image_encoding[0]
            )
            is_face_similar = results[0] == True
            if is_face_similar:
                similar_list.append(face_to_compare)

        return similar_list

    def __get_face_dir(self) -> str:
        return os.path.join(tempfile.gettempdir(), self.face_dir)

    def __create_face_dir_if_not_exists(self) -> None:
        os.makedirs(self.__get_face_dir(), exist_ok=True)
