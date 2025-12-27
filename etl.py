import csv
import psycopg2
import os

CSV_FILE = "data/items.csv"

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )

def run_etl():
    conn = get_db_connection()
    cur = conn.cursor()

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        inserted = 0

        for row in reader:
            cur.execute(
                """
                INSERT INTO items (name, price)
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM items WHERE name = %s
                );
                """,
                (row["name"], row["price"], row["name"])
            )
            if cur.rowcount > 0:
                inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"ETL completed. Inserted {inserted} new records.")

if __name__ == "__main__":
    run_etl()
