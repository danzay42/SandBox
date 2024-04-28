package main

import (
	"slices"
)

func maxProfit(prices []int) int {
	res := 0
	m := prices[0]
	for _, p := range prices {
		switch {
		case p-m > res:
			res = p - m
		case p < m:
			m = p
		}
	}
	return res
}

func lengthOfLongestSubstringSlow(s string) int {
	res := 0
	mem := map[byte]int{}
	for i := 0; i < len(s); i++ {
		r := s[i]
		l, ok := mem[r]
		if !ok {
			mem[r] = i
			continue
		}
		res = max(res, len(mem))
		mem = map[byte]int{}
		i = l
	}
	return max(res, len(mem))
}

func lengthOfLongestSubstring(s string) int {
	res, left := 0, 0
	mem := map[rune]int{}
	for i, r := range s {
		l, ok := mem[r]
		if ok && l >= left {
			res = max(res, i-left)
			left = l + 1
		}
		mem[r] = i
	}
	return max(res, len(s)-left)
}

func characterReplacement(s string, k int) int {
	mem := map[byte]int{}
	winStart, mostFreqWinChar := 0, s[0]

	for i, r := range []byte(s) {
		mem[r]++
		if mem[r] > mem[mostFreqWinChar] {
			mostFreqWinChar = r
		}

		winLen := i - winStart + 1
		if winLen-mem[mostFreqWinChar] > k {
			mem[s[winStart]]--
			winStart++
		}
	}
	return len(s) - winStart
}

func checkInclusion(s1 string, s2 string) bool {
	if len(s1) > len(s2) {
		return false
	}

	search := [26]byte{}
	winLetters := [26]byte{}
	for i := range s1 {
		search[s1[i]-'a']++
		winLetters[s2[i]-'a']++
	}
	if winLetters == search {
		return true
	}

	for i, r := range s2[len(s1):] {
		winLetters[r-'a']++
		winLetters[s2[i]-'a']--
		if winLetters == search {
			return true
		}
	}
	return false
}

func minWindow(s string, t string) string {
	if len(t) > len(s) {
		return ""
	}
	//----------------------------
	search := ['z' - 'A' + 1]int{}
	for i := range t {
		search[t[i]-'A']++
	}
	//----------------------------
	winTo := 0
	window := ['z' - 'A' + 1]int{}
	count := len(t)
	for count != 0 && winTo < len(s) {
		ci := s[winTo] - 'A'
		window[ci]++
		if window[ci] == search[ci] {
			count -= search[ci]
		}
		winTo++
	}
	if count != 0 {
		return ""
	}
	//----------------------------
	winFrom := 0
	for winFrom < len(s) && window[s[winFrom]-'A'] > search[s[winFrom]-'A'] {
		window[s[winFrom]-'A']--
		winFrom++
	}
	//----------------------------
	minWinFrom, minWinTo := winFrom, winTo
	for ; winTo < len(s); winTo++ {
		ci := s[winTo] - 'A'
		window[ci]++
		if search[ci] == 0 {
			continue
		}

		for window[s[winFrom]-'A'] > search[s[winFrom]-'A'] {
			window[s[winFrom]-'A']--
			winFrom++
		}

		if winTo-winFrom < minWinTo-minWinFrom {
			minWinTo = winTo + 1
			minWinFrom = winFrom
		}
	}
	return s[minWinFrom:minWinTo]
}

type SortedStack struct {
	s []int
}

func (d *SortedStack) Insert(v int) {
	i, _ := slices.BinarySearch(d.s, v)
	d.s = slices.Insert(d.s, i, v)
}

func (d *SortedStack) Remove(v int) {
	i, _ := slices.BinarySearch(d.s, v)
	d.s = append(d.s[:i], d.s[i+1:]...)
}

func (d *SortedStack) Top() int {
	return d.s[len(d.s)-1]
}

func maxSlidingWindowSlow(nums []int, k int) []int {
	result := make([]int, len(nums)-k+1)
	deque := SortedStack{s: make([]int, 0, k)}

	for _, n := range nums[:k] {
		deque.Insert(n)
	}
	result[0] = deque.Top()

	for i, n := range nums[k:] {
		deque.Insert(n)
		deque.Remove(nums[i])
		result[i+1] = deque.Top()
	}
	return result
}

type Deque struct {
	nums       []int
	indexStack []int
}

func (d *Deque) PushRight(numsIndex int) {
	i := len(d.indexStack) - 1
	for i >= 0 && d.nums[numsIndex] >= d.nums[d.indexStack[i]] {
		i--
	}
	d.indexStack = append(d.indexStack[:i+1], numsIndex)
}

func (d *Deque) PopLeft(numsIndex int) {
	if numsIndex == d.indexStack[0] {
		d.indexStack = d.indexStack[1:]
	}
}

func (d *Deque) Left() int {
	return d.nums[d.indexStack[0]]
}

func maxSlidingWindowObject(nums []int, k int) []int {
	result := make([]int, 0, len(nums)-k+1)
	deque := Deque{nums: nums, indexStack: make([]int, 0, len(nums))}

	for i := range nums {
		deque.PushRight(i)
		deque.PopLeft(i - k)
		if i >= k-1 {
			result = append(result, deque.Left())
		}
	}
	return result
}

func maxSlidingWindow(nums []int, k int) []int {
	result := make([]int, 0, len(nums)-k+1)
	deque := make([]int, 0, len(nums))

	for i, num := range nums {
		for len(deque) > 0 && num >= nums[deque[len(deque)-1]] {
			deque = deque[:len(deque)-1]
		}
		deque = append(deque, i)

		if i-k == deque[0] {
			deque = deque[1:]
		}

		if i >= k-1 {
			result = append(result, nums[deque[0]])
		}
	}
	return result
}
