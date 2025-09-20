def test_register_and_login(client):
    r = client.post("/api/auth/register", json={"username":"alice","password":"pass"})
    assert r.status_code == 200
    r2 = client.post("/api/auth/login", json={"username":"alice","password":"pass"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()
