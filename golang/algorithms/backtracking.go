package main

import (
	"fmt"
)

func subsets(nums []int) [][]int {
	if len(nums) == 0 {
		return [][]int{{}}
	}
	subset := subsets(nums[1:])
	for _, s := range subset {
		subset = append(subset, append([]int{nums[0]}, s...))
	}
	return subset
}

func main() {
	fmt.Println(subsets([]int{1, 2, 3}))
}
