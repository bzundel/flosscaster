import os

DATABASE_FILE = os.getenv("DATABASE_FILE")

def test_list_empty_db(empty_database, client):
    response = client.get("/api/list")
    assert response.status_code == 200
    assert b'[]' in response.data

def test_list(database_entry_id, client):
    response = client.get("/api/list")
    assert response.status_code == 200
    assert f"\"id\":{database_entry_id}".encode("utf8") in response.data
    assert b"\"title\":" in response.data
    assert b"\"date\":" in response.data
    assert b"\"description\":" in response.data
    assert b"\"filepath\":" in response.data

def test_list_with_param(database_entry_id, client):
    response = client.get("/api/list/")
    response2 = client.get("/api/list/test")
    assert response.status_code == 404
    assert response2.status_code == 404