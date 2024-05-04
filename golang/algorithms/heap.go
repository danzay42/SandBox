package main

import (
	"container/heap"
	"slices"
)

/**
 * Your KthLargest object will be instantiated and called as such:
 * obj := Constructor(k, nums);
 * param_1 := obj.Add(val);
 */

type KthLargest1 struct {
	queue []int
	k     int
}

func newKthLargest1(k int, nums []int) *KthLargest1 {
	kQueue := &KthLargest1{k: k}
	for _, n := range nums {
		kQueue.Add(n)
	}
	return kQueue
}

func (q *KthLargest1) Add(val int) int {
	i, _ := slices.BinarySearch(q.queue, val)
	q.queue = slices.Insert(q.queue, i, val)
	if len(q.queue) > q.k {
		q.queue = q.queue[1:]
	}
	return q.queue[0]
}

// ------------------------------------------------

func (q *KthLargest2) Len() int {
	return len(q.heap)
}

func (q *KthLargest2) Less(i, j int) bool {
	return q.heap[i] < q.heap[j]
}

func (q *KthLargest2) Swap(i, j int) {
	q.heap[i], q.heap[j] = q.heap[j], q.heap[i]
}

func (q *KthLargest2) Push(x any) {
	q.heap = append(q.heap, x.(int))
}

func (q *KthLargest2) Pop() (val any) {
	val = q.heap[q.Len()-1]
	q.heap = q.heap[:q.Len()-1]
	return
}

type KthLargest2 struct {
	heap []int
	size int
}

func newKthLargest2(k int, nums []int) KthLargest2 {
	kQueue := KthLargest2{size: k}
	heap.Init(&kQueue)
	for _, n := range nums {
		kQueue.Add(n)
	}
	return kQueue
}

func (q *KthLargest2) Add(val int) int {
	heap.Push(q, val)
	if q.Len() > q.size {
		heap.Pop(q)
	}
	return q.heap[0]
}

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

type IntHeapMax []int

func (h IntHeapMax) Len() int           { return len(h) }
func (h IntHeapMax) Less(i, j int) bool { return h[i] > h[j] }
func (h IntHeapMax) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *IntHeapMax) Push(x any)        { *h = append(*h, x.(int)) }
func (h *IntHeapMax) Pop() any {
	x := (*h)[len(*h)-1]
	*h = (*h)[:len(*h)-1]
	return x
}

func lastStoneWeight(stones []int) int {
	h := IntHeapMax(stones)
	heap.Init(&h)

	for h.Len() > 1 {
		r1 := heap.Pop(&h).(int)
		r2 := heap.Pop(&h).(int)
		if r1 != r2 {
			heap.Push(&h, r1-r2)
		}
	}
	if h.Len() == 0 {
		return 0
	}
	return h[0]
}

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

type PointHeap [][]int

func (h PointHeap) Len() int { return len(h) }
func (h PointHeap) Less(i, j int) bool {
	return distToZero(h[i]) > distToZero(h[j])
}
func (h PointHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *PointHeap) Push(x any)   { *h = append(*h, x.([]int)) }
func (h *PointHeap) Pop() any {
	x := (*h)[len(*h)-1]
	*h = (*h)[:len(*h)-1]
	return x
}

func (h PointHeap) Max() int {
	return distToZero(h[0])
}

func distToZero(p []int) int {
	return p[0]*p[0] + p[1]*p[1]
}

func kClosest(points [][]int, k int) [][]int {
	h := PointHeap(points[:k])
	heap.Init(&h)
	for _, p := range points[k:] {
		if distToZero(p) >= h.Max() {
			continue
		}
		heap.Pop(&h)
		heap.Push(&h, p)
	}

	return h
}

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

type IntHeapMin []int

func (h IntHeapMin) Len() int           { return len(h) }
func (h IntHeapMin) Less(i, j int) bool { return h[i] < h[j] }
func (h IntHeapMin) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *IntHeapMin) Push(x any)        { *h = append(*h, x.(int)) }
func (h *IntHeapMin) Pop() any {
	x := (*h)[len(*h)-1]
	*h = (*h)[:len(*h)-1]
	return x
}

