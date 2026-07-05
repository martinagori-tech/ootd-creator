import sqlite3
import os
from PIL import Image
import io

DB_PATH = "data/wardrobe.db"
IMAGES_DIR = "data/images"

def init_db():
    os.makedirs("data/images", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_clothing_item(name, category, image_file):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    image_path = f"{IMAGES_DIR}/{name.replace(' ', '_')}.png"
    image = Image.open(image_file)
    image.save(image_path)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clothes (name, category, image_path) VALUES (?, ?, ?)",
        (name, category, image_path)
    )
    conn.commit()
    conn.close()

def get_all_clothes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, image_path FROM clothes")
    items = cursor.fetchall()
    conn.close()
    return items