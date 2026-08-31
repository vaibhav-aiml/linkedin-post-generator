import pytest


def test_generate_post_rate_limit_exceeded(client):
    """Verify that rate limiter returns 429 when exceeding 10 requests/minute on generate-post."""
    post_payload = {
        "topic": "Testing Rate Limits in FastAPI",
        "type": "tech",
        "length": "short",
        "tone": "direct"
    }

    # First 10 requests should succeed (200 OK)
    for i in range(10):
        resp = client.post("/api/v1/generate-post", json=post_payload)
        assert resp.status_code == 200, f"Request {i+1} failed with status {resp.status_code}"

    # 11th request within the same minute should be throttled (429 Too Many Requests)
    excess_resp = client.post("/api/v1/generate-post", json=post_payload)
    assert excess_resp.status_code == 429
    assert "rate limit exceeded" in excess_resp.text.lower() or "too many requests" in excess_resp.text.lower()


def test_health_check_exempt_from_rate_limit(client):
    """Verify that health check route is exempt and not throttled even with rapid successive calls."""
    for _ in range(15):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"