func findKthLargest(nums []int, k int) int {
	h := IntHeapMin(nums[:k])
	heap.Init(&h)

	for _, n := range nums[k:] {
		if n < h[0] {
			continue
		}
		heap.Pop(&h)
		heap.Push(&h, n)
	}

	return h[0]
}

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

func leastInterval(tasks []byte, n int) int {
	freq := [26]int{}
	maxFreq := 0
	for _, t := range tasks {
		freq[t-'A']++
		maxFreq = max(maxFreq, freq[t-'A'])
	}

	res := (maxFreq - 1) * (n + 1)
	for _, f := range freq {
		if f == maxFreq {
			res++
		}
	}

	return max(len(tasks), res)
}

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

/**
 * Your TwitterSimple object will be instantiated and called as such:
 * obj := Constructor();
 * obj.PostTweet(userId,tweetId);
 * param_2 := obj.GetNewsFeed(userId);
 * obj.Follow(followerId,followeeId);
 * obj.Unfollow(followerId,followeeId);
 */

type User1 struct {
	id     int
	follow map[int]*User1
}

type Tweet1 struct {
	id     int
	userId int
}

type TwitterSimple struct {
	users    map[int]*User1
	tweets   []*Tweet1
	feedSize int
}

func newSimpleTwitter() *TwitterSimple {
	return &TwitterSimple{users: make(map[int]*User1), feedSize: 10}
}

func (t *TwitterSimple) addUser(id int) *User1 {
	if t.users[id] == nil {
		t.users[id] = &User1{id: id, follow: make(map[int]*User1)}
	}
	return t.users[id]
}

func (t *TwitterSimple) PostTweet(userId int, tweetId int) {
	t.addUser(userId)
	tweet := &Tweet1{id: tweetId, userId: userId}
	t.tweets = append(t.tweets, tweet)
}

func (t *TwitterSimple) GetNewsFeed(userId int) []int {
	results := make([]int, 0, t.feedSize)
	user := t.users[userId]
	for i := len(t.tweets) - 1; i >= 0 && len(results) < t.feedSize; i-- {
		owner := t.tweets[i].userId
		if userId != owner && user.follow[owner] == nil {
			continue
		}
		results = append(results, t.tweets[i].id)
	}
	return results
}

func (t *TwitterSimple) Follow(followerId int, followeeId int) {
	follower := t.addUser(followerId)
	followee := t.addUser(followeeId)
	follower.follow[followeeId] = followee
}

func (t *TwitterSimple) Unfollow(followerId int, followeeId int) {
	if t.users[followerId] != nil {
		delete(t.users[followerId].follow, followeeId)
	}
}

// ------------------------------------------------

type User struct {
	id     int
	follow map[int]*User
	tweets []*Tweet
}

type Tweet struct {
	id        int
	timestamp int
}

type TweetHeapOldest []*Tweet

func (h TweetHeapOldest) Len() int           { return len(h) }
func (h TweetHeapOldest) Less(i, j int) bool { return h[i].timestamp < h[j].timestamp }
func (h TweetHeapOldest) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *TweetHeapOldest) Push(x any)        { *h = append(*h, x.(*Tweet)) }
func (h *TweetHeapOldest) Pop() any          { x := (*h)[len(*h)-1]; *h = (*h)[:len(*h)-1]; return x }
func (h TweetHeapOldest) Oldest() int        { return h[0].timestamp }

type TwitterHeap struct {
	users    map[int]*User
	feedSize int
	time     int
}

func newTwitterHeap() *TwitterHeap {
	return &TwitterHeap{users: make(map[int]*User), feedSize: 10}
}

func (t *TwitterHeap) addUser(id int) *User {
	if t.users[id] == nil {
		t.users[id] = &User{id: id, follow: make(map[int]*User)}
	}
	return t.users[id]
}

