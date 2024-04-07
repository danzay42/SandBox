package main

import (
	"sort"
)

func containsDuplicate[T byte | int](nums []T) bool {
	m := make(map[T]struct{}, len(nums))

	for _, v := range nums {
		_, ok := m[v]
		if ok {
			return true
		}
		m[v] = struct{}{}
	}
	return false
}

func isAnagram(s string, t string) bool {
	if len(s) != len(t) {
		return false
	}
	c := make(map[byte]int, len(s))
	for i := range s {
		if s[i] == t[i] {
			continue
		}
		c[s[i]] += 1
		c[t[i]] -= 1
	}

	for _, v := range c {
		if v != 0 {
			return false
		}
	}
	return true
}

func twoSumMem(nums []int, target int) []int {
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			if nums[i]+nums[j] == target {
				return []int{i, j}
			}
		}
	}
	return []int{}
}
func twoSumSpeed(nums []int, target int) []int {
	sums := map[int]int{}
	for i, num := range nums {
		j, ok := sums[target-num]
		if ok {
			return []int{i, j}
		}
		sums[num] = i
	}
	return []int{}
}

func groupAnagrams(strs []string) [][]string {
	hashMap := map[[26]int][]string{}

	for _, s := range strs {
		k := [26]int{}
		for _, c := range s {
			k[c-'a']++
		}
		hashMap[k] = append(hashMap[k], s)
	}

	var res [][]string
	for _, v := range hashMap {
		res = append(res, v)
	}
	return res
}

func topKFrequent(nums []int, k int) []int {
	c := map[int]int{}
	for _, num := range nums {
		c[num]++
	}

	freq := make([][]int, 0, len(c))
	for key, val := range c {
		freq = append(freq, []int{key, val})
	}

	sort.Slice(freq, func(i, j int) bool {
		return freq[i][1] < freq[j][1]
	})

	res := make([]int, len(c))
	for i, v := range freq {
		res[i] = v[0]
	}
	return res[:k]
}

func productExceptSelf(nums []int) []int {
	result := make([]int, len(nums))
	acc := 1
	for i, num := range nums {
		result[i] = acc
		acc *= num
	}
	acc = 1
	for i := len(nums) - 1; i > -1; i-- {
		result[i] *= acc
		acc *= nums[i]
	}
	return result
}

func isValidSudoku(board [][]byte) bool {
	var idxs [][][]int

	for i := 0; i < 9; i++ {
		var row [][]int
		var col [][]int
		var grid [][]int
		for j := 0; j < 9; j++ {
			row = append(row, []int{i, j})
			col = append(col, []int{j, i})
			grid = append(grid, []int{3*(i/3) + j/3, 3*(i%3) + j%3})
		}
		idxs = append(idxs, row, col, grid)
	}

	for _, idx := range idxs {
		if containsDuplicateOnBoard(board, idx) {
			return false
		}
	}
	return true
}

func containsDuplicateOnBoard(board [][]byte, idx [][]int) bool {
	m := make(map[byte]struct{}, len(idx))
	for _, i := range idx {
		v := board[i[0]][i[1]]
		if v == byte('.') {
			continue
		}
		_, ok := m[v]
		if ok {
			return true
		}
		m[v] = struct{}{}
	}
	return false
}

func isValidSudoku2(board [][]byte) bool {
	var rows, columns, squares [9][9]bool
	for i := 0; i < 9; i++ {
		for j := 0; j < 9; j++ {
			item := board[i][j]
			if item == '.' {
				continue
			}
			k := int(item - '1') // element id
			s := i/3*3 + j/3     // square id
			if rows[i][k] || columns[j][k] || squares[s][k] {
				return false
			}
			rows[i][k], columns[j][k], squares[s][k] = true, true, true
		}
	}
	return true
}

func longestConsecutive(nums []int) int {
	mem := make(map[int]bool, len(nums))
	for _, num := range nums {
		mem[num] = true
	}

	maxSeq := 0
	for k, _ := range mem {
		deleted := deleteSeqRecursiveFrom(mem, k)
		//deleted := deleteSeqCycleFrom(mem, k)
		if deleted > maxSeq {
			maxSeq = deleted
		}
		if deleted > len(mem) {
			break
		}
	}

	return maxSeq
}

func deleteSeqRecursiveFrom(seq map[int]bool, key int) int {
	if !seq[key] {
		return 0
	}
	delete(seq, key)
	return 1 + deleteSeqRecursiveFrom(seq, key+1) + deleteSeqRecursiveFrom(seq, key-1)
}

func deleteSeqCycleFrom(seq map[int]bool, key int) int {
	delete(seq, key)
	res := 1
	for l := key - 1; seq[l]; l-- {
		delete(seq, l)
		res++
	}
	for r := key + 1; seq[r]; r++ {
		delete(seq, r)
		res++
	}
	return res
}
