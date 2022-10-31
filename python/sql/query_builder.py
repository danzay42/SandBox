import sqlite3
from pypika import Order, Query, Table, functions


number_of_customers = int(
    input("How many customers do you want to query? ")
)

invoice = Table("Invoice")
customer = Table("Customer")
query = (
    Query.from_(invoice)
    .left_join(customer)
    .on(invoice.customer_id == customer.id)
    .groupby(customer.id, customer.first_name)
    .orderby(functions.Sum(invoice.total), order=Order.desc)
    .limit(number_of_customers)
    .select(
        customer.id,
        customer.first_name,
        functions.Sum(invoice.total).as_("total"),
    )
)


con = sqlite3.connect("sample.db")
cur = con.cursor()
for row in cur.execute(query):
    print(row)