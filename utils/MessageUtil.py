from flask import make_response, jsonify


def log_message(message):
    print(message)


def log_message_response(message):
    print(message)

    return make_response(
            jsonify(
                message = message
            )
        )