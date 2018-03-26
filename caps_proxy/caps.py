"""Blueprint of the caps proxy service
"""
import flask
import requests
from flask_json import as_json
from flask import request, current_app, jsonify
from werkzeug.exceptions import HTTPException

service_blueprint = flask.Blueprint('caps_service', __name__)


@service_blueprint.route('/to_caps', methods=['POST'])
@as_json
def service_handler():
    """Convert string to caps

    This endpoint takes a string input and returns it converted to all caps.
    It uses an external service to do the conversion and spare some really
    heavy computations.

    expected json payload:
    {'input':"some_string"}

    return json payload:
    {
    'INPUT':"some_string",
    'OUTPUT':"SOME_STRING",
    }
    """
    # input checking
    try:
        input_data = request.json['input']
        if not isinstance(input_data, str):
            raise TypeError

    except Exception:
        current_app.logger.debug('input error')
        return {
            'message': 'input error. send json input in the as follow: '
            '"{"input":"string to be capitalized"}"'
        }, 400

    current_app.logger.debug('received string :"{}"'.format(input_data))

    # forward string to external caps service
    service_url = current_app.config['CAPS_SERVICE_URL']
    current_app.logger.debug(
        'forwarding call to caps service at "{}"'.format(service_url)
    )
    service_response = requests.post(service_url, json={'input': input_data})
    if not service_response.ok:
        return {'message': 'caps conversion failed'}, 500

    returned_data = service_response.json()

    # repackage service response
    our_response = {
        'input': returned_data['INPUT'], 'output': returned_data['OUTPUT']}
    return our_response


@service_blueprint.errorhandler(HTTPException)
def handle_error(e):
    # translates all http errors coming from this blueprint into json errors
    return jsonify(error=str(e)), e.code
