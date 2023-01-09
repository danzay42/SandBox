# import sys

# #j, s = map(str.strip, sys.stdin.readlines(3))
# j = sys.stdin.readline().strip()
# s = sys.stdin.readline().strip()

# def rocks_and_jewelry(j, s):
# 	res = 0	
# 	for c in set(j):
# 		res += s.count(c)
# 	return res
# print(rocks_and_jewelry(j, s))

# ---------------------------------------------
# import sys

# size = int(sys.stdin.readline()) + 1

# res = 0
# current = 0

# while size := size - 1:
# 	if int(sys.stdin.readline()) == 1:
# 		current += 1
# 		res = max(res, current)
# 	else:
# 		current = 0

# print(res)

# # ---------------------------------------------
# import sys

# size = int(sys.stdin.readline()) + 1
# last = -sys.maxsize - 1

# while size := size - 1:
# 	current = int(sys.stdin.readline())
# 	if current > last:
# 		last = current
# 		print(last)
# 
# # ---------------------------------------------
# import sys

# def counter(s: str) -> dict:
# 	res = dict()
# 	for ch in s:
# 		if ch in res:
# 			res[ch] += 1
# 		else:
# 			res[ch] = 1
# 	return res

# s1 = sys.stdin.readline().strip()
# s2 = sys.stdin.readline().strip()

# print(int(counter(s1)==counter(s2)))

#------------------------------------------
# def gen(br, bo=0, bc=0, res=""):
# 	if bo == bc == br:
# 		print(res)
# 		return
	
# 	if bo <= br:
# 		gen(br, bo+1, bc, res+"(")		
# 	if bc <= br and bc < bo:
# 		gen(br, bo, bc+1, res+")")
	
# gen(int(input()))

# # -----------------------------------------
# import sys
# from dataclasses import dataclass 
# from collections import deque

# # @dataclass
# class Point:
# 	x: int
# 	y: int
# 	to_root: int

# 	def __init__(self, row: str) -> None:
# 		self.x, self.y = map(int, row.split())
# 		self.to_root = -1

# 	def len_to(self, point):
# 		return abs(self.x - point.x) + abs(self.y - point.y)

# 	def __repr__(self) -> str:
# 		return f"({self.x},{self.y})"

# _, *points, max_len, route = sys.stdin.readlines()
# points = list(map(Point, points))
# max_len = int(max_len)
# root, dest = map(lambda x: points[int(x)-1], route.split())


# def route(root: Point, passed=0):
# 	if root.len_to(dest) <= max_len:
# 		return passed + 1
	
# 	neighbors: list[Point] = [points.pop(i) for i, p in enumerate(points) if root.len_to(p) <= max_len]
# 	if not neighbors:
# 		return -1
	
# 	routes = [route(p_root, passed+1) for p_root in neighbors]
# 	print(routes)
# 	return min(filter(lambda r: r>=0, routes))

# points.remove(root)
# print(route(root))
# # print(points)


# -----------------------------------------
import sys
from dataclasses import dataclass 
from collections import deque

# @dataclass
class Point:
	x: int
	y: int
	to_root: int

	def __init__(self, row: str) -> None:
		self.x, self.y = map(int, row.split())
		self.to_root = -1

	def len_to(self, point):
		return abs(self.x - point.x) + abs(self.y - point.y)

	def __repr__(self) -> str:
		return f"({self.x},{self.y},{self.to_root})"

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

# def route(root: Point, passed=0):
# 	if root.len_to(dest) <= max_len:
# 		return passed + 1
	
# 	neighbors: list[Point] = [points.pop(i) for i, p in enumerate(points) if root.len_to(p) <= max_len]
# 	if not neighbors:
# 		return -1
	
# 	routes = [route(p_root, passed+1) for p_root in neighbors]
# 	print(routes)
# 	return min(filter(lambda r: r>=0, routes))

# points.remove(root)
# print(route(root))

