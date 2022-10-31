
import random
O = 0


def merge_sort(data: list[int]) -> list[int]:
    """
    O(n*log2(n))
    """
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2

    data_left = merge_sort(data[:mid])
    data_right = merge_sort(data[mid:])
    return merge(data_left, data_right)


def merge_v1(data_l: list[int], data_r: list[int]):
    """
    O(n)
    """
    global O
    sorted_data = []
    l = r = 0

    while l < len(data_l) and r < len(data_r):
        O += 1
        if data_l[l] < data_r[r]:
            sorted_data.append(data_l[l])
            l += 1
        else:
            sorted_data.append(data_r[r])
            r += 1
    else:
        sorted_data.extend(data_l[l:] or data_r[r:])
    
    return sorted_data


def merge_v2(data_l: list[int], data_r: list[int]):
    """
    O(n)
    """
    global O
    sorted_data = []
    while data_l and data_r:
        O += 1
        if data_l[0] < data_r[0]:
            sorted_data.append(data_l.pop(0))
        else:
            sorted_data.append(data_r.pop(0))
    else:
        sorted_data.extend(data_l or data_r)
    return sorted_data


merge = merge_v2
n = 10000
test_data = random.sample(range(n), n)
# assert sorted(test_data) == merge_sort(test_data) 
merge_sort(test_data)
print(f"{O=}, {n=}")
