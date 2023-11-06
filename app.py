import os
from src.application.container import Container
from src.application.controller import init_database, main

if __name__ == "__main__":
    app_dir = os.path.join(os.path.dirname(__file__))
    runtime_dir = os.path.join(app_dir, ".runtime")

    input_dir = os.path.join(runtime_dir, "input-photos")
    output_dir = os.path.join(runtime_dir, "output")

    container = Container()

    container.config.set("gallery_path", input_dir)
    container.config.set("output_dir", output_dir)
    container.config.set(
        "db_path", os.path.join(runtime_dir, container.config.get("db_path"))
    )

    container.init_resources()
    container.wire(packages=[__name__, "src"], from_package=".")

    init_database()
    main()
