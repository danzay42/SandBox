import os
import sys
import psycopg

host = os.getenv("PGHOST", "db")
port = os.getenv("PGPORT", 5432)
dbname = os.getenv("POSTGRES_DB", "postgres")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "")
conninfo = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
print(f"{sys.argv=}")
print(f"{conninfo=}")

with psycopg.connect(conninfo) as conn:
    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        cur.execute("SELECT * FROM test")

        # print(cur.fetchall())
        
        cur.execute("DROP TABLE test")

        conn.commit()
