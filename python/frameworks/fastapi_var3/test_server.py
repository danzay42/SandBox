import requests
addr = "http://127.0.0.1:8000/"

print("======================REQUEST TEST==========================")
print(requests.get(addr).json(), end="\n" + "="*60 + "\n")
print(requests.get(f"{addr}items/0").json(), end="\n" + "="*60 + "\n")
print(requests.get(f"{addr}items/10").json(), end="\n" + "="*60 + "\n")
print(requests.get(f"{addr}items/slkdf").json(), end="\n" + "="*60 + "\n")
print(requests.get(f"{addr}items?name=Nails").json(), end="\n" + "="*60 + "\n")

print("======================REQUEST TEST 2==========================")
print("Adding an item:")
print(
    requests.post(
    addr,
    json={"name": "sqrewdriver", "price": 3.99, "count": 10, "id": 4, "category": "tools"}
    ).json()
)
print(requests.get(addr).json())
print()

print("Updating an item:")
print(requests.put(f"{addr}items/0?count=9001").json())
print(requests.get(addr).json())
print()

print("Deleteng an item:")
print(requests.delete(f"{addr}items/0").json())
print(requests.get(addr).json())
print()

