package main

import (
	"slices"
)

func search(nums []int, target int) int {
	i, found := slices.BinarySearch(nums, target)
	if found {
		return i
	}
	return -1
}

func searchMatrix(matrix [][]int, target int) bool {
	i, found := slices.BinarySearchFunc(matrix, target, func(ints []int, i int) int {
		if ints[0] == i {
			return 0
		}
		if ints[0] < i {
			return -1
		}
		return 1
	})
	if found || len(matrix[0]) == 1 {
		return found
	}
	if i == 0 {
		i++
	}

	_, found = slices.BinarySearch(matrix[i-1], target)
	return found
}

func searchMatrix2(matrix [][]int, target int) bool {
	rows := len(matrix)
	cols := len(matrix[0])
	size := rows * cols
	left := -1
	right := size
	for right-left > 1 {
		mid := (right + left) >> 1
		if matrix[mid/cols][mid%cols] < target {
			left = mid
		} else {
			right = mid
		}
	}
	return right < size && matrix[right/cols][right%cols] == target
}

func canEat(piles []int, timeLimit, speed int) bool {
	timeNeed := 0
	for _, banana := range piles {
		timeNeed += (banana + speed - 1) / speed
		if timeNeed > timeLimit {
			return false
		}
	}

	return true
}

func minEatingSpeed(piles []int, h int) int {
	lo, hi := 1, slices.Max(piles)
	res := 1

	for lo <= hi {
		mid := (lo + hi) / 2

		if canEat(piles, h, mid) {
			res = mid
			hi = mid - 1
		} else {
			lo = mid + 1
		}
	}
	return res
}

func findMin(nums []int) int {
	i, j := 0, len(nums)-1
	for i < j {
		h := int(uint(i+j) >> 1)
		if nums[h] > nums[j] {
			i = h + 1
		} else {
			j = h
		}
	}
	return nums[i]
}

func searchRotate(nums []int, target int) int {
	i, j := 0, len(nums)-1
	for i <= j {
		m := int(uint(i+j) >> 1)
		if nums[m] == target {
			return m
		}
		if nums[m] < nums[j] {
			if nums[m] < target && target <= nums[j] {
				i = m + 1
			} else {
				j = m - 1
			}
		} else {
			if nums[i] <= target && target < nums[m] {
				j = m - 1
			} else {
				i = m + 1
			}
		}
	}
	return -1
}

type TimeMap struct {
	s map[string][]ValTimeStamp
}

type ValTimeStamp struct {
	ts  int
	val string
}

func NewTimeMap() TimeMap {
	return TimeMap{map[string][]ValTimeStamp{}}
}

func (this *TimeMap) Set(key string, value string, timestamp int) {
	if _, ok := this.s[key]; !ok {
		this.s[key] = []ValTimeStamp{}
	}
	this.s[key] = append(this.s[key], ValTimeStamp{timestamp, value})
}

func (this *TimeMap) Get(key string, timestamp int) string {
	s, ok := this.s[key]
	if !ok || s[0].ts > timestamp {
		return ""
	}
	i, found := slices.BinarySearchFunc(s, timestamp, func(stamp ValTimeStamp, tc int) int {
		if stamp.ts == tc {
			return 0
		}
		if stamp.ts < tc {
			return -1
		}
		return 1
	})
	if !found {
		i--
	}
	return this.s[key][i].val
}
