from main.models import HandDetector, BodyDetector, CustomDetector, FaceDetector
from main.utils import get_cap_name


def cmd_help(params):
    """
    python manage.py --help: For more information
    """
    from main.controllers import keys_handlers
    print('More information')
    for keys, render, p in keys_handlers:
        print(*keys, render.__doc__)


def run_face_detector(params: dict):
    """
    python manage.py <capture_name> --face: For detection faces
    """
    cap_name = get_cap_name(params)
    FaceDetector(cap_name, params).streem()


def run_hand_detector(params: dict):
    """
    python manage.py <capture_name> --hands: For detection hands
    """
    cap_name = get_cap_name(params)
    HandDetector(cap_name, params).streem()


def run_body_detector(params: dict):
    """
    python manage.py <capture_name> --body: For detections body
    """
    cap_name = get_cap_name(params)
    BodyDetector(cap_name, params).streem()


def run_person_detector(params: dict):
    """
    python manage.py <capture_name> --person: For detection person
    """
    cap_name = get_cap_name(params)
    CustomDetector(detectors=[
        BodyDetector(),
        HandDetector(),
        FaceDetector(),
    ], cap_name=cap_name, params=params).streem()


def run_body_hand_detector(params: dict):
    """
    python manage.py <capture_name> --hands --body: For detection hands and body
    """
    cap_name = get_cap_name(params)
    CustomDetector(detectors=[
        BodyDetector(),
        HandDetector(),
    ], cap_name=cap_name, params=params).streem()


def run_body_face_detector(params: dict):
    """
        python manage.py <capture_name> --face --body: for detection body and faces
        """
    cap_name = get_cap_name(params)
    CustomDetector(detectors=[
        BodyDetector(),
        FaceDetector(),
    ], cap_name=cap_name, params=params).streem()


def run_hand_face_detector(params: dict):
    """
        python manage.py <capture_name> --hands --face: For detection hands and faces
        """
    cap_name = get_cap_name(params)
    CustomDetector(detectors=[
        HandDetector(),
        FaceDetector(),
    ], cap_name=cap_name, params=params).streem()


def run_hand_body_face_detector(params: dict):
    """
    python manage.py <capture_name> --face --hands --body: For detection faces, hands and body
    """
    run_person_detector(params)

