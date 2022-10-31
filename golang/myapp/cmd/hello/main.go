package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"runtime"
)

type mass float64

type person struct {
	name string
	age  int
}

func (p *person) updateAge(newAge int) {
	p.age = newAge
}

func test0() {
	const A = 1 << 10
	defer fmt.Println("this is the end!")
	fmt.Println(A)
	fmt.Println("Hello, World!")
	slice := []int{}
	array := [3]int{}
	fmt.Println(slice, array)
	var some mass = 10.
	println(some)
}

func test1() {

	var tom = person{name: "Tom", age: 24}
	var tomPointer *person = &tom
	fmt.Println("before", tom.age)
	tomPointer.updateAge(33)
	fmt.Println("after", tom.age)
}

func test2() {
	resp, err := http.Get("https://google.com")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer resp.Body.Close()
	io.Copy(os.Stdout, resp.Body)
}

func test3() {
	err := errors.New("some error")
	fmt.Println(err)
}

func test4() {
	var numCPU = runtime.NumCPU()
	var numGORUT = runtime.NumGoroutine()
	fmt.Printf("%v\n", numCPU)
	fmt.Printf("%+v\n", numCPU)
	fmt.Printf("%#v\n", numCPU)
	fmt.Printf("%+#v\n", numGORUT)
}

func main() {
	test0()
	test1()
	test2()
	test3()
	test4()
}
