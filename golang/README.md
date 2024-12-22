# Docs
- [100 go mistakes](https://100go.co/)
- [Uber Style Guide](https://github.com/sau00/uber-go-guide-ru/blob/master/style.md)
- [Goggle Style Guide](https://google.github.io/styleguide/go/best-practices)
- [Practical Go](https://dave.cheney.net/practical-go)
- [Patterns](https://github.com/AlexanderGrom/go-patterns)
- [Go by Example](https://gobyexample.com/)
- [GC Guide](https://tip.golang.org/doc/gc-guide)
- [DevDocs](https://go.dev/doc/)

# Dependencies
- [**awesome-go**](https://github.com/avelino/awesome-go)/[awesome-go-web](https://go.libhunt.com/)
- [samber](https://github.com/samber) - базовые инструменты разработки
- [copier](https://github.com/jinzhu/copier) - базовый инструмент мапинга структур
- [RAFT](https://github.com/lni/dragonboat)
## Http servers
- [net/http](https://pkg.go.dev/net/http)
  - middleware
  - subrouting, [routegroup](https://github.com/go-pkgz/routegroup)
  - path parameters
  - http methods
  - passing down context
- fasthttp
- [fiber](https://github.com/gofiber/fiber)
- [gin](https://github.com/gin-gonic/gin)
- [echo](https://github.com/labstack/echo)
- [chi](https://github.com/go-chi/chi)
## Logging
- [slog](https://github.com/gookit/slog)
- [tint](https://github.com/lmittmann/tint)
- [slog-multi](https://github.com/samber/slog-multi)
- [slog-sampling](https://github.com/samber/slog-sampling)
- [slog-formatter](https://github.com/samber/slog-formatter)
## Config
- [viper](https://github.com/spf13/viper)
- [envconfig](https://github.com/kelseyhightower/envconfig)
## CLI
- [cobra](https://github.com/spf13/cobra)
## DI
- [fx](https://github.com/uber-go/fx)
- [wire](https://github.com/google/wire)
## [ORM](https://github.com/d-tsuji/awesome-go-orms)
- [gorm](https://github.com/go-gorm/gorm)
- [beego](https://github.com/beego/beego)
- [squirrel](https://github.com/Masterminds/squirrel)
## Documentation
- [pkgsite](https://pkg.go.dev/golang.org/x/pkgsite/cmd/pkgsite)
## MQ,KV,Cache
- Redis
- Memcache
- [NATSio](https://nats.io/)
- [pebble](https://github.com/cockroachdb/pebble)
## Kuber Framework
- [kubebuilder](https://book.kubebuilder.io/)
- [operatorframework](https://operatorframework.io/)

# Tools
- `go generate`
- `go fmt`
- `go build`
- `go vet` - линтер
- `go test` - тестирование
- `go tool cover` - покрытие тестами
- `go doc` - генерация документации
- `go mod`
- `go get`
- `go install`
- [go tool pprof](https://github.com/google/pprof)
- [goenv](https://github.com/drewgonzales360/goenv)
- [mokery](https://github.com/vektra/mockery)
- [nil check linter](https://github.com/uber-go/nilaway)

# Templates
- [go-template](https://github.com/exepirit/go-template)
- [go-kit](https://github.com/go-kit/kit)
- [go-micro](https://github.com/go-micro/go-micro)

## [Project Layout](https://github.com/golang-standards/project-layout)
`/cmd/{...}/main.go` - точки запуска/сборки приложения  
`/internal` - приватные модули  
`/pkg/{public libs...}` - публичные модули  
### Internal layout
`/internal/pkg/{private libs...}` - приватные вспомогательные библиотеки  
`/internal/transport/{rest,grpc,...}` - логика для взаимодействия с потребителем  
`/internal/repository` - (storage) логика для доступа к хранилищам данных  
### DDD layout
`/internal/domain`  
`/internal/services`  
### CQS layout
`/internal/commands`  
`/internal/queries`