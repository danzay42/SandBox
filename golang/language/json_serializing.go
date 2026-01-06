package main

import (
	"encoding/json"
	"fmt"
)

type user struct {
	ID   int64  `json:"id"`
	Name string `json:"name"`
}

type fooUser struct {
	user
	Foo string `json:"foo"`
}

type barUser struct {
	user
	Bar string `json:"bar"`
}

type complexUser struct {
	User user   `json:"user"`
	Data string `json:"data"`
}

func check(data string, v any) {
	json.Unmarshal([]byte(data), &v)
	fmt.Printf("%#v\n", v)
}

func main() {
	a := `{
		"id": 1,
		"name": "foo",
		"foo": "...foo..."
	}`
	b := `{
		"id": 2,
		"name": "bar",
		"bar": "...bar..."
	}`
	c := `{
		"user": {
			"id": 3,
			"name": "complex"
		},
		"data": "..."
	}`

	u := user{}
	uFoo := fooUser{}
	uBar := barUser{}

	check(a, &u)
	check(a, &uFoo)
	check(a, &uBar)

	check(b, &u)
	check(b, &uFoo)
	check(b, &uBar)

	uComplex := complexUser{}
	check(c, &uComplex)
}
