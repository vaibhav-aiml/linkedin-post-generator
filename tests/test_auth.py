def test_register_and_login_user(client):
    # Test Register
    reg_payload = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["email"] == "testuser@example.com"
    assert "id" in user_data

    # Test Duplicate Register
    dup_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_resp.status_code == 400

    # Test Login
    login_payload = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    login_resp = client.post("/api/v1/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert "access_token" in login_resp.cookies

    # Test Profile
    profile_resp = client.get("/api/v1/auth/me")
    assert profile_resp.status_code == 200
    profile_data = profile_resp.json()
    assert profile_data["email"] == "testuser@example.com"
