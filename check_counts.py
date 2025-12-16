import sqlite3
from db import DB_PATH


conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

tables = ["pokemon", "pokemon_types", "github_repos"]

for t in tables:

    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]

    print(t, n)

conn.close()
