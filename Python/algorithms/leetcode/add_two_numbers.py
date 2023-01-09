from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"{self.val}->{str(self.next)}"

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        head = point = ListNode()
        while l1 or l2:
            if l1:
                point.val += l1.val
                l1 = l1.next
            if l2:
                point.val += l2.val
                l2 = l2.next
            if l1 or l2 or point.val > 9:
                point.next = ListNode(point.val // 10)
            point.val = point.val % 10
            point = point.next
        return head
 

if __name__ == "__main__":
    res = Solution().addTwoNumbers(
            ListNode(2, ListNode(4, ListNode(3))),
            ListNode(5, ListNode(6, ListNode(4)))
            )
    print(res)
