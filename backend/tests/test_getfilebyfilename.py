from backend.tests.random_file_generator import generate_random_ascii

def test_getFileByFilename(upload_file, client):
    response = client.get(f"/api/get_upload/{upload_file}")
    assert response.status_code == 200
    assert "audio/mpeg" in response.headers["content-type"]

def test_getFileByFilename_wrong(client):
    request = "/api/get_upload/" + generate_random_ascii(length=32)
    response = client.get(request)
    assert response.status_code == 404