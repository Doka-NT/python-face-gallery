from logging import Logger
from .service import find_photo_list, detect_all_faces, get_all_detected_faces, detect_photo_list_with_similar_face

def main(logger:Logger):
    logger.info("Запуск сканирования списка фотографий")
    photo_list = find_photo_list()

    logger.info("Запуск распознавания лиц")
    detect_all_faces(photo_list)

    logger.info("Получение списка всех распознанных лиц")
    detected_face_list = get_all_detected_faces()

    logger.info("Запуск поиска похожих лиц и группировка фотографий")
    for face in detected_face_list:
        detect_photo_list_with_similar_face(face)
