from logging import Logger
from sqlite3 import Connection
from dependency_injector.wiring import inject, Provide

from .service import AppService
from .container import Container
from ..infrastructure.controller import init_database as infrastructure_init_database


@inject
def main(
    logger: Logger = Provide[Container.logger],
    app_service: AppService = Provide[Container.app_service],
):
    logger.info("Запуск сканирования списка фотографий")
    photo_list = app_service.find_photo_list()

    logger.info("Сохранение фотографий в базу данных")
    photo_entity_list = app_service.save_photo_list(photo_list)

    logger.info("Запуск распознавания лиц")
    app_service.detect_all_faces(photo_entity_list)

    logger.info("Удаление фотографий без лиц из БД")
    app_service.delete_photo_without_face()

    logger.info(f"Получение списка всех распознанных лиц")
    detected_face_list = app_service.get_all_detected_faces()
    logger.info(f"Распознанных лиц: {len(detected_face_list)}")

    logger.info("Запуск поиска похожих лиц и группировка фотографий")
    for face in detected_face_list:
        app_service.detect_photo_list_with_similar_face(face, detected_face_list)

    logger.info("Формирование фотоальбома")
    app_service.create_album()


@inject
def init_database(db_connection: Connection = Provide[Container.db_connection]):
    infrastructure_init_database(db_connection)
