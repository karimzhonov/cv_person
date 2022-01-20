from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.pose import Pose, POSE_CONNECTIONS
from mediapipe.python.solutions.face_mesh import FaceMesh

from main.utils import Detector
from config import *


class HandDetector(Detector):
    def __init__(self, *args, **kwargs):
        Detector.__init__(self,
                          id_list=HAND_LANDMARK_ID_LIST,
                          max_count=MAX_NUM_HANDS,
                          *args, **kwargs)

        self.mediapipe_detector = Hands(max_num_hands=self.max_count)
        self.draw_connection = HAND_CONNECTIONS

    def get_landmarks(self, img_rgb):
        return self.mediapipe_detector.process(img_rgb).multi_hand_landmarks


class BodyDetector(Detector):
    def __init__(self, *args, **kwargs):
        Detector.__init__(self,
                          id_list=BODY_LANDMARK_ID_LIST,
                          max_count=MAX_COUNT_BODY,
                          *args, **kwargs)

        self.mediapipe_detector = Pose()
        self.draw_connection = POSE_CONNECTIONS

    def get_landmarks(self, img_rgb):
        return [self.mediapipe_detector.process(img_rgb).pose_landmarks]


class FaceDetector(Detector):
    def __init__(self, *args, **kwargs):
        Detector.__init__(self,
                          id_list=FACE_LANDMARK_ID_LIST, max_count=1,
                          *args, **kwargs)

        self.mediapipe_detector = FaceMesh(max_num_faces=MAX_COUNT_FACE)
        self.draw_connection = None

    def get_landmarks(self, img_rgb):
        return self.mediapipe_detector.process(img_rgb).multi_face_landmarks


class CustomDetector(Detector):
    def __init__(self, detectors: list, *args, **kwargs):
        Detector.__init__(self, draw=True,
                          id_list=[], max_count=MAX_COUNT_PERSON,
                          *args, **kwargs)
        self.detectors = detectors

    def get_coordinate(self, img, _id=None):
        res = []
        for detector in self.detectors:
            coordinates, img = detector.get_coordinate(img)
            res += coordinates
        return res, img


