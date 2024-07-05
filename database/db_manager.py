import sqlite3

class DatabaseManager:
    def __init__(self, db_name="timemaster.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               username TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS timers (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               user_id INTEGER,
                               timer_type TEXT,
                               duration INTEGER,
                               FOREIGN KEY(user_id) REFERENCES users(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usage_logs (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               user_id INTEGER,
                               timer_id INTEGER,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                               FOREIGN KEY(user_id) REFERENCES users(id),
                               FOREIGN KEY(timer_id) REFERENCES timers(id))''')

        self.connection.commit()

    def add_user(self, username):
        self.cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        self.connection.commit()

    def close(self):
        self.connection.close()
