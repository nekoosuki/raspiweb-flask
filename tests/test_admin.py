from flaskr.db import get_db

def test_auth_admin(client, auth):
    auth.login()
    response = client.get('/admin/lookup')
    assert response.headers['Location'] == 'http://localhost/'

    auth.logout()
    auth.login(devname='testadmin', password='testadmin')
    response = client.get('/admin/lookup')
    assert response.status_code == 200

def test_admin(client, auth):
    auth.login(devname='testadmin', password='testadmin')
    response = client.get('/admin/lookup')
    assert b'other' in response.data

def test_set(client, auth):
    auth.login(devname='testadmin', password='testadmin')
    response = client.post('/admin/lookup', data={'id':1, 'isadmin':'y'})
    assert response.status_code == 200
    auth.logout()
    auth.login()
    response = client.get('/')
    assert b'admin' in response.data

def test_delete(client, auth, app):
    auth.login(devname='testadmin', password='testadmin')
    client.post('/admin/delete', data={'id':3})
    response = client.get('admin/lookup')
    assert b'other' not in response.data
    with app.app_context():
        db = get_db()
        assert db.execute('SELECT * FROM user WHERE id = 3').fetchone() is None
