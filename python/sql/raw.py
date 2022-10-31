import sqlite3

number_of_customers = int(
    input("How many customers do you want to query? ")
)
con = sqlite3.connect("sample.db")
cur = con.cursor()

raw_sql = """
SELECT
    c.id,
    c.first_name,
    SUM(i.total) as total
FROM Invoice i
LEFT JOIN Customer c ON i.customer_id = c.id
GROUP BY c.id, c.first_name
ORDER BY total DESC
LIMIT ?;
"""

for row in cur.execute(raw_sql, (number_of_customers, )):
    print(row)