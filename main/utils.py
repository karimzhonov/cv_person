import cv2
import time
from config import COLOR


def draw_circles(img, coordinates: list):
    for (cx, cy) in coordinates:
        img = cv2.circle(img, (cx, cy), 2, COLOR, cv2.FILLED)
    return img


def get_cap_name(params):
    try:
        cap_name = int(params['cap_name'])
    except IndexError:
        raise 'Enter Capture'
    except ValueError:
        cap_name = params['cap_name']
    return cap_name


def imshow(frame):
    try:
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow('Video')
            return False
        return True
    except cv2.error:
        return False


def max_arg(array: list):
    m = array[0]
    k = 0
    for i, point in enumerate(array):
        if m < point:
            m = point
            k = i
    return k


def cmd_handler(keys: tuple, render, params: dict = {}):
    return keys, render, params


def start_cmd_handlers(_flags):
    from main.controllers import keys_handlers
    response = []
    for keys, render, params in keys_handlers:
        counter = 0
        for key in keys:
            if key in _flags:
                counter += 1
        response.append(counter)
    res = max_arg(response)
    keys, render, params = keys_handlers[res]
    try:
        params['cap_name'] = _flags[0]
        params['keys'] = keys
        params['flags'] = _flags
    except IndexError:
        pass
    render(params)


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

    def get_coordinate(self, img, _id=None):
        """
        Get Coordinate
        :param img: Image
        :param _id: None or int
        :return: List coordinates and Image
        """
        coordinates = []
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except cv2.error:
            return [], img
        else:
            if not _id:
                fingers_ids = self.id_list
            else:
                fingers_ids = [self.id_list[_id]]

            landmarks = self.get_landmarks(img_rgb)
            if landmarks:
                for point in landmarks:
                    for idd in fingers_ids:
                        if point:
                            finger = point.landmark[idd]
                            h, w, c = img_rgb.shape
                            cx, cy = int(finger.x * w), int(finger.y * h)
                            coordinates.append((cx, cy))
                            # img = cv2.putText(img, str(idd), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 0.6, COLOR, 1)
                    # if self.draw:
                    #     draw_landmarks(img, point, self.draw_connection)
            return coordinates, img

    def streem(self):
        cap = cv2.VideoCapture(self.cap_name)
        _, img = cap.read()
        print('For quit press "q"')
        while imshow(img):
            _, img = cap.read()
            coordinates, img = self.get_coordinate(img)
            if self.draw:
                img = draw_circles(img, coordinates)
            img = self.set_fps(img)
