from main.models import FaceMeshDetector, FaceDetector, BodyDetector, HandDetector


key_handlers = [
    ('--body', BodyDetector),
    ('--hand', HandDetector),
    ('--face', FaceDetector),
    ('--face-mesh', FaceMeshDetector),
]
