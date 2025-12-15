import requests
from db import get_conn, init_db

POKE_LIST_URL = "https://pokeapi.co/api/v2/pokemon"


def get_meta(conn, key):
    return conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()[0]

def set_meta(conn, key, value):
    conn.execute("UPDATE meta SET value=? WHERE key=?", (value, key))


def fetch_and_store_pokemon(batch_size=25):

    init_db()
    conn = get_conn()
    cur = conn.cursor()

    offset = get_meta(conn, "poke_offset")
    params = {
        "limit": batch_size, 
        "offset": offset
        }
    data = requests.get(POKE_LIST_URL, params=params, timeout=30).json()


    for item in data.get("results", []):

        detail = requests.get(item["url"], timeout=30).json()
        pid = int(detail["id"])
        name = detail["name"]
        height = detail.get("height")
        weight = detail.get("weight")
        base_exp = detail.get("base_experience")


        cur.execute("""
            INSERT OR IGNORE INTO pokemon(id, name, height, weight, base_experience)
            VALUES (?, ?, ?, ?, ?)
        """, (pid, name, height, weight, base_exp))


        for t in detail.get("types", []):

            type_name = t["type"]["name"]

            cur.execute("""
                INSERT OR IGNORE INTO pokemon_types(pokemon_id, type_name)
                VALUES (?, ?)
            """, (pid, type_name))


    set_meta(conn, "poke_offset", offset + batch_size)
    conn.commit()
    conn.close()

    
    print(f"Stored up to {batch_size} Pokémon. Next offset = {offset + batch_size}")


if __name__ == "__main__":
    fetch_and_store_pokemon(25)
