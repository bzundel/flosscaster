import pytest
import os

from pathlib import Path

from backend.src.main import UPLOAD_PATH
from backend.tests.random_file_generator import generate_random_ascii, generate_random_ascii_path, generate_mp3_size, generate_mp3_tts, generate_mp3_duration

@pytest.mark.parametrize("title, description, audio", [
    ("First FLOSScast", "The very first flosscast", generate_mp3_tts("Hello to the very first flosscast episode.", lang="en")),
    (generate_random_ascii(length=10), generate_random_ascii(length=99), generate_mp3_size(1024)),
    (generate_random_ascii(length=24, letters=False, numbers =False, punctuation=True), generate_random_ascii(length=240, punctuation=True), generate_mp3_duration(30))
])


def test_create_podcasts(client, title, description, audio):
    response = client.post("/api/create", content_type="multipart/form-data",
                           data={
        "title": title,
        "description": description,
        "audio": open(audio, 'rb')
    })
    assert response.status_code == 200