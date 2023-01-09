from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        i, j = 0, len(nums)-1
        while i <= j:
            half = (i+j)//2
            if nums[half] > target:
                j = half-1
            elif nums[half] < target:
                i = half+1
            else:
                return half
        return -1
