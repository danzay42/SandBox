package main

import (
	"math"
	"slices"
)

func climbStairs(n int) int {
	vars, mem := 1, 0
	for i := 0; i < n; i++ {
		vars, mem = mem+vars, vars
	}
	return vars
}

// ----------------------------------------------------

func minCostClimbingStairs(cost []int) int {
	costSum, mem := 0, 0
	for i := 0; i < len(cost)-1; i++ {
		newSum := min(costSum+cost[i+1], mem+cost[i])
		costSum, mem = newSum, costSum
	}
	return costSum
}

// ----------------------------------------------------

func rob1(nums []int) int {
	snatch, mem := 0, 0
	for i := 0; i < len(nums); i++ {
		snatch, mem = max(mem+nums[i], snatch), snatch
	}
	return snatch
}

func rob2(nums []int) int {
	return max(nums[0], rob1(nums[1:]), rob1(nums[:len(nums)-1]))
}

// ----------------------------------------------------

func longestPalindrome(s string) string {
	result, maxLen := "", 0
	palindrome := func(l, r int) {
		for 0 <= l && r < len(s) && s[l] == s[r] {
			rr := r + 1
			if rr-l > maxLen {
				maxLen = rr - l
				result = s[l:rr]
			}
			r++
			l--
		}
	}

	for i := 0; i < len(s); i++ {
		palindrome(i, i)
		palindrome(i, i+1)
	}
	return result
}

// ----------------------------------------------------

func countSubstrings(s string) (c int) {
	palindrome := func(l, r int) {
		for 0 <= l && r < len(s) && s[l] == s[r] {
			c++
			r++
			l--
		}
	}

	for i := 0; i < len(s); i++ {
		palindrome(i, i)
		palindrome(i, i+1)
	}
	return c
}

// ----------------------------------------------------

func numDecodings(s string) int {
	s += "1"
	count, mem := 1, 0
	canDivPrev := true
	for i := 0; i < len(s)-1; i++ {
		if s[i] == '0' {
			return 0
		}
		// v, _ := strconv.Atoi(s[i : i+2])
		v := (s[i]-'0')*10 + (s[i+1] - '0')
		tmp := mem
		mem = count
		if canDivPrev && s[i+1] != '0' {
			count += tmp
		}
		canDivPrev = v < 27 && s[i+1] != '0'
		if v < 27 && s[i+1] == '0' {
			i++
		}
	}
	return count
}

// ----------------------------------------------------

func coinChangeRecursion(coins []int, amount int) int {
	slices.Sort(coins)
	slices.Reverse(coins)

	if len(coins) == 0 {
		return -1
	}

	w, r := amount/coins[0], amount%coins[0]
	if r == 0 {
		return w
	}

	minRes := math.MaxInt
	for i := w; i >= 0; i-- {
		m := coinChangeRecursion(coins[1:], amount-coins[0]*i)
		if m != -1 && m+i < minRes {
			minRes = m + i
		}
	}
	if minRes != math.MaxInt {
		return minRes
	}
	return -1
}

func coinChangeRecursionWithMemo(coins []int, amount int) int {
	slices.Sort(coins)
	slices.Reverse(coins)
	memo := map[int]int{}

	var dfs func(int) int
	dfs = func(remains int) int {
		if r, ok := memo[remains]; ok {
			return r
		}
		if remains == 0 {
			return 0
		}
		if remains < 0 {
			return math.MaxInt32
		}
		res := math.MaxInt32
		for _, c := range coins {
			if c > remains {
				continue
			}
			res = min(res, 1+dfs(remains-c))
		}
		memo[remains] = res
		return res
	}

	res := dfs(amount)
	if res == math.MaxInt32 {
		return -1
	}
	return res
}

func coinChange(coins []int, amount int) int {
	dp := make([]int, amount+1)
	for i := 1; i < amount+1; i++ {
		dp[i] = math.MaxInt32
	}
	for _, c := range coins {
		for a := c; a < amount+1; a++ {
			dp[a] = min(dp[a], 1+dp[a-c])
		}
	}
	if dp[amount] == math.MaxInt32 {
		return -1
	}
	return dp[amount]
}

// ----------------------------------------------------

func maxProduct(nums []int) int {
	prod, cMin, cMax := nums[0], 1, 1
	for _, num := range nums {
		if num < 0 {
			cMax, cMin = cMin, cMax
		}
		cMax = max(num, num*cMax)
		cMin = min(num, num*cMin)
		prod = max(prod, cMax)
	}
	return prod
}

// ----------------------------------------------------

func wordBreakRecursionWithMemo(s string, wordDict []string) bool {
	type dfsT = func(string) bool
	var dfs dfsT
	dfs = func(s string) bool {
		for _, k := range wordDict {
			if len(k) < len(s) &&
				k == s[:len(k)] &&
				dfs(s[len(k):]) {
				return true
			}
		}
		return false
	}
	cache := func(f dfsT) dfsT {
		m := map[string]bool{}
		for _, word := range wordDict {
			m[word] = true
		}
		return func(s string) bool {
			if _, ok := m[s]; !ok {
				m[s] = f(s)
			}
			return m[s]
		}
	}

	dfs = cache(dfs)
	return dfs(s)
}

func wordBreakDP(s string, wordDict []string) bool {
	mem := make([]bool, len(s)+1)
	mem[len(s)] = true

	for i := len(s) - 1; i >= 0; i-- {
		for j := 0; j < len(wordDict) && !mem[i]; j++ {
			w, wi := wordDict[j], len(wordDict[j])+i
			if wi <= len(s) && w == s[i:wi] {
				mem[i] = mem[wi]
			}
		}
	}

	return mem[0]
}

// ----------------------------------------------------

func lengthOfLISDP(nums []int) int {
	dp := make([]int, len(nums))
	lis := 1
	for i := 0; i < len(nums); i++ {
		for j := 0; j <= i; j++ {
			if nums[j] < nums[i] {
				dp[i] = max(dp[i], dp[j])
			}
		}
		dp[i]++
		lis = max(lis, dp[i])
	}
	return lis
}

func lengthOfLISBinary(nums []int) int {
	lis := []int{nums[0]}
	for _, n := range nums {
		if n > lis[len(lis)-1] {
			lis = append(lis, n)
			continue
		}
		i, _ := slices.BinarySearch(lis, n)
		lis[i] = n
	}
	return len(lis)
}

// ----------------------------------------------------

func canPartition(nums []int) bool {
	sum, maxNum := 0, 0
	for _, n := range nums {
		sum += n
		maxNum = max(maxNum, n)
	}
	target, odd := sum/2, sum%2 == 1
	if odd || maxNum > target {
		return false
	}

	mem := make([]bool, target)
	mem[0] = true
	for _, n := range nums {
		if mem[target-n] {
			return true
		}
		for j := target - n; j >= 0; j-- {
			if mem[j] {
				mem[j+n] = mem[j]
			}
		}
	}
	return false
}
