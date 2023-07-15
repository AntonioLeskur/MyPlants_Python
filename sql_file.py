import sqlite3
import values_file

# SQL stuff

class UsersSql:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cur = self.conn.cursor()

    def create_user_table(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
        """)

    def import_starting_users(self):
        self.cur.execute("""
        INSERT OR REPLACE INTO users (id, username, password) VALUES
        (1, 'Admin', 'admin')
        """)
        self.conn.commit()

    def add_user(self, connection, username, password):
        INSERT_USER = "INSERT INTO users (username, password) VALUES (?, ?);"
        with connection:
            connection.execute(INSERT_USER, (username, password))
            connection.commit()

    def create_current_user_db(self):
        self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS current_user (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password TEXT
                    )""")
        self.conn.commit()


class PlantSql:
    def __init__(self):
        self.conn_plants = sqlite3.connect("plants_datab.db")
        self.c = self.conn_plants.cursor()

    def create_plant_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY,
    plant_name TEXT,
    plant_location TEXT,
    plant_humidity INTEGER,
    ph REAL,
    plant_sunlight INTEGER,
    plant_photo BLOB,
    plant_notes TEXT
)""")

    def import_starting_plants(self):
        self.c.executemany("INSERT OR REPLACE INTO plants VALUES (?,?,?,?,?,?,?,?)", values_file.STARTING_PLANTS)
        self.conn_plants.commit()
        self.conn_plants.close()
