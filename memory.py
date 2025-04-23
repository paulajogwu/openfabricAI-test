import sqlite3
from datetime import datetime
import os
from typing import List, Tuple

class Memory:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self) -> None:
        """Initialize database with proper error handling"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS creations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prompt TEXT NOT NULL,
                        enhanced_prompt TEXT,
                        image_path TEXT,
                        model_3d_path TEXT,
                        timestamp TEXT
                    )
                ''')
                # Add index for faster searches
                conn.execute('CREATE INDEX IF NOT EXISTS idx_prompt ON creations(prompt)')
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to initialize database: {str(e)}")

    def save_creation(self, prompt: str, enhanced_prompt: str, 
                     image_path: str, model_3d_path: str = None) -> None:
        """Save creation with transaction support"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    '''INSERT INTO creations 
                    (prompt, enhanced_prompt, image_path, model_3d_path, timestamp)
                    VALUES (?, ?, ?, ?, ?)''',
                    (prompt, enhanced_prompt, image_path, model_3d_path, datetime.now().isoformat())
                )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to save creation: {str(e)}")

    def recall(self, query: str) -> List[Tuple]:
        """Search creations with parameterized query"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT * FROM creations 
                    WHERE prompt LIKE ? 
                    ORDER BY timestamp DESC''',
                    (f'%{query}%',)
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to recall creations: {str(e)}")