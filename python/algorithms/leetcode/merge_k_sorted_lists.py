from typing import Optional, List

class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next

            
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        head = point = ListNode(0)
        while list1 and list2:
            if list1.val <= list2.val:
                point.next = list1
                list1 = list1.next
            else:
                point.next = list2
                list2 = list2.next
            point = point.next
        point.next = list1 or list2
        return head.next
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        lc = len(lists)
        interval = 1
        while interval < lc:
            for i in range(0, lc - interval, interval * 2):
                lists[i] = self.mergeTwoLists(lists[i], lists[i+interval])
            interval *= 2
        return lists[0] if lc > 0 else None

