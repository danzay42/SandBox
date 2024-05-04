package main

import "fmt"

func uniquePathsSlow(m int, n int) int {
	if m == 1 || n == 1 {
		return 1
	}
	return uniquePathsSlow(m-1, n) + uniquePathsSlow(m, n-1)
}

func uniquePaths(m int, n int) int {
	dp := make([]int, n)
	dp[0] = 1

	for i := 0; i < m; i++ {
		for j := 1; j < n; j++ {
			dp[j] += dp[j-1]
		}
	}
	return dp[n-1]
}

// ----------------------------------------------------

func main() {
	fmt.Println(uniquePaths(3, 7))
}