func (t *TwitterHeap) PostTweet(userId int, tweetId int) {
	user := t.addUser(userId)
	tweet := &Tweet{id: tweetId, timestamp: t.time}
	user.tweets = append(user.tweets, tweet)
	t.time++
}

func (t *TwitterHeap) GetNewsFeed(userId int) []int {
	user := t.users[userId]
	if user == nil {
		return nil
	}
	h := &TweetHeapOldest{}
	from := max(0, len(user.tweets)-t.feedSize)
	for _, tweet := range user.tweets[from:] {
		heap.Push(h, tweet)
	}

	for _, u := range user.follow {
		for i := len(u.tweets) - 1; i >= 0; i-- {
			tweet := u.tweets[i]
			if h.Len() < t.feedSize {
				heap.Push(h, tweet)
				continue
			}
			if tweet.timestamp < h.Oldest() {
				break
			}
			heap.Pop(h)
			heap.Push(h, tweet)
		}
	}
	feed := make([]int, h.Len())
	for i := range feed {
		feed[len(feed)-1-i] = heap.Pop(h).(*Tweet).id
	}
	return feed
}

func (t *TwitterHeap) Follow(followerId int, followeeId int) {
	follower := t.addUser(followerId)
	followee := t.addUser(followeeId)
	follower.follow[followeeId] = followee
}

func (t *TwitterHeap) Unfollow(followerId int, followeeId int) {
	if t.users[followerId] != nil {
		delete(t.users[followerId].follow, followeeId)
	}
}

// ------------------------------------------------
// ------------------------------------------------
// ------------------------------------------------

/**
 * Your MedianFinder object will be instantiated and called as such:
 * obj := Constructor();
 * obj.AddNum(num);
 * param_2 := obj.FindMedian();
 */

type MedianFinderSlow struct {
	data []int
}

func newSlowMF() *MedianFinderSlow {
	return &MedianFinderSlow{}
}

func (m *MedianFinderSlow) AddNum(num int) {
	i, _ := slices.BinarySearch(m.data, num)
	m.data = slices.Insert(m.data, i, num)
}

func (m *MedianFinderSlow) FindMedian() float64 {
	i, odd := len(m.data)/2, len(m.data)%2 == 1
	if odd {
		return float64(m.data[i])
	}
	return float64(m.data[i-1]+m.data[i]) / 2
}

// ------------------------------------------------

type IntHeapB []int

func (h IntHeapB) Len() int      { return len(h) }
func (h IntHeapB) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *IntHeapB) Push(x any)   { *h = append(*h, x.(int)) }
func (h *IntHeapB) Pop() any     { x := (*h)[len(*h)-1]; *h = (*h)[:len(*h)-1]; return x }
func (h IntHeapB) Top() int      { return h[0] }

type IntHeapBMax struct{ IntHeapB }

func (h IntHeapBMax) Less(i, j int) bool { return h.IntHeapB[i] > h.IntHeapB[j] }

type IntHeapBMin struct{ IntHeapB }

func (h IntHeapBMin) Less(i, j int) bool { return h.IntHeapB[i] < h.IntHeapB[j] }

type MedianFinder struct {
	left  *IntHeapBMax
	right *IntHeapBMin
}

func newMedianFinder() *MedianFinder {
	return &MedianFinder{
		left:  new(IntHeapBMax),
		right: new(IntHeapBMin),
	}
}

func (m *MedianFinder) AddNum(num int) {
	var dst, src heap.Interface = m.left, m.right
	if m.right.Len() > 0 && num > m.right.Top() {
		dst, src = m.right, m.left
	}
	heap.Push(dst, num)
	if dst.Len() > src.Len()+1 {
		heap.Push(src, heap.Pop(dst))
	}
}

func (m *MedianFinder) FindMedian() float64 {
	if m.left.Len() == m.right.Len() {
		return float64(m.left.Top()+m.right.Top()) / 2
	}
	if m.left.Len() > m.right.Len() {
		return float64(m.left.Top())
	}
	return float64(m.right.Top())
}
