from typing import Optional, List

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle1(self, head: Optional[ListNode]) -> bool:
        nodes = dict()
        while head:
            if nodes.get(head):
                return True
            else:
                nodes[head] = True
                head = head.next
        return False

    def hasCycle2(self, head: Optional[ListNode]) -> bool:
        while head:
            if getattr(head, "ab", None):
                return True
            else:
                setattr(head, "ab", True)
                head = head.next
        return False
    
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        try:
            fast_head = head.next
            while head != fast_head:
                head = head.next
                fast_head = fast_head.next.next
            return True
        except AttributeError:
            return False
