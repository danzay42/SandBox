package main

import (
	"sort"
	"unicode"
)

func isPalindrome(s string) bool {
	runes := make([]rune, 0, len(s))
	for _, r := range s {
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			runes = append(runes, unicode.ToLower(r))
		}
	}

	i, j := 0, len(runes)-1
	for i < j {
		if runes[i] != runes[j] {
			return false
		}
		i++
		j--
	}
	return true
}

func twoSumSorted(numbers []int, target int) []int {
	i, j := 0, len(numbers)-1
	for i < j {
		sum := numbers[i] + numbers[j]
		switch {
		case sum == target:
			return []int{i, j}
		case sum < target:
			i++
		case sum > target:
			j--
		}
	}
	return []int{}
}

func twoSumSortedAll(nums []int, target int) [][]int {
	var result [][]int
	l, r := 0, len(nums)-1
	for l < r {
		sum := nums[l] + nums[r]
		switch {
		case sum == target:
			result = append(result, []int{-target, nums[l], nums[r]})
			l++
			r--
			for l < r && nums[l] == nums[l-1] {
				l++
			}
			for l < r && nums[r] == nums[r+1] {
				r--
			}
		case sum < target:
			l++
		case sum > target:
			r--
		}
	}
	return result
}

func threeSum(nums []int) [][]int {
	sort.Ints(nums)
	var results [][]int

	for i := 0; i < len(nums)-2; i++ {
		if i > 0 && nums[i] == nums[i-1] {
			continue
		}
		res := twoSumSortedAll(nums[i+1:], -nums[i])
		results = append(results, res...)
	}
	return results
}

func maxArea(height []int) int {
	m := 0
	l, r := 0, len(height)-1
	for l < r {
		m = max(m, min(height[l], height[r])*(r-l))
		if height[l] < height[r] {
			l++
		} else {
			r--
		}
	}
	return m
}

func trap(height []int) int {
	trapArea := 0
	maxAreaHeight := 0
	left, right := 0, len(height)-1
	for left < right {
		h := min(height[left], height[right])
		trapArea -= h
		if h > maxAreaHeight {
			trapArea += (h - maxAreaHeight) * (right - left)
			maxAreaHeight = h
		}
		if height[left] < height[right] {
			left++
		} else {
			right--
		}
	}
	return trapArea
}
