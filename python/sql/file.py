import sqlite3
from pathlib import Path


def read_sql_query(sql_path: Path) -> str:
    return Path(sql_path).read_text()

number_of_customers = int(
    input("How many customers do you want to query? ")
)
con = sqlite3.connect("sample.db")
cur = con.cursor()
raw_sql = read_sql_query("query.sql") 

placeholders = {
    "limit": number_of_customers
}

for row in cur.execute(raw_sql, placeholders):
    print(row)