import os
from src.application.container import Container
from src.application.controller import main

if __name__ == "__main__":
    container = Container()
    container.config.set('gallery_path', os.path.join(os.path.dirname(__file__), '.runtime', 'input-photos'))
    container.init_resources()
    container.wire(packages=[__name__, 'src'], from_package='.')

    main()
