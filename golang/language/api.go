package main

import "net/http"

func main() {
	mp := http.NewServeMux()
	mp.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		_, _ = writer.Write([]byte("base response"))
	})

	_ = http.ListenAndServe(":8080", mp)
}
