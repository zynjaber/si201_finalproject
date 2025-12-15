import csv
import os
import sqlite3
import matplotlib.pyplot as plt
from db import DB_PATH


OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)


def pokemon_avg_height_by_type(conn):

    rows = conn.execute("""
        SELECT pt.type_name, AVG(p.height) AS avg_height, COUNT(*) as n
        FROM pokemon p
        JOIN pokemon_types pt ON p.id = pt.pokemon_id
        GROUP BY pt.type_name
        HAVING n >= 5
        ORDER BY avg_height DESC;
    """).fetchall()

    return rows

def github_avg_stars_by_language(conn):

    rows = conn.execute("""
        SELECT COALESCE(language, 'Unknown') AS language,
               AVG(stargazers_count) AS avg_stars,
               COUNT(*) as n
        FROM github_repos
        GROUP BY COALESCE(language, 'Unknown')
        HAVING n >= 3
        ORDER BY avg_stars DESC;
    """).fetchall()

    return rows

def write_csv(path, header, rows):

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def bar_chart(categories, values, title, xlabel, ylabel, outpath):

    plt.figure()
    plt.bar(categories, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def main():

    conn = sqlite3.connect(DB_PATH)

    poke_rows = pokemon_avg_height_by_type(conn)
    gh_rows = github_avg_stars_by_language(conn)


    write_csv(f"{OUT_DIR}/pokemon_avg_height_by_type.csv",
              ["type_name", "avg_height", "count"], poke_rows)
    write_csv(f"{OUT_DIR}/github_avg_stars_by_language.csv",
              ["language", "avg_stars", "count"], gh_rows)
    

    top = poke_rows[:10]

    bar_chart([r[0] for r in top], [r[1] for r in top],
              "Avg Pokémon Height by Type (Top 10)",
              "Type", "Average Height",
              f"{OUT_DIR}/viz_pokemon_avg_height_by_type.png")


    top2 = gh_rows[:10]

    bar_chart([r[0] for r in top2], [r[1] for r in top2],
              "Avg GitHub Repo Stars by Language (Top 10)",
              "Language", "Average Stars",
              f"{OUT_DIR}/viz_github_avg_stars_by_language.png")

    conn.close()

    print("Wrote CSV outputs + saved 2 visualizations.")


if __name__ == "__main__":
    main()
