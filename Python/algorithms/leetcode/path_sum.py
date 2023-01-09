
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if root:
            new_sum = targetSum - root.val
            paths = self.pathSum(root.left, new_sum) + self.pathSum(root.right, new_sum)
            for p in paths:
                p.insert(0, root.val)
            if new_sum == 0 and not any((root.left, root.right)):
                return [[root.val]]
            else:
                return paths
        return []


# [5,4,8,11,null,13,4,7,2,null,null,5,1]
if __name__ == "__main__":
    res = Solution().pathSum(
            TreeNode(5, 
                     TreeNode(4,
                              TreeNode(11,
                                          TreeNode(7), TreeNode(2))), 
                     TreeNode(8,
                              TreeNode(13), TreeNode(4,
                                                     TreeNode(5), TreeNode(1))))
            , 22)
    # res = Solution().pathSum(TreeNode(1, TreeNode(2), TreeNode(3)), 1)
    print(res)
