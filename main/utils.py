
def max_arg(array: list):
    m = array[0]
    k = 0
    for i, point in enumerate(array):
        if m < point:
            m = point
            k = i
    return k


def cmd_handler(keys: tuple, render, params: dict):
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
    params['keys'] = keys
    render(params)


def run(sys_args: list):
    _flags = sys_args[1:]
    start_cmd_handlers(_flags)
