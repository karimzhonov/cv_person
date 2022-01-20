import cv2
import time
from config import COLOR
from main.views import view


def draw_circles(img, coordinates: list):
    for cx, cy in coordinates:
        img = cv2.circle(img, (cx, cy), 2, COLOR, cv2.FILLED)
    return img


def imshow(frame):
    try:
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow('Video')
            return False
        return True
    except cv2.error:
        return False


def start_cmd_handlers(_flags):
    from main.controllers import key_handlers
    layers = []
    for key in _flags[1:]:
        for flag, layer in key_handlers:
            if key == flag:
                layers.append(layer())

    params = {
        '_flags': _flags
    }
    try:
        params['cap_name'] = int(_flags[0])
        view(layers, params=params)
    except IndexError:
        from main.views import cmd_help
        cmd_help()
    except ValueError:
        params['cap_name'] = _flags[0]
        view(layers, params=params)


def run(sys_args: list):
    _flags = sys_args[1:]
    start_cmd_handlers(_flags)


class Detector:
    p_time = 0

    def __init__(self, cap_name=None, params=None, id_list=None, max_count=None, draw=True):
        self.cap_name = cap_name
        self.params = params
        self.id_list = id_list
        self.max_count = max_count
        self.draw = draw
        self.mediapipe_detector = None
        self.draw_connection = None

    def set_fps(self, img):
        c_time = time.time()
        fps = 1/(c_time - self.p_time)
        self.p_time = c_time
        return cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

    def get_landmarks(self, img_rgb):
        pass

    def insert_coordinate_from_point(self, point, img_shape, _id_list=None):
        h, w, c = img_shape
        if not _id_list:
            fingers_ids = self.id_list
        else:
            fingers_ids = [self.id_list[_id] for _id in _id_list ]
        res = []
        for idd in fingers_ids:
            finger = point.landmark[idd]
            cx, cy = int(finger.x * w), int(finger.y * h)
            res.append((cx, cy))
        return res

    def get_coordinate(self, img, _id_list=None):
        """
        Get Coordinate
        :param img: Image
        :param _id_list: list of id
        :return: List coordinates and Image
        """
        coordinates = []
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except cv2.error:
            return coordinates
        else:
            landmarks = self.get_landmarks(img_rgb)
            if landmarks:
                for point in landmarks:
                    if point:
                        res = self.insert_coordinate_from_point(point, img_rgb.shape, _id_list=_id_list)
                        coordinates += res
            return coordinates

    def streem(self):
        cap = cv2.VideoCapture(self.cap_name)
        _, img = cap.read()
        print('For quit press "q"')
        while imshow(img):
            _, img = cap.read()
            coordinates = self.get_coordinate(img)
            if self.draw:
                img = draw_circles(img, coordinates)
            img = self.set_fps(img)
