import sqlite3
import os
from datetime import datetime
import logging

class Memory:
    def __init__(self):
        self.session_context = {}  # Short-term memory
        self.db_path = os.getenv("DB_PATH", "memory.db")
        try:
            self.init_db()
        except Exception as e:
            logging.error(f"Failed to initialize database: {e}")
            raise

    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS creations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          prompt TEXT, enhanced_prompt TEXT,
                          image_path TEXT, model_3d_path TEXT,
                          timestamp TEXT)''')
            conn.commit()
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            raise
        finally:
            conn.close()

    def save_creation(self, prompt: str, enhanced_prompt: str, image_path: str, model_3d_path: str):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            timestamp = datetime.now().isoformat()
            c.execute('INSERT INTO creations (prompt, enhanced_prompt, image_path, model_3d_path, timestamp) VALUES (?, ?, ?, ?, ?)',
                      (prompt, enhanced_prompt, image_path, model_3d_path, timestamp))
            conn.commit()
            # Update session context
            self.session_context[prompt] = {
                "enhanced_prompt": enhanced_prompt,
                "image_path": image_path,
                "model_3d_path": model_3d_path
            }
        except Exception as e:
            logging.error(f"Failed to save creation: {e}")
            raise
        finally:
            conn.close()

    def recall(self, query: str):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('SELECT * FROM creations WHERE prompt LIKE ?', (f'%{query}%',))
            results = c.fetchall()
          
            return results
        except Exception as e:
            logging.error(f"Failed to recall creations: {e}")
            raise
        finally:
            conn.close()