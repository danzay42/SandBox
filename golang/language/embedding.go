package main

import (
	"fmt"
)

type chatter interface {
	sayHi()
}

type human struct {
	name      string
	age       int
	greetings string
}

func (h *human) sayHi() {
	fmt.Printf("Hi, I'm %s, %s\n", h.name, h.greetings)
}

type american struct {
	human
	bankAccount int
}

type russian struct {
	chatter
	lizzardDamange int
}

func talk(o chatter) {
	o.sayHi()
}

func NewAmerican() *american {
	return &american{human: human{name: "John", age: 69, greetings: "I think I'm non binary, let's go starbucks"}, bankAccount: 777}
}

func NewRussian() russian {
	return russian{chatter: &human{name: "Ivan", age: 9999, greetings: "Нужно валить ящеров!"}, lizzardDamange: 9999}
}

func main() {
	talk(&human{name: "a Man", age: 33, greetings: "Hello World!"})
	talk(NewAmerican())
	talk(NewRussian())
}
