import sqlite3


DB_PATH = "data/final.db"

def get_conn(db_path=DB_PATH):

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

def init_db():

    conn = get_conn()
    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        height INTEGER,
        weight INTEGER,
        base_experience INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_types (
        pokemon_id INTEGER,
        type_name TEXT,
        PRIMARY KEY (pokemon_id, type_name),
        FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS github_repos (
        id INTEGER PRIMARY KEY,
        full_name TEXT UNIQUE,
        name TEXT,
        owner_login TEXT,
        stargazers_count INTEGER,
        forks_count INTEGER,
        language TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value INTEGER
    );
    """)

    cur.execute("INSERT OR IGNORE INTO meta(key, value) VALUES ('poke_offset', 0);")
    cur.execute("INSERT OR IGNORE INTO meta(key, value) VALUES ('gh_page', 1);")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized.")
