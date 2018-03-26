"""Application creation

Application components are assembled here at application startup
"""
import flask
import logging.config
import yaml

from caps_proxy import config
from flask_json import FlaskJSON
from flask_json import as_json

# ------------------Test endpoint------------------------


test_blueprint = flask.Blueprint('test', __name__)


@test_blueprint.route('/ping')
@as_json
def test_handler():
    """A test endpoint to check if the app is running
    """
    return {'output': 'pong'}

# ---------------------Application object creation--------------------------


def create_app():
    """Application object factory"""
    app = flask.Flask('caps_proxy')

    # configure logging
    logger = app.logger
    logging.config.dictConfig(yaml.load(open('caps_proxy/logging.conf')))

    # apply config
    logger.info('=' * 50)
    logger.info('application startup')
    app.config.from_object(config)

    # initialize extensions
    FlaskJSON(app)

    # register blueprints
    app.register_blueprint(test_blueprint)
    from .caps import service_blueprint
    app.register_blueprint(service_blueprint)

    # for http errors coming from routing or generic 500 error
    # override default HTML errors with JSON errors

    @app.errorhandler(404)
    def page_not_found(e):
        return flask.jsonify(error=404, message=str(e)), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return flask.jsonify(error=405, message=str(e)), 405

    @app.errorhandler(500)
    def internal_error(e):
        return flask.jsonify(error=500, message=str(e)), 500

    logger.info('application ready to serve')

    return app
