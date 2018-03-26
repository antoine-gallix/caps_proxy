"""Test service
"""


def test_server_is_up(client):
    """smoke test"""
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json['output'] == 'pong'


def test_caps_service(client):
    """working example"""
    response = client.post('/to_caps', data={'input': 'caracoles'})
    assert response.status_code == 200
    assert response.json['output'] == 'CARACOLES'


# ---------------------errors---------------------


def test_caps_service_no_input(client):
    """no payload posted"""

    response = client.post('/to_caps')
    assert response.status_code == 400
    assert 'input error' in response.json['message']


def test_caps_service_float(client):
    """bytestring payload"""
    response = client.post('/to_caps', data={'input': 123.456})
    assert response.status_code == 400
    assert 'input error' in response.json['message']


def test_caps_service_wrong_http_method(client):
    response = client.get('/to_caps')
    assert response.status_code == 405
    assert '405 Method Not Allowed' in response.json['message']


def test_caps_service_wrong_endpoint(client):
    response = client.get('/to_the_disco')
    assert response.status_code == 404
    assert 'The requested URL was not found on the server' \
        in response.json['message']
