from typing import Optional, List
from itertools import permutations, combinations
from functools import lru_cache, cache
from math import factorial
  
class Solution:
    def numTrees(self, n: int) -> int:
        sol = 1
        for i in range (n):
            sol *= 2 * (2 * i + 1) / (i + 2)
        return int(sol)


c = Solution()
print(c.numTrees(1), 1)
print(c.numTrees(2), 2)
print(c.numTrees(3), 5)
print(c.numTrees(4), 14)
print(c.numTrees(5), 42)
print(c.numTrees(6), 132)
print(c.numTrees(7), 429)
print(c.numTrees(8), 1430)