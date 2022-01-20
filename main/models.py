from main.utils import Detector
from config import *


class HandDetector(Detector):
    def __init__(self, *args, **kwargs):
        Detector.__init__(self, id_list=HAND_LANDMARK_ID_LIST, max_count=MAX_NUM_HANDS, *args, **kwargs)
        from mediapipe.python.solutions.hands import Hands

        self.mediapipe_detector = Hands(max_num_hands=self.max_count)

    def get_landmarks(self, img_rgb):
        return self.mediapipe_detector.process(img_rgb).multi_hand_landmarks


class BodyDetector(Detector):
    """--body"""
    def __init__(self, *args, **kwargs):
        Detector.__init__(self, id_list=BODY_LANDMARK_ID_LIST, max_count=MAX_COUNT_BODY, *args, **kwargs)
        from mediapipe.python.solutions.pose import Pose

        self.mediapipe_detector = Pose()

    def get_landmarks(self, img_rgb):
        return [self.mediapipe_detector.process(img_rgb).pose_landmarks]


class FaceMeshDetector(Detector):
    """--face-mesh"""
    def __init__(self, *args, **kwargs):
        Detector.__init__(self, id_list=FACE_LANDMARK_ID_LIST, max_count=MAX_COUNT_FACE, *args, **kwargs)
        from mediapipe.python.solutions.face_mesh import FaceMesh

        self.mediapipe_detector = FaceMesh(max_num_faces=self.max_count)

    def get_landmarks(self, img_rgb):
        return self.mediapipe_detector.process(img_rgb).multi_face_landmarks


class FaceDetector(Detector):
    """--face"""
    def __init__(self, *args, **kwargs):
        Detector.__init__(self, id_list=FACE_LANDMARK_ID_LIST, max_count=MAX_COUNT_FACE, *args, **kwargs)
        from mediapipe.python.solutions.face_detection import FaceDetection

        self.mediapipe_detector = FaceDetection()

    def get_landmarks(self, img_rgb):
        return self.mediapipe_detector.process(img_rgb).detections

    def insert_coordinate_from_point(self, point, img_shape, _id_list=None):
        h, w, c = img_shape
        res = []
        coord = point.location_data.relative_bounding_box
        left, top, ww, hh = coord.xmin, coord.ymin, coord.width, coord.height
        res.append((int(left*w), int(top*h)))
        res.append((int((left+ww)*w), int(top*h)))
        res.append((int(left*w), int((top+hh)*h)))
        res.append((int((left+ww)*w), int((top+hh)*h)))
        return res


class CustomDetector(Detector):
    def __init__(self, detectors: list, cap_name=None, params=None, max_count=1):
        """
        Custom Detector
        :param detectors: list of Detectors
        :param max_count: Max count detection element
        :param cap_name: Video path(0 - webcam)
        :param params: dict of params
        """
        Detector.__init__(self, cap_name, params, max_count)
        self.detectors = detectors

    def get_coordinate(self, img, _id_list: list = None):
        res = []
        for detector in self.detectors:
            coordinates = detector.get_coordinate(img, _id_list=_id_list)
            res += coordinates
        return res
