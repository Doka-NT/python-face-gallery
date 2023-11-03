import os

from src.application.controller import main
from src.infrastructure.logger import logger
from src.infrastructure.gallery import FileSystemFileScanner

if __name__ == "__main__":
    main(
        logger,
        FileSystemFileScanner(os.path.join(os.path.dirname(__file__), '.runtime', 'input-photos'))
    )
