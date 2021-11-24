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
