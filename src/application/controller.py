from logging import Logger
from pprint import pprint

from .service import find_photo_list, detect_all_faces, get_all_detected_faces, detect_photo_list_with_similar_face
from ..domain.gallery import FileScannerInterface

def main(
        logger:Logger,
        file_scanner:FileScannerInterface
    ):
    logger.info("Запуск сканирования списка фотографий")
    photo_list = find_photo_list(file_scanner)

    pprint(photo_list)

    logger.info("Запуск распознавания лиц")
    detect_all_faces(photo_list)

    logger.info("Получение списка всех распознанных лиц")
    detected_face_list = get_all_detected_faces()

    logger.info("Запуск поиска похожих лиц и группировка фотографий")
    for face in detected_face_list:
        detect_photo_list_with_similar_face(face)
