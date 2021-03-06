import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={'devname':'a', 'password':'a', 'admin':''})
    assert response.headers['Location'] == 'http://localhost/auth/login' 
    with app.app_context():
        db = get_db()
        assert db.execute('SELECT * FROM user WHERE devname = "a"').fetchone() is not None
        assert db.execute('SELECT conf FROM user WHERE devname="a"').fetchone() is not None

    response = client.post('/auth/register', data={'devname':'b', 'password':'b', 'admin':'neko'})
    assert response.headers['Location'] == 'http://localhost/auth/login'

@pytest.mark.parametrize(('devname', 'password', 'admin', 'message'),(
    ('','','',b'Devname is required'),
    ('a','','',b'Password is required'),
    ('test','test','',b'already registered'),
))
def test_register_validata_input(client, devname, password, admin, message):
    response=client.post(
        '/auth/register',
        data = {'devname':devname,'password':password,'admin':admin},
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    respose = auth.login()
    assert respose.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['id'] == 1
        assert g.dev['devname'] == 'test'
    
    auth.logout()
    
    respose = auth.login(devname='testadmin',password='testadmin')
    assert respose.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['id'] == 2
        assert g.dev['devname'] == 'testadmin'


@pytest.mark.parametrize(('devname','password','message'),(
    ('a','test',b'Incorrect devname'),
    ('test','a',b'Incorrect password'),
))
def test_login_validate_input(auth, devname, password, message):
    response = auth.login(devname, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'id' not in session
