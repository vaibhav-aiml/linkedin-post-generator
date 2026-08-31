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

    post_id = data["post"]["id"]

    # Verify detail retrieval (unassigned post allowed for creator session)
    post_detail = client.get(f"/api/v1/get-post/{post_id}")
    assert post_detail.status_code == 200

    # Verify history
    history_resp = client.get("/api/v1/get-history")
    assert history_resp.status_code == 200
    hist_data = history_resp.json()
    assert hist_data["success"] is True
    assert hist_data["count"] >= 1


def test_generate_post_with_document_context(client):
    """Test that post generation with document_context grounds the post in the provided context."""
    doc_context = "AWS Certified Solutions Architect – Associate, Issued by Amazon Web Services, Completed August 2026, Credential ID AWS-987654"
    post_payload = {
        "topic": "Cloud Architecture Certification",
        "type": "achievement",
        "length": "medium",
        "tone": "celebratory",
        "document_context": doc_context
    }
    response = client.post("/api/v1/generate-post", json=post_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["post"]["document_context"] == doc_context
    content = data["post"]["content"]
    assert "AWS Certified Solutions Architect" in content or "Credential" in content or "AWS-987654" in content


def test_delete_history_requires_auth(client):
    # Unauthenticated delete-history should fail (401 Unauthorized)
    response = client.delete("/api/v1/delete-history")
    assert response.status_code == 401


def test_llm_provider_prompt_includes_document_context(client, monkeypatch):
    """Test that LLM provider receives document_context and is invoked with proper arguments."""
    from unittest.mock import MagicMock
    from backend.app.services.llm_service import LLMFactory

    mock_provider = MagicMock()
    mock_provider.generate_post.return_value = "Grounded LinkedIn Post Content"
    mock_provider.generate_hashtags.return_value = ["#Test", "#Context"]

    monkeypatch.setattr(LLMFactory, "get_provider", lambda: mock_provider)

    doc_context = "Stanford Machine Learning Specialization, Grade 99.4%"
    payload = {
        "topic": "Machine Learning Journey",
        "type": "career",
        "length": "medium",
        "tone": "insightful",
        "document_context": doc_context
    }

    response = client.post("/api/v1/generate-post", json=payload)
    assert response.status_code == 200

    # Verify provider was called with the document_context
    mock_provider.generate_post.assert_called_once_with(
        topic="Machine Learning Journey",
        post_type="career",
        length="medium",
        tone="insightful",
        document_context=doc_context
    )


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



