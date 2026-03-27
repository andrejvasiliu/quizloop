from flask import jsonify


def error_response(message, status):
    """Helper for returning jsonified error messages including status code."""
    return jsonify({"error": message}), status
