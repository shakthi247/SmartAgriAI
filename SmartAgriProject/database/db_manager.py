"""
Minimal database manager for Smart Agriculture AI
"""
import sqlite3
from pathlib import Path

class AgriDB:
    def __init__(self):
        self.db_path = Path(__file__).parent / "agriculture.db"
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS crops (
                name TEXT PRIMARY KEY,
                soil_min INTEGER,
                season TEXT,
                category TEXT,
                price REAL,
                yield_qty REAL,
                cost REAL
            )''')
            
            # Insert basic crop data
            crops = [
                ('wheat', 6, 'winter', 'cereals', 2200, 45, 35000),
                ('rice', 7, 'monsoon', 'cereals', 2800, 40, 45000),
                ('corn', 6, 'summer', 'cereals', 1800, 50, 38000),
                ('potato', 6, 'winter', 'vegetables', 1200, 250, 60000),
                ('tomato', 6, 'summer', 'vegetables', 1500, 300, 65000),
                ('cotton', 6, 'summer', 'cash_crops', 6000, 20, 55000),
                ('soybean', 5, 'summer', 'legumes', 3800, 25, 32000),
                ('mustard', 5, 'winter', 'oilseeds', 4800, 15, 32000)
            ]
            
            conn.executemany('INSERT OR IGNORE INTO crops VALUES (?,?,?,?,?,?,?)', crops)
    
    def get_crop_data(self, crop_name=None):
        """Get crop data"""
        with sqlite3.connect(self.db_path) as conn:
            if crop_name:
                return conn.execute('SELECT * FROM crops WHERE name=?', (crop_name,)).fetchone()
            return conn.execute('SELECT * FROM crops').fetchall()
    
    def get_crops_by_season(self, season):
        """Get crops by season"""
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute('SELECT name FROM crops WHERE season=?', (season,)).fetchall()

# Global instance
db = AgriDB()