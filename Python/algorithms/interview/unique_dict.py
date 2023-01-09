def made_unique(data: list[dict]):
    res = dict()
    for d in data:
        res[str(d)] = d
    return list(res.values())

def make_unique(data: list[dict]):
    return {str(d): d for d in data}.values()

if __name__ == "__main__":
    d = [{"key1": "value1"}, {"k1": "v1", "k2": "v2", "k3": "v3"}, {}, {}, {"key1": "value1"}, {"key1": "value1"}, {"key2": "value2"}]
    res = made_unique(d)
    res = make_unique(d)
    print(res)
