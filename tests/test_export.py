def test_export_pdf_with_xml_special_characters(client):
    """Verify that ReportLab safely renders content containing <, >, &, and xml tags without error."""
    special_content = """Excited to announce our new release! <v2.0>
Tested with A & B scenarios where latency < 50ms and throughput > 1000 req/sec.
Check out: <https://example.com/demo?user=1&test=true>
<div>Safe html/xml text formatting</div>"""

    resp = client.post("/api/v1/export-pdf", json={"content": special_content})
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF")


def test_export_pdf_oversized_content_rejected(client):
    """Verify that PDF export rejects content larger than 5000 characters with 400."""
    oversized_content = "A" * 5001
    resp = client.post("/api/v1/export-pdf", json={"content": oversized_content})
    assert resp.status_code == 400
    assert "exceeds maximum" in resp.json()["detail"].lower()


def test_export_pdf_empty_content_rejected(client):
    resp = client.post("/api/v1/export-pdf", json={"content": "   "})
    assert resp.status_code == 400


def test_export_pdf_by_post_id(client):
    # First generate a post
    post_payload = {
        "topic": "Export Verification Post",
        "type": "tech",
        "length": "short"
    }
    gen_resp = client.post("/api/v1/generate-post", json=post_payload)
    assert gen_resp.status_code == 200
    post_id = gen_resp.json()["post"]["id"]

    # Export using post_id
    export_resp = client.post("/api/v1/export-pdf", json={"post_id": post_id})
    assert export_resp.status_code == 200
    assert export_resp.headers["content-type"] == "application/pdf"
    assert export_resp.content.startswith(b"%PDF")


def test_export_pdf_nonexistent_post_id(client):
    export_resp = client.post("/api/v1/export-pdf", json={"post_id": 999999})
    assert export_resp.status_code == 404
