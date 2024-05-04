package main

/**
 * Your Trie object will be instantiated and called as such:
 * obj := Constructor();
 * obj.Insert(word);
 * param_2 := obj.Search(word);
 * param_3 := obj.StartsWith(prefix);
 */

type Trie struct {
	end      bool
	children map[byte]*Trie
}

func newTrie() *Trie {
	return &Trie{children: map[byte]*Trie{}}
}

func (t *Trie) Insert(word string) {
	if len(word) == 0 {
		t.end = true
		return
	}
	next, ok := t.children[word[0]]
	if !ok {
		next = newTrie()
		t.children[word[0]] = next
	}
	next.Insert(word[1:])
}

func (t *Trie) Search(word string) bool {
	if len(word) == 0 {
		return t.end
	}
	if next, ok := t.children[word[0]]; ok {
		return next.Search(word[1:])
	}
	return false
}

func (t *Trie) StartsWith(prefix string) bool {
	if len(prefix) == 0 {
		return true
	}
	if next, ok := t.children[prefix[0]]; ok {
		return next.StartsWith(prefix[1:])
	}
	return false
}

//--------------------------------------------------------------

/**
 * Your WordDictionary object will be instantiated and called as such:
 * obj := Constructor();
 * obj.AddWord(word);
 * param_2 := obj.Search(word);
 */

type WordDictionary struct {
	children [26]*WordDictionary
	word     bool
}

func newDict() *WordDictionary {
	return &WordDictionary{}
}

func (d *WordDictionary) AddWord(word string) {
	if len(word) == 0 {
		d.word = true
		return
	}
	next := d.children[word[0]-'a']
	if next == nil {
		next = newDict()
		d.children[word[0]-'a'] = next
	}
	next.AddWord(word[1:])
}

func (d *WordDictionary) Search(word string) bool {
	if len(word) == 0 {
		return d.word
	}
	if word[0] != '.' {
		next := d.children[word[0]-'a']
		return next != nil && next.Search(word[1:])
	}
	for _, next := range d.children {
		if next == nil {
			continue
		}
		if next.Search(word[1:]) {
			return true
		}
	}
	return false
}

// ---------------------------------------------------

func findWordsSlow(board [][]byte, words []string) (result []string) {
	var dfs func([][]byte, []byte, int, int) bool
	dfs = func(board [][]byte, word []byte, i, j int) bool {
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
		res := dfs(board, word[1:], i+1, j) ||
			dfs(board, word[1:], i-1, j) ||
			dfs(board, word[1:], i, j+1) ||
			dfs(board, word[1:], i, j-1)
		board[i][j] = tmp
		return res
	}

	found := map[string]bool{}
	for _, w := range words {
		for i := range board {
			for j := range board[i] {
				if found[w] {
					continue
				}
				if dfs(board, []byte(w), i, j) {
					found[w] = true
					result = append(result, w)
				}
			}
		}
	}
	return
}

type Trie2 struct {
	word     string
	end      bool
	children [26]*Trie2
}

func (t *Trie2) Insert(word string) {
	for _, ch := range word {
		i := ch - 'a'
		if t.children[i] == nil {
			t.children[i] = new(Trie2)
		}
		t = t.children[i]
	}
	t.word = word
}

func (t *Trie2) Delete(word string) bool {
	if len(word) == 0 {
		t.word = ""
	} else if t.children[word[0]-'a'].Delete(word[1:]) {
		t.children[word[0]-'a'] = nil
	}
	return t.word == "" && t.children == [26]*Trie2{}
}

func findWordsDfs(board [][]byte, root, trie *Trie2, result *[]string, i, j int) {
	if i < 0 || i >= len(board) ||
		j < 0 || j >= len(board[i]) ||
		board[i][j] == 0 ||
		trie.children[board[i][j]-'a'] == nil {
		return
	}
	trie = trie.children[board[i][j]-'a']
	if trie.word != "" {
		*result = append(*result, trie.word)
		root.Delete(trie.word)
	}

	tmp := board[i][j]
	board[i][j] = 0
	findWordsDfs(board, root, trie, result, i+1, j)
	findWordsDfs(board, root, trie, result, i-1, j)
	findWordsDfs(board, root, trie, result, i, j+1)
	findWordsDfs(board, root, trie, result, i, j-1)
	board[i][j] = tmp
}

func findWords(board [][]byte, words []string) (result []string) {
	root := new(Trie2)
	for _, w := range words {
		root.Insert(w)
	}
	for i := range board {
		for j := range board[i] {
			findWordsDfs(board, root, root, &result, i, j)
		}
	}
	return
}

func findWords1(board [][]byte, words []string) (result []string) {
	root := new(Trie2)
	var dfs func([][]byte, *Trie2, int, int)
	dfs = func(board [][]byte, trie *Trie2, i, j int) {
		if i < 0 || i >= len(board) ||
			j < 0 || j >= len(board[i]) ||
			board[i][j] == 0 ||
			trie.children[board[i][j]-'a'] == nil {
			return
		}
		trie = trie.children[board[i][j]-'a']
		if trie.word != "" {
			result = append(result, trie.word)
			root.Delete(trie.word)
		}

		tmp := board[i][j]
		board[i][j] = 0
		dfs(board, trie, i+1, j)
		dfs(board, trie, i-1, j)
		dfs(board, trie, i, j+1)
		dfs(board, trie, i, j-1)
		board[i][j] = tmp
		return
	}

	for _, w := range words {
		root.Insert(w)
	}
	for i := range board {
		for j := range board[i] {
			dfs(board, root, i, j)
		}
	}
	return
}
