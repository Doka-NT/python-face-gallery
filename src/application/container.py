from dependency_injector import containers, providers

from .service import AppService
from ..domain.gallery import Gallery
from ..infrastructure.gallery import FileSystemFileScanner
from ..infrastructure.logger import logger


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()

    config = providers.Configuration(yaml_files=['parameters.yaml'])

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

    app_service = providers.Factory(
        AppService,
        file_scanner=domain_gallery_file_scanner,
        gallery=domain_gallery
    )    
