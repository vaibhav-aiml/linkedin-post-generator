def test_analyze_text(client):
    text_to_test = """Excited to share our team's achievement in building an AI pipeline!

We reduced latent processing time by 45% using optimized models.

What tools are you using for optimization? #AI #SoftwareEngineering #Tech #Growth"""

    payload = {"text": text_to_test}
    response = client.post("/api/v1/analyze-text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]
    assert analysis["score"] > 50
    assert analysis["word_count"] > 10
    assert analysis["hashtag_count"] == 4
    assert analysis["question_count"] == 1
