import os
import sqlite3
from dependency_injector import containers, providers
from src.infrastructure.indexer import DatabaseIndexerRepository

from src.infrastructure.recognizer import FaceRecognitionRecognizer
from .service import AppService
from ..domain.gallery import Gallery
from ..domain.indexer import Indexer
from ..infrastructure.gallery import (
    FaceFileStorage,
    FaceRepository,
    FileSystemFileScanner,
    FileSystemGalleryStorage,
    PhotoRepository,
    SimilarFaceRepository,
)
from ..infrastructure.logger import logger


class Container(containers.DeclarativeContainer):
    parameters_file = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        "config",
        "parameters.yaml",
    )

    config = providers.Configuration(yaml_files=[parameters_file])

    logger = providers.Factory(lambda: logger)

    db_connection = providers.Factory(
        lambda db_path: sqlite3.connect(db_path),
        config.db_path,
    )

    domain_gallery_file_scanner = providers.Factory(
        FileSystemFileScanner, config.gallery_path
    )

    domain_face_file_storage = providers.Factory(
        FaceFileStorage,
        config.output_dir,
        config.face_dir,
    )

    domain_face_repository = providers.Factory(
        FaceRepository,
        db_connection=db_connection,
    )

    domain_photo_repository = providers.Factory(
        PhotoRepository,
        db_connection=db_connection,
    )

    domain_similar_face_repository = providers.Factory(
        SimilarFaceRepository,
        db_connection=db_connection,
    )

    domain_gallery_storage = providers.Factory(
        FileSystemGalleryStorage,
        config.output_dir,
        config.album_dir,
    )

    domain_gallery = providers.Factory(
        Gallery,
        domain_gallery_file_scanner,
        domain_face_file_storage,
        domain_face_repository,
        domain_photo_repository,
        domain_similar_face_repository,
        domain_gallery_storage,
    )

    domain_recognizer = providers.Factory(
        FaceRecognitionRecognizer,
        face_dir=config.face_dir,
    )

    domain_indexer_repository = providers.Factory(
        DatabaseIndexerRepository,
        db_connection=db_connection,
    )

    domain_indexer = providers.Factory(Indexer, domain_indexer_repository)

    app_service = providers.Factory(
        AppService,
        file_scanner=domain_gallery_file_scanner,
        gallery=domain_gallery,
        recognizer=domain_recognizer,
        indexer=domain_indexer,
        logger=logger,
    )
