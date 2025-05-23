import os

def test_getrss(create_rss, client):
    response = client.get("/rss")
    assert "text/xml" in response.headers["content-type"]
    assert response.status_code == 200 or response.status_code == 304

def test_getrss_no_file(delete_rss, client):
    response = client.get("/rss")
    assert response.status_code == 404
    if not delete_rss == "failure":
        rss_path = os.getenv("RSS_FILE")
        with open(rss_path, "w") as file:
            file.write(delete_rss)
