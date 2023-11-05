from logging import Logger
from pprint import pprint
from dependency_injector.wiring import inject, Provide

from .service import AppService
from .container import Container

@inject
def main(
        logger: Logger = Provide[Container.logger],
        app_service: AppService = Provide[Container.app_service],
    ):

    logger.info("Запуск сканирования списка фотографий")
    photo_list = app_service.find_photo_list()

    pprint(photo_list)

    logger.info("Запуск распознавания лиц")
    app_service.detect_all_faces(photo_list)

    logger.info("Получение списка всех распознанных лиц")
    detected_face_list = app_service.get_all_detected_faces()

    logger.info("Запуск поиска похожих лиц и группировка фотографий")
    for face in detected_face_list:
        app_service.detect_photo_list_with_similar_face(face)
