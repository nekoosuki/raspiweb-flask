import pytest
from flaskr.db import get_db

def test_config_interface(client, auth):
    response = client.get('/',follow_redirects=True)
    assert b'login' in response.data
    assert b'register' in response.data

    auth.login()

    response = client.get('/')
    assert b'logout' in response.data
    assert b'conf' in response.data
    assert b'iou' in response.data

def test_auth_config(client, app):
    response = client.post('/business/config',data={'conf':0.6,'iou':0.6})
    assert response.headers['Location'] == 'http://localhost/auth/login'
    with app.app_context():
        assert get_db().execute('SELECT * FROM user WHERE id = "1"').fetchone()['conf'] is None

@pytest.mark.parametrize(('conf','iou','message'),(
    (b'0.6',b'0.6',b'"conf": 0.6'),
    (b'1.1',b'0.5',b'"code": -1'),
    (b'-1',b'0.5',b'"code": -1'),
    (b'0',b'',b'"code": -1'),
))
def test_config(client,auth,conf,iou,message):
    auth.login()
    response = client.post('/business/config',data={'conf':conf,'iou':iou})
    assert message in response.data
    assert response.status_code == 200


