
from typing import List

class Solution:
    def twoSums(self, nums: List[int], target: int) -> List[List[int]]:
        s = set()
        res = []
        for num in nums:
            if target-num in s and (not res or num != res[-1][0]):
                # print(target, num, res, res[-1][1] if res else None)
                res.append([num, target-num])
            s.add(num)
        # print(f"{res=}")
        return res
    def kSums(self, nums: List[int], target: int, k=2) -> List[List[int]]:
        if k == 2:
            return self.twoSums(nums, target)
        res = []
        for i in range(len(nums)):
            if i == 0 or nums[i-1] != nums[i]:
                sub_res = self.kSums(nums[i+1:], target-nums[i], k-1)
                res += map(lambda sr: [nums[i]]+sr, sub_res)
        return res
        
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        return self.kSums(nums, target, 4)

if __name__ == "__main__":
    print(Solution().twoSums([2,2,2], 4))
    print(Solution().twoSums([2,7,11,15], 9))
    print(Solution().twoSums([3,3], 6))
    print(Solution().fourSum([-2,-1,-1,1,1,2,2], 0))

