package main

import (
	"fmt"
)

type ListNode struct {
	Val  int
	Next *ListNode
}

func (l *ListNode) String() string {
	return fmt.Sprint(l.Val, "->", l.Next)
}

func reverseList(head *ListNode) *ListNode {
	var prev *ListNode
	for head != nil {
		next := head.Next
		head.Next = prev
		prev = head
		head = next
	}
	return prev
}

func reorderList(head *ListNode) {
	// create head half and reversed
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
	}

	reversed := reverseList(slow.Next)
	slow.Next = nil
	// shuffle head and reversed
	for head != nil && reversed != nil {
		nextHead := head.Next
		nextReversed := reversed.Next
		head.Next = reversed
		reversed.Next = nextHead
		head = nextHead
		reversed = nextReversed
	}
}

func removeNthFromEnd(head *ListNode, n int) *ListNode {
	slow, fast := head, head
	for ; n > 0; n-- {
		fast = fast.Next
	}

	if fast == nil {
		return slow.Next
	}

	for fast.Next != nil {
		slow = slow.Next
		fast = fast.Next
	}

	slow.Next = slow.Next.Next
	return head
}

type Node struct {
	Val    int
	Next   *Node
	Random *Node
}

func (l *Node) String() string {
	return fmt.Sprint(l.Val, "->", l.Next)
}

func copyRandomList(head *Node) *Node {
	if head == nil {
		return nil
	}

	// Create copyNodes
	tmp := head
	for tmp != nil {
		node := &Node{Val: tmp.Val, Next: tmp.Next}
		tmp.Next = node
		tmp = node.Next
	}

	// Update copyNodes random
	tmp = head
	for tmp != nil {
		if tmp.Random != nil {
			tmp.Next.Random = tmp.Random.Next
		}
		tmp = tmp.Next.Next
	}

	// Update copyNodes next
	result := head.Next
	tmp = head
	for tmp.Next.Next != nil {
		copyNode := tmp.Next
		nextOrig := copyNode.Next
		copyNode.Next = nextOrig.Next

		tmp.Next = nextOrig
		tmp = nextOrig
	}
	tmp.Next = nil

	return result
}

func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
	result := l1
	mem := 0
	for l2 != nil || mem > 0 {
		if l2 == nil {
			l2 = &ListNode{Val: 0}
		}
		s := l1.Val + l2.Val + mem
		l1.Val, mem = s%10, s/10
		if l1.Next == nil && (l2.Next != nil || mem > 0) {
			l1.Next = &ListNode{Val: 0}
		}
		l1 = l1.Next
		l2 = l2.Next
	}

	return result
}

func hasCycle(head *ListNode) bool {
	fast := head
	for fast != nil && fast.Next != nil {
		head = head.Next
		fast = fast.Next.Next
		if head == fast {
			return true
		}
	}
	return false
}

func findDuplicateWithMem(nums []int) int {
	seen := map[int]bool{}
	for _, num := range nums {
		if seen[num] {
			return num
		}
		seen[num] = true
	}
	return 0
}

func findDuplicate(nums []int) int {
	slow, fast := nums[0], nums[nums[0]]
	for slow != fast {
		slow = nums[slow]
		fast = nums[nums[fast]]
	}

	slow = 0
	for slow != fast {
		slow = nums[slow]
		fast = nums[fast]
	}
	return slow
}

type DoubleLinkedNode struct {
	key   int
	value int
	prev  *DoubleLinkedNode
	next  *DoubleLinkedNode
}

func (l *DoubleLinkedNode) String() string {
	return fmt.Sprint(l.value, "<->", l.next)
}

type LRUCache struct {
	s   map[int]*DoubleLinkedNode
	cap int
	top *DoubleLinkedNode
	bot *DoubleLinkedNode
}

func NewLRUCache(capacity int) LRUCache {
	return LRUCache{
		s:   make(map[int]*DoubleLinkedNode, capacity),
		cap: capacity,
	}
}

func (l *LRUCache) Get(key int) int {
	node, ok := l.s[key]
	if !ok {
		return -1
	}
	l.updateNodePosition(node)
	return node.value
}

func (l *LRUCache) Put(key int, value int) {
	node, ok := l.s[key]
	if !ok {
		l.insertNode(key, value)
		return
	}
	node.value = value
	l.updateNodePosition(node)
}

func (l *LRUCache) updateNodePosition(node *DoubleLinkedNode) {
	if node == l.top {
		return
	}
	if node == l.bot {
		node.next.prev = nil
		l.bot = node.next
	} else {
		node.next.prev = node.prev
		node.prev.next = node.next
	}
	node.next = nil
	node.prev = l.top
	l.top.next = node
	l.top = node
}

func (l *LRUCache) insertNode(key int, value int) {
	node := &DoubleLinkedNode{
		key:   key,
		value: value,
		prev:  l.top,
	}
	if len(l.s) == 0 {
		l.bot = node
	} else {
		l.top.next = node
	}
	l.s[key] = node
	l.top = node

	if len(l.s) > l.cap {
		delete(l.s, l.bot.key)
		l.bot = l.bot.next
		l.bot.prev = nil
	}
}

func mergeTwoLists(list1 *ListNode, list2 *ListNode) *ListNode {
	if list1 == nil {
		return list2
	}
	if list2 == nil {
		return list1
	}

	tmp := &ListNode{}
	result := tmp

	for list1 != nil && list2 != nil {
		if list1.Val < list2.Val {
			tmp.Next = list1
			list1 = list1.Next
		} else {
			tmp.Next = list2
			list2 = list2.Next
		}
		tmp = tmp.Next
	}

	if list1 != nil {
		tmp.Next = list1
	}
	if list2 != nil {
		tmp.Next = list2
	}

	return result.Next
}

func mergeKLists(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}
	result := lists[0]

	for _, list := range lists[1:] {
		result = mergeTwoLists(result, list)
	}

	return result
}

func mergeKListsFaster(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}

	for i := 1; i < len(lists); i *= 2 {
		for j := 0; j < len(lists)-i; j += 2 * i {
			lists[j] = mergeTwoLists(lists[j], lists[j+i])
		}
	}

	return lists[0]
}

func reverseListUntilNode(head *ListNode, target *ListNode) *ListNode {
	var prev *ListNode
	for head != nil {
		next := head.Next
		head.Next = prev
		prev = head
		head = next
	}
	return prev
}

func reverseKGroup(head *ListNode, k int) *ListNode {
	result := &ListNode{Next: head}

	groupPrev := result
	var kth *ListNode
	for {
		kth = groupPrev
		for i := 0; i < k && kth != nil; i++ {
			kth = kth.Next
		}
		if kth == nil {
			break
		}
		groupNext := kth.Next

		prev, curr := groupNext, groupPrev.Next
		for curr != groupNext {
			next := curr.Next
			curr.Next = prev
			prev = curr
			curr = next
		}

		tmp := groupPrev.Next
		groupPrev.Next = kth
		groupPrev = tmp
	}

	return result.Next
}
