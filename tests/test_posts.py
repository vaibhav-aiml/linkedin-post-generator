def test_generate_post_and_get_history(client):
    post_payload = {
        "topic": "Artificial Intelligence in Software Development",
        "type": "tech",
        "length": "medium",
        "tone": "insightful"
    }
    response = client.post("/api/v1/generate-post", json=post_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "post" in data
    assert data["post"]["topic"] == "Artificial Intelligence in Software Development"
    assert len(data["post"]["content"]) > 20

    # Verify history
    history_resp = client.get("/api/v1/get-history")
    assert history_resp.status_code == 200
    hist_data = history_resp.json()
    assert hist_data["success"] is True
    assert hist_data["count"] >= 1


def test_generate_message(client):
    msg_payload = {
        "recipient_name": "Jane Smith",
        "context": "AI in Healthcare Conference",
        "purpose": "networking"
    }
    response = client.post("/api/v1/generate-message", json=msg_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Jane" in data["message"]
