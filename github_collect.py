import requests
from db import get_conn, init_db



GH_SEARCH_URL = "https://api.github.com/search/repositories"


def get_meta(conn, key):
    return conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()[0]

def set_meta(conn, key, value):
    conn.execute("UPDATE meta SET value=? WHERE key=?", (value, key))

def fetch_and_store_repos(per_page=25):

    init_db()
    conn = get_conn()
    cur = conn.cursor()

    page = get_meta(conn, "gh_page")


    params = {
        "q": "stars:>50000",   
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
        "page": page
    }

    resp = requests.get(GH_SEARCH_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()


    for r in data.get("items", []):

        cur.execute("""
            INSERT OR IGNORE INTO github_repos(
                id, full_name, name, owner_login,
                stargazers_count, forks_count, language
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            int(r["id"]),
            r.get("full_name"),
            r.get("name"),
            (r.get("owner") or {}).get("login"),
            int(r.get("stargazers_count") or 0),
            int(r.get("forks_count") or 0),
            r.get("language")
        ))


    set_meta(conn, "gh_page", page + 1)
    conn.commit()

    conn.close()

    print(f"Stored up to {per_page} repos. Next page = {page + 1}")



if __name__ == "__main__":
    fetch_and_store_repos(25)
