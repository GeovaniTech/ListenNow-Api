import base64


def bytes_to_base64(bytes_data):
    return base64.b64encode(bytes_data).decode('utf-8')

