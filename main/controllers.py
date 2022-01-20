from main.utils import cmd_handler
from main.views import *

keys_handlers = [
    cmd_handler(keys=('--help',), render=cmd_help, params={})
]
