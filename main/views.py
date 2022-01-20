
def cmd_help():
    text = """
    --help: For more information

    --face: For face detection

    --face-mesh: For face mesh detection

    --hand: For hands detection

    --body: for body detection
    """
    print('More Information')
    print(text)


def view(layers, params):
    from main.models import CustomDetector

    cap_name = params['cap_name']
    CustomDetector(detectors=layers, cap_name=cap_name, params=params).streem()

