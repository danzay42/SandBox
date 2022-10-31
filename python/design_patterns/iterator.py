class ListNode:
    def __init__(self, val=0, next=None) -> None:
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self, head) -> None:
        self.head = head
        self.cur = None
    def __iter__(self):
        self.cur = self.head
        return self
    def __next__(self):
        if self.cur:
            val = self.cur.val
            self.cur = self.cur.next
            return val
        else:
            raise StopIteration

my_list = LinkedList(
    ListNode(1,
        ListNode(2, 
            ListNode(3)))
)

for n in my_list:
    print(n)