import pytest
import os
import sqlite3

from gtts import gTTS

from backend.src.main import app

DATABASE_FILE = os.getenv("DATABASE_FILE")
DATA_PATH = os.getenv("FLOSSCASTER_DATA_PATH")

@pytest.fixture()
def init_testing():
    app.config.update({'TESTING': True})
    yield app
    app.config.update({'TESTING': False})

@pytest.fixture()
def empty_database(init_testing):
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date, filepath)")
    con.close()

@pytest.fixture()
def client(init_testing):
    return app.test_client()