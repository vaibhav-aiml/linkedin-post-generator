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


def test_analyzer_rewrites_user_text_specifically(client):
    """Verify that analyzer's improved version actually rewrites the user's text and preserves its core content."""
    original_text = "We just deployed a new Kubernetes cluster with zero downtime across three regions."

    response = client.post("/api/v1/analyze-text", json={"text": original_text})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]

    corrected = analysis["corrected_version"]
    assert corrected is not None and len(corrected) > len(original_text)
    # Assert substantial content of the original text is retained
    assert "Kubernetes cluster" in corrected or "zero downtime" in corrected
    assert "three regions" in corrected or "deployed" in corrected
    # Assert missing elements (question and hashtags) were added
    assert "?" in corrected
    assert "#" in corrected


def test_analyzer_empty_text(client):
    response = client.post("/api/v1/analyze-text", json={"text": "   "})
    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["score"] == 0
    assert data["analysis"]["word_count"] == 0

