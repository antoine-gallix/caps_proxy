import json
import logging

from caps_proxy import create_app
from flask import Response
from flask.testing import FlaskClient
from pathlib import Path
from pytest import fixture
from time import sleep


# ---------Test client with easy JSON features-----------------


class JSON_Client(FlaskClient):
    """Test client that sends json payloads

    instead of:

        test_client.post(some_url,
                        content_type='application/json',
                        data=json.dumps(some_dict))

    just do:

        json_test_client.post(some_url,
                        data=some_dict)

    """

    def open(self, *args, **kwargs):
        # encode data into json and set content type
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
            return super().open(*args, **kwargs,
                                content_type='application/json')
        else:
            return super().open(*args, **kwargs)


class Load_JSON_Response(Response):
    """Adds a method to load json data

    This is used as a response class by the app test client.
    """

    def load(self):
        return json.loads(self.json)


@fixture(scope='session')
def app():
    """Creates an app with a JSON enabled test client"""

    application = create_app()
    application.test_client_class = JSON_Client
    application.response_class = Load_JSON_Response
    return application


# -----------------------------------------------
