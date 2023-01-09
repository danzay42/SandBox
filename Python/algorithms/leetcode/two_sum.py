from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pair = dict()
        for i, num in enumerate(nums):
            if p:= pair.get(num) is None:
                return [i, int(p)]
            else:
                pair[target - num] = i
            print(pair)
        return []

if __name__ == "__main__":
    print(Solution().twoSum([2,7,11,15], 9))
