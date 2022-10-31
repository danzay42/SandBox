package main

import (
	_ "myapp/docs"

	"github.com/gin-gonic/gin"
	swaggerfiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

func main() {
	var r = gin.New()

	// "http://localhost:8080/"
	var url = ginSwagger.URL("swagger/openapi.yaml")
	r.GET(
		"/swagger/*a",
		ginSwagger.WrapHandler(swaggerfiles.Handler, url),
	)
	r.StaticFile("swagger/openapi.yaml", "./docs/openapi.yaml")

	r.Run()
}
