import uuid
from datetime import datetime

import pytest
import os
import sqlite3

from backend.src.main import app

DATABASE_FILE = os.getenv("DATABASE_FILE")
DATA_PATH = os.getenv("UPLOAD_PATH")

@pytest.fixture()
def init_testing():
    app.config.update({'TESTING': True})
    if not os.path.exists(DATABASE_FILE):
        con = sqlite3.connect(DATABASE_FILE)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date, filepath)")
        con.close()
    yield app
    app.config.update({'TESTING': False})

@pytest.fixture()
def client(init_testing):
    with app.test_client() as client:
        yield client

@pytest.fixture()
def empty_database(init_testing):
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS podcasts(id INTEGER PRIMARY KEY, title, description, date, filepath)")
    con.close()

@pytest.fixture()
def database_entry_id(init_testing):
    title = "Test entry"
    description = "Test description"
    date = datetime.now().strftime("%c")
    filename = f"{str(uuid.uuid4())}.mp3"
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("INSERT INTO podcasts (id, title, description, date, filepath) VALUES (NULL, ?,?,?,?)", (title, description, date, filename))
    lastid = cur.lastrowid
    con.commit()
    con.close()
    return lastid