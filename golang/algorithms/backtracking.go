package main

import (
	"bytes"
	"fmt"
	"math"
	"slices"
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

// -------------------------------------------------------------------

func combinationSum(candidates []int, target int) [][]int {
	if target < 0 || len(candidates) == 0 {
		return nil
	}
	if target == 0 {
		return [][]int{{}}
	}

	result := combinationSum(candidates[1:], target)
	for _, comb := range combinationSum(candidates, target-candidates[0]) {
		result = append(result, append([]int{candidates[0]}, comb...))
	}
	return result
}

func combinationSumFaster(candidates []int, target int) (result [][]int) {
	var backtrack func(int, []int, []int)
	backtrack = func(target int, nums, set []int) {
		if target < 0 || len(nums) == 0 {
			return
		}
		if target == 0 {
			result = append(result, append([]int{}, set...))
			return
		}
		backtrack(target, nums[1:], set)
		backtrack(target-nums[0], nums, append(set, nums[0]))
	}

	backtrack(target, candidates, []int{})
	return result
}

// -------------------------------------------------------------------

func permute(nums []int) (result [][]int) {
	if len(nums) == 1 {
		return [][]int{nums}
	}
	for i := 0; i < len(nums); i++ {
		for _, perm := range permute(append(nums[i+1:], nums[:i]...)) {
			result = append(result, append([]int{nums[i]}, perm...))
		}
	}
	return
}

// -------------------------------------------------------------------

func subsetsWithDup(nums []int) [][]int {
	if len(nums) == 0 {
		return [][]int{{}}
	}
	slices.Sort(nums)
	count := 1
	for count < len(nums) && nums[0] == nums[count] {
		count++
	}
	subset := subsetsWithDup(nums[count:])
	for _, s := range subset {
		for l := 1; l <= count; l++ {
			val := make([]int, l)
			copy(val, nums)
			subset = append(subset, append(val, s...))
		}
	}
	return subset
}

func subsetsWithDupFaster(nums []int) (result [][]int) {
	slices.Sort(nums)

	var backtrack func(int, []int)
	backtrack = func(idx int, set []int) {
		result = append(result, append([]int{}, set...))
		for i := idx; i < len(nums); i++ {
			if i > idx && nums[i] == nums[i-1] {
				continue
			}
			backtrack(i+1, append(set, nums[i]))
		}
	}

	backtrack(0, []int{})
	return
}

// -------------------------------------------------------------------

func combinationSum2(candidates []int, target int) (result [][]int) {
	var backtrack func(int, []int, []int)
	backtrack = func(target int, nums, set []int) {
		if target == 0 {
			result = append(result, append([]int{}, set...))
			return
		}
		if target < 0 {
			return
		}
		for i := 0; i < len(nums); i++ {
			if i > 0 && nums[i] == nums[i-1] {
				continue
			}
			backtrack(target-nums[i], nums[i+1:], append(set, nums[i]))
		}
	}

	slices.Sort(candidates)
	backtrack(target, candidates, []int{})
	return result
}

// -------------------------------------------------------------------

func existDfs(board [][]byte, word []byte, i, j int) bool {
	if len(word) == 0 {
		return true
	}
	if i < 0 || i >= len(board) ||
		j < 0 || j >= len(board[i]) ||
		board[i][j] != word[0] || board[i][j] == 0 {
		return false
	}

	tmp := board[i][j]
	board[i][j] = 0
	res := existDfs(board, word[1:], i+1, j) ||
		existDfs(board, word[1:], i-1, j) ||
		existDfs(board, word[1:], i, j+1) ||
		existDfs(board, word[1:], i, j-1)
	board[i][j] = tmp
	return res
}

func exist(board [][]byte, word string) bool {
	for i := range board {
		for j := range board[i] {
			if existDfs(board, []byte(word), i, j) {
				return true
			}
		}
	}
	return false
}

func exist2(board [][]byte, word string) bool {
	var dfs func([]byte, int64, int, int) bool
	dfs = func(word []byte, visited int64, i, j int) bool {
		if len(word) == 0 {
			return true
		}
		if i < 0 || i >= len(board) ||
			j < 0 || j >= len(board[i]) ||
			board[i][j] != word[0] {
			return false
		}
		var bitMask int64 = 1 << (i*len(board[0]) + j)
		if visited&bitMask > 0 {
			return false
		}

		return dfs(word[1:], visited|bitMask, i+1, j) ||
			dfs(word[1:], visited|bitMask, i-1, j) ||
			dfs(word[1:], visited|bitMask, i, j+1) ||
			dfs(word[1:], visited|bitMask, i, j-1)
	}

	for i := range board {
		for j := range board[i] {
			if dfs([]byte(word), 0, i, j) {
				return true
			}
		}
	}
	return false
}

// -------------------------------------------------------------------

func isPalindromeSimple(s string) bool {
	i, j := 0, len(s)-1
	for i < j {
		if s[i] != s[j] {
			return false
		}
		i++
		j--
	}
	return true
}

func partitionDfs(partitions *[][]string, s string, parts []string) {
	if len(s) == 0 {
		c := make([]string, len(parts))
		copy(c, parts)
		*partitions = append(*partitions, c)
		return
	}
	for i := 1; i <= len(s); i++ {
		left, right := s[:i], s[i:]
		if isPalindromeSimple(left) {
			partitionDfs(partitions, right, append(parts, left))
		}
	}
}

func partition(s string) (result [][]string) {
	partitionDfs(&result, s, []string{})
	return
}

// -------------------------------------------------------------------

var phoneMap = []string{"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}

func letterCombinations(digits string) (combs []string) {
	if len(digits) == 0 {
		return
	}
	prevComb := letterCombinations(digits[1:])
	if prevComb == nil {
		prevComb = []string{""}
	}
	for _, ch := range phoneMap[digits[0]-'2'] {
		for _, comb := range prevComb {
			combs = append(combs, string(ch)+comb)
		}
	}
	return
}

// -------------------------------------------------------------------

type Board [][]byte

func (b Board) String() string {
	var buf bytes.Buffer
	for _, s := range b {
		for _, sb := range s {
			if sb == 0 {
				buf.WriteString(fmt.Sprint("_"))
			} else {
				buf.WriteString(fmt.Sprint(string(sb)))
			}
		}
		buf.WriteString(fmt.Sprintln())
	}
	return buf.String()
}

func (b Board) stringSlice() []string {
	s := make([]string, len(b))
	for i, row := range b {
		s[i] = string(row)
	}
	return s
}

func newBytesBoard(n int) Board {
	b := make([][]byte, n)
	for i := range b {
		b[i] = make([]byte, n)
	}
	return b
}

func (b Board) copy() Board {
	copyBoard := make(Board, len(b))
	for i := 0; i < len(b); i++ {
		copyBoard[i] = make([]byte, len(b))
		copy(copyBoard[i], b[i])
	}
	return copyBoard
}

func (b Board) block(i, j int) {
	if i >= 0 && i < len(b) && b[i][j] != 'Q' {
		b[i][j] = '.'
	}
}

func (b Board) setQueen(i, j int) Board {
	for d := 0; d < len(b); d++ {
		b.block(d, j)
		b.block(i, d)
		b.block(i-j+d, d)
		b.block(i+j-d, d)
	}
	b[i][j] = 'Q'
	return b
}

func solveNQueens0(n int) (permutations [][]string) {
	var dfs func(Board, int)
	dfs = func(b Board, queens int) {
		if queens == 0 {
			permutations = append(permutations, b.stringSlice())
			return
		}
		for i := 0; i < len(b); i++ {
			row := len(b) - queens
			if b[row][i] != 0 {
				continue
			}
			dfs(b.copy().setQueen(row, i), queens-1)
		}
	}

	dfs(newBytesBoard(n), n)
	return
}

func newBoard(queens []Queen) []string {
	b := make([]string, len(queens))
	for _, q := range queens {
		row := make([]byte, len(queens))
		for j := range row {
			var ch byte = '.'
			if q.j == j {
				ch = 'Q'
			}
			row[j] = ch
		}
		b[q.i] = string(row)
	}
	return b
}

type Queen struct {
	i, j int
}

func (q *Queen) ok(queens []Queen) bool {
	for _, a := range queens {
		if q.i == a.i || q.j == a.j ||
			math.Abs(float64(q.i-a.i))/
				math.Abs(float64(q.j-a.j)) == 1 {
			return false
		}
	}
	return true
}

func solveNQueens(n int) (permutations [][]string) {
	var dfs func([]Queen)
	dfs = func(queens []Queen) {
		if len(queens) == n {
			permutations = append(permutations, newBoard(queens))
			return
		}
		for j := 0; j < n; j++ {
			q := Queen{i: len(queens), j: j}
			if !q.ok(queens) {
				continue
			}
			dfs(append(queens, q))
		}
	}

	dfs(nil)
	return
}
