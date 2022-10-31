package main

import (
	"fmt"
	"sync"
	"time"
)

type Fetcher interface {
	// Fetch returns the body of URL and
	// a slice of URLs found on that page.
	Fetch(url string) (body string, urls []string, err error)
}

type Visiter interface {
	CheckOrPending(url string) bool
	Done(url string)
	WaitComplete()
}

type VisitedUrls struct {
	v  map[string]bool
	mu sync.Mutex
	wg sync.WaitGroup
}

func (vu *VisitedUrls) CheckOrPending(url string) bool {
	vu.mu.Lock()
	defer vu.mu.Unlock()
	_, pre := vu.v[url]
	if pre {
		return true
	}
	vu.v[url] = false
	vu.wg.Add(1)
	return false
}
func (vu *VisitedUrls) Done(url string) {
	vu.mu.Lock()
	vu.v[url] = true
	vu.mu.Unlock()
	vu.wg.Done()
}
func (vu *VisitedUrls) WaitComplete() {
	time.Sleep(100 * time.Millisecond)
	vu.wg.Wait()
}

// Crawl uses fetcher to recursively crawl
// pages starting with url, to a maximum of depth.
func Crawl(vu Visiter, url string, depth int, fetcher Fetcher) {
	// TODO: Fetch URLs in parallel.
	// TODO: Don't fetch the same URL twice.
	// This implementation doesn't do either:
	if depth <= 0 || vu.CheckOrPending(url) {
		return
	}
	defer vu.Done(url)
	body, urls, err := fetcher.Fetch(url)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Printf("found: %s %q\n", url, body)
	for _, u := range urls {
		go Crawl(vu, u, depth-1, fetcher)
	}
}

func main() {
	var vu *VisitedUrls = &VisitedUrls{v: make(map[string]bool)}
	Crawl(vu, "https://golang.org/", 4, fetcher)
	vu.WaitComplete()
}

// fakeFetcher is Fetcher that returns canned results.
type fakeFetcher map[string]*fakeResult

type fakeResult struct {
	body string
	urls []string
}

func (f fakeFetcher) Fetch(url string) (string, []string, error) {
	if res, ok := f[url]; ok {
		return res.body, res.urls, nil
	}
	return "", nil, fmt.Errorf("not found: %s", url)
}

// fetcher is a populated fakeFetcher.
var fetcher = fakeFetcher{
	"https://golang.org/": &fakeResult{
		"The Go Programming Language",
		[]string{
			"https://golang.org/pkg/",
			"https://golang.org/cmd/",
		},
	},
	"https://golang.org/pkg/": &fakeResult{
		"Packages",
		[]string{
			"https://golang.org/",
			"https://golang.org/cmd/",
			"https://golang.org/pkg/fmt/",
			"https://golang.org/pkg/os/",
		},
	},
	"https://golang.org/pkg/fmt/": &fakeResult{
		"Package fmt",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
	"https://golang.org/pkg/os/": &fakeResult{
		"Package os",
		[]string{
			"https://golang.org/",
			"https://golang.org/pkg/",
		},
	},
}
