import uuid
from datetime import datetime

import pytest
import os
import sqlite3

from backend.src.main import app
from backend.tests.random_file_generator import generate_mp3_size
from backend.src.tools import rss_helper

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

@pytest.fixture()
def upload_file(init_testing):
    path = generate_mp3_size()
    return path.replace(DATA_PATH + "/", "")

@pytest.fixture()
def create_rss(init_testing):
    rss_file = os.getenv("RSS_FILE")
    url = os.getenv("FRONTEND_URL")
    if not os.path.exists(rss_file):
        rss_helper.create_template_if_not_exists()
        rss_helper.add_episode_to_podcast("test", url, "fuer testzwecke", "42")

@pytest.fixture()
def delete_rss(init_testing):
    rss_path = os.getenv("RSS_FILE")
    if os.path.exists(rss_path):
        file = open(rss_path, "r")
        rss_file = file.read()
        file.close()
        os.remove(rss_path)
        return rss_file
    return "failure"
