from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        f,t = 0, len(nums)-1
        while f<=t:
            m = (f+t)//2
            if nums[m] == target:
                return m
            if target < nums[m]:
                if target < nums[t] < nums[m]:
                    f = m + 1
                else:
                    t = m - 1
            else:
                if target > nums[f] > nums[m]:
                    t = m - 1
                else:
                    f = m + 1
        return -1


if __name__ == "__main__":
    res = Solution().search([4,5,6,7,0,1,2], 0)
    print(res)
    res = Solution().search([1,3], 3)
    print(res)
    res = Solution().search([4,5,6,7,8,1,2,3], 8)
    print(res)
