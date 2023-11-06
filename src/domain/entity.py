class Face:
    def __init__(self, id=None):
        self.id = id


class Photo:
    def __init__(self, file_path: str, id=None):
        self.id = id
        self.file_path = file_path
