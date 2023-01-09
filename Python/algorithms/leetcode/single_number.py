from typing import List
from functools import reduce
from operator import xor

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # i = len(nums)-1
        # while i:
        #     try:
        #         r = nums.index(nums[i], 0, i)
        #         nums[r], nums[i-1] = nums[i-1], nums[r] 
        #         i -= 2
        #     except ValueError:
        #         break
        # return nums[i]
        return reduce(xor, nums)

if __name__ == "__main__":
    res = Solution().singleNumber([4,1,2,1,2])
    print(res)
