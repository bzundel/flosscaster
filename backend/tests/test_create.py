import pytest

from pathlib import Path
from backend.src.main import app
from backend.tests.random_file_generator import generate_random_ascii, generate_random_ascii_path, generate_mp3_size, generate_mp3_tts, generate_mp3_duration

@pytest.mark.parametrize("title, description, audio", [
    ("First FLOSScast", "The very first flosscast", generate_mp3_tts("Hello to the very first flosscast episode.", lang="en")),
    (generate_random_ascii(length=100), generate_random_ascii(length=1000), generate_mp3_size(10240)),
    (generate_random_ascii(length=24, letters=False, numbers =False, punctuation=True, printable=True), generate_random_ascii(length=240, punctuation=True, printable=True), generate_mp3_duration(300))
])


def test_create_podcasts(init_testing, title, description, audio):
    client = app.test_client()
    with open(audio, "rb") as audio_file:
        response = client.post("/api/create", data={
            "title": title,
            "description": description,
            "audio": audio_file,
        })
    assert response.status_code == 200