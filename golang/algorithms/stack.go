package main

import (
	"fmt"
	"sort"
	"strconv"
)

func main() {
	fmt.Println(carFleet(12, []int{10, 8, 0, 5, 3}, []int{2, 4, 1, 1, 3}))
}

func isValid(s string) bool {
	brackets := map[rune]rune{'(': ')', '{': '}', '[': ']'}

	var stack []rune
	for _, p := range s {
		if brackets[p] != 0 {
			stack = append(stack, p)
			continue
		}
		if len(stack) == 0 {
			return false
		}
		top := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if brackets[top] != p {
			return false
		}
	}
	return len(stack) == 0
}

func evalRPN(tokens []string) int {
	var stack []int

	for _, t := range tokens {
		val, err := strconv.Atoi(t)
		if err == nil {
			stack = append(stack, val)
			continue
		}

		v1 := stack[len(stack)-2]
		v2 := stack[len(stack)-1]
		switch t {
		case "+":
			val = v1 + v2
		case "-":
			val = v1 - v2
		case "*":
			val = v1 * v2
		case "/":
			val = v1 / v2
		}
		stack[len(stack)-2] = val
		stack = stack[:len(stack)-1]
	}

	return stack[0]
}

func generateParenthesis(n int) []string {
	var result []string

	var dfs func(s string, o, c int)
	dfs = func(s string, o, c int) {
		if len(s) == n*2 {
			result = append(result, s)
			return
		}
		if o < n {
			dfs(s+"(", o+1, c)
		}
		if c < o {
			dfs(s+")", o, c+1)
		}
	}

	dfs("", 0, 0)
	return result
}

func dailyTemperatures(temperatures []int) []int {
	result := make([]int, len(temperatures))
	stack := make([]int, 0, len(temperatures))
	for i, t := range temperatures[:len(temperatures)-1] {
		next := temperatures[i+1]
		if next <= t {
			stack = append(stack, i)
			continue
		}
		result[i] = 1

		for j := len(stack) - 1; j >= 0; j-- {
			k := stack[j]
			if next <= temperatures[k] {
				break
			}
			result[k] = i + 1 - k
			stack = stack[:j]
		}
	}
	return result
}

// n*log(n)
func carFleetWithSort(target int, position []int, speed []int) int {
	cars := make([]struct {
		pos   int
		speed int
		time  float32
	}, len(position))
	for i := range cars {
		cars[i] = struct {
			pos   int
			speed int
			time  float32
		}{
			pos:   position[i],
			speed: speed[i],
			time:  float32(target-position[i]) / float32(speed[i]),
		}
	}

	sort.Slice(cars, func(i, j int) bool {
		return cars[i].pos > cars[j].pos
	})

	slowest := 0
	res := 1
	for i := range cars[:len(cars)-1] {
		if cars[i+1].time > cars[slowest].time {
			res++
			slowest = i + 1
		}
	}
	return res
}

// n*m
func carFleet(target int, position []int, speed []int) int {
	time := make([]float64, target+1)
	for i := range position {
		left := target - position[i]
		time[left] = float64(left) / float64(speed[i])
	}

	slowest := 0.0
	res := 0
	for _, t := range time {
		if t == 0 {
			continue
		}

		if t > slowest {
			res++
			slowest = t
		}
	}
	return res
}
