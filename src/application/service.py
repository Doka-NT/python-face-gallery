from ..domain.gallery import FileScannerInterface, Gallery


def find_photo_list(file_scanner:FileScannerInterface) -> list:
    gallery = Gallery()

    return gallery.find_photo_list(file_scanner)

def detect_all_faces(photo_list):
    pass

def get_all_detected_faces() -> list:
    return []

def detect_photo_list_with_similar_face(face):
    pass
