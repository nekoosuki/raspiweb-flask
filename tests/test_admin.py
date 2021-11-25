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

def test_set_admin(client, auth):
    auth.login(devname='testadmin', password='testadmin')
    response = client.post('/admin/lookup', data={'id':1, 'isadmin':'y'})
    assert response.status_code == 200
    auth.logout()
    auth.login()
    response = client.get('/')
    assert b'admin' in response.data
