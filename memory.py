import sqlite3
from datetime import datetime
import os

class Memory:
    def __init__(self):
        self.session_context = {}  # Short-term memory
        self.db_path = "memory.db"
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS creations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      prompt TEXT, enhanced_prompt TEXT,
                      image_path TEXT, model_3d_path TEXT,
                      timestamp TEXT)''')
        conn.commit()
        conn.close()

    def save_creation(self, prompt: str, enhanced_prompt: str, image_path: str, model_3d_path: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute('INSERT INTO creations (prompt, enhanced_prompt, image_path, model_3d_path, timestamp) VALUES (?, ?, ?, ?, ?)',
                  (prompt, enhanced_prompt, image_path, model_3d_path, timestamp))
        conn.commit()
        conn.close()
        # Update session context
        self.session_context[prompt] = {
            "enhanced_prompt": enhanced_prompt,
            "image_path": image_path,
            "model_3d_path": model_3d_path
        }

    def recall(self, query: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM creations WHERE prompt LIKE ?', (f'%{query}%',))
        results = c.fetchall()
        conn.close()
        return results