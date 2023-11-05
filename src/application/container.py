import os
from dependency_injector import containers, providers

from src.infrastructure.recognizer import FaceRecognitionRecognizer
from .service import AppService
from ..domain.gallery import Gallery
from ..domain.recognizer import RecognizerInterface
from ..infrastructure.gallery import FileSystemFileScanner
from ..infrastructure.logger import logger


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()

    parameters_file = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, 'config', 'parameters.yaml')

    config = providers.Configuration(yaml_files=[parameters_file])

    logger = providers.Factory(
        lambda: logger
    )

    domain_gallery_file_scanner = providers.Factory(
        FileSystemFileScanner,
        config.gallery_path
    )

    domain_gallery = providers.Factory(
        Gallery,
        domain_gallery_file_scanner
    )

    domain_recognizer = providers.Factory(
        FaceRecognitionRecognizer,
        output_dir=config.output_dir,
        face_dir=config.face_dir,
    )

    app_service = providers.Factory(
        AppService,
        file_scanner=domain_gallery_file_scanner,
        gallery=domain_gallery,
        recognizer=domain_recognizer,
        logger=logger,
    )    
