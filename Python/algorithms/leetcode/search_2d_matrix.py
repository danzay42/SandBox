from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])
        f, t = 0, rows*cols-1
        while f <= t:
            m = (f+t)//2
            num = matrix[m//cols][m%cols]
            if num == target:
                return True
            elif target < num:
                t = m - 1
            else:
                f = m + 1
        return False
