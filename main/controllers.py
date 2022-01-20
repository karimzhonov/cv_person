from main.utils import cmd_handler
from main.views import *

keys_handlers = [
    cmd_handler(keys=('--help',), render=cmd_help),
    cmd_handler(keys=('--hands',), render=run_hand_detector),
    cmd_handler(keys=('--body',), render=run_body_detector),
    cmd_handler(keys=('--face',), render=run_face_detector),
    cmd_handler(keys=('--person',), render=run_person_detector),

    cmd_handler(keys=('--body', '--hands'), render=run_body_hand_detector),
    cmd_handler(keys=('--body', '--face'), render=run_hand_face_detector),
    cmd_handler(keys=('--face', '--hands'), render=run_hand_face_detector),
    cmd_handler(keys=('--body', '--hands', '--face'), render=run_person_detector),
]
