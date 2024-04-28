package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func (t *TreeNode) String() string {
	return fmt.Sprintf("[%d:%s,%s]", t.Val, t.Left, t.Right)
}

func invertTree(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}
	tmp := invertTree(root.Left)
	root.Left = invertTree(root.Right)
	root.Right = tmp
	return root
}

func maxDepth(root *TreeNode) int {
	if root == nil {
		return 0
	}
	return max(maxDepth(root.Left), maxDepth(root.Right)) + 1
}

func diameterOfBinaryTree(root *TreeNode) int {
	diameter := 0
	depthAndDiameter(root, &diameter)
	return diameter
}

func depthAndDiameter(root *TreeNode, diameter *int) int {
	if root == nil {
		return 0
	}
	l := depthAndDiameter(root.Left, diameter)
	r := depthAndDiameter(root.Right, diameter)
	*diameter = max(*diameter, l+r)
	return max(l, r) + 1
}

func isBalanced(root *TreeNode) bool {
	balance, _ := depthAndBalance(root)
	return balance
}

func depthAndBalance(root *TreeNode) (bool, int) {
	if root == nil {
		return true, 0
	}
	lb, ld := depthAndBalance(root.Left)
	rb, rd := depthAndBalance(root.Right)
	abs := ld - rd
	if abs < 0 {
		abs = -abs
	}
	if !lb || !rb || abs > 1 {
		return false, 0
	}
	return true, max(ld, rd) + 1
}

func isSameTree(p *TreeNode, q *TreeNode) bool {
	return (p == nil && q == nil) ||
		p != nil && q != nil && p.Val == q.Val &&
			isSameTree(p.Left, q.Left) &&
			isSameTree(p.Right, q.Right)
}

func isSubtree(root *TreeNode, subRoot *TreeNode) bool {
	return isSameTree(root, subRoot) ||
		root != nil &&
			(isSubtree(root.Left, subRoot) ||
				isSubtree(root.Right, subRoot))
}

func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
	if p.Val < root.Val && q.Val < root.Val {
		return lowestCommonAncestor(root.Left, p, q)
	}
	if p.Val > root.Val && q.Val > root.Val {
		return lowestCommonAncestor(root.Right, p, q)
	}
	return root
}

func levelOrderDfs(root *TreeNode, vals *[][]int, level int) {
	if root == nil {
		return
	}
	if level >= len(*vals) {
		*vals = append(*vals, []int{})
	}
	(*vals)[level] = append((*vals)[level], root.Val)
	levelOrderDfs(root.Left, vals, level+1)
	levelOrderDfs(root.Right, vals, level+1)
}

func levelOrder(root *TreeNode) (result [][]int) {
	levelOrderDfs(root, &result, 0)
	return
}

func rightSideViewDfs(root *TreeNode, vals *[]int, level int) {
	if root == nil {
		return
	}
	if level >= len(*vals) {
		*vals = append(*vals, 0)
	}
	(*vals)[level] = root.Val
	rightSideViewDfs(root.Left, vals, level+1)
	rightSideViewDfs(root.Right, vals, level+1)
}

func rightSideView(root *TreeNode) (result []int) {
	rightSideViewDfs(root, &result, 0)
	return
}

func goodNodesDfs(root *TreeNode, maxNode *TreeNode, goodNodesCount *int) {
	if root == nil {
		return
	}
	if root.Val >= maxNode.Val {
		*goodNodesCount++
		maxNode = root
	}
	goodNodesDfs(root.Left, maxNode, goodNodesCount)
	goodNodesDfs(root.Right, maxNode, goodNodesCount)
}

func goodNodes(root *TreeNode) (result int) {
	goodNodesDfs(root, root, &result)
	return
}

func isValidBSTDfs(root *TreeNode, tMin, tMax *int) bool {
	if root == nil {
		return true
	}
	if tMin != nil && root.Val <= *tMin ||
		tMax != nil && root.Val >= *tMax {
		return false
	}
	return isValidBSTDfs(root.Left, tMin, &root.Val) &&
		isValidBSTDfs(root.Right, &root.Val, tMax)
}

func isValidBST(root *TreeNode) bool {
	return isValidBSTDfs(root, nil, nil)
}

func isValidBSTDfs2(root *TreeNode, tMin, tMax int) bool {
	return root == nil ||
		tMin < root.Val && root.Val < tMax &&
			isValidBSTDfs2(root.Left, tMin, root.Val) &&
			isValidBSTDfs2(root.Right, root.Val, tMax)
}

func isValidBST2(root *TreeNode) bool {
	return isValidBSTDfs2(root, math.MinInt32-1, math.MaxInt32+1)
}

func kthSmallestDfs(root *TreeNode, nums *[]int, k int) {
	if root == nil || len(*nums) >= k {
		return
	}
	kthSmallestDfs(root.Left, nums, k)
	*nums = append(*nums, root.Val)
	kthSmallestDfs(root.Right, nums, k)
}

func kthSmallest(root *TreeNode, k int) int {
	var nums []int
	kthSmallestDfs(root, &nums, k)
	return nums[k-1]
}

func indexOf(nums []int, target int) int {
	for i, num := range nums {
		if num == target {
			return i
		}
	}
	return -1
}

func buildTree(preorder []int, inorder []int) *TreeNode {
	if len(preorder) == 0 {
		return nil
	}

	idx := indexOf(inorder, preorder[0])
	return &TreeNode{
		Val:   preorder[0],
		Left:  buildTree(preorder[1:idx+1], inorder[:idx]),
		Right: buildTree(preorder[idx+1:], inorder[idx+1:]),
	}
}

type Codec struct{}

func Constructor() Codec { return Codec{} }

func (this *Codec) serialize(root *TreeNode) string {
	var result []string
	var dfs func(node *TreeNode)

	dfs = func(node *TreeNode) {
		if node == nil {
			result = append(result, "null")
			return
		}
		result = append(result, strconv.Itoa(node.Val))
		dfs(node.Left)
		dfs(node.Right)
	}

	dfs(root)
	return fmt.Sprintf("[%s]", strings.Join(result, ","))
}

func (this *Codec) deserialize(data string) *TreeNode {
	tokens := strings.Split(data[1:len(data)-1], ",")

	var dfs func() *TreeNode
	dfs = func() *TreeNode {
		if tokens[0] == "null" {
			tokens = tokens[1:]
			return nil
		}
		val, _ := strconv.Atoi(tokens[0])
		tokens = tokens[1:]
		return &TreeNode{
			Val:   val,
			Left:  dfs(),
			Right: dfs(),
		}
	}

	return dfs()
}

func maxPathSum(root *TreeNode) int {
	maxPath := math.MinInt32
	var dfs func(*TreeNode) int
	dfs = func(tree *TreeNode) int {
		if tree == nil {
			return 0
		}
		leftMax := max(dfs(tree.Left), 0)
		rightMax := max(dfs(tree.Right), 0)
		maxPath = max(maxPath, leftMax+rightMax+tree.Val)
		return max(leftMax, rightMax) + tree.Val
	}
	return max(maxPath, dfs(root))
}

func main() {
	root := &TreeNode{
		Val: -10,
		Left: &TreeNode{
			Val:   9,
			Left:  nil,
			Right: nil,
		},
		Right: &TreeNode{
			Val: 20,
			Left: &TreeNode{
				Val:   15,
				Left:  nil,
				Right: nil,
			},
			Right: &TreeNode{
				Val:   7,
				Left:  nil,
				Right: nil,
			},
		},
	}

	fmt.Println(maxPathSum(root))
}
