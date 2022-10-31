# def n(k):
#     return 3*k / sum(map(int, str(k))) ** 2
# ll = 1000
# a = set(range(1, ll))
# b = set(filter(lambda res: res%1 == 0, [n(k) for k in range(1, ll)]))
# print(min(a-b))

import sys
from collections import deque

class Point:
	x: int
	y: int
	to_root: int
	def __init__(self, row: str) -> None:
		self.x, self.y = map(int, row.split())
		self.to_root = -1
	def len_to(self, point):
		return abs(self.x - point.x) + abs(self.y - point.y)

_, *points, max_len, route = sys.stdin.readlines()
points = list(map(Point, points))
max_len = int(max_len)
root, dest = map(lambda x: points[int(x)-1], route.split())
points.remove(root)
root.to_root = 0

def bfs(points: list[Point], root: Point):
    queue = deque([root])
    while queue:
        root_point = queue.popleft()
        for p in points:
            if root_point.len_to(p) <= max_len:
                p.to_root = root_point.to_root+1
                if p == dest:
                    return
                points.remove(p)
                queue.append(p)

bfs(points, root)
print(dest.to_root)