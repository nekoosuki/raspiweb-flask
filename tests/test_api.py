def test_api_query(client):
    response = client.post('/api/query_config', data={'n':'unreg','p':'neko'})
    assert response.get_json()['code'] == -1

    response = client.post('/api/query_config', data={'n':'other','p':'n'})
    assert response.get_json()['code'] == -1

    response = client.post('/api/query_config', data={'n':'other','p':'neko'})
    j = response.get_json()
    assert j['code'] == 0
    assert j['conf'] == 0.5
