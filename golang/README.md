# Project Layout

`/cmd/{...}/main.go` - точки запуска/сборки приложения  
`/internal` - приватные модули  
`/pkg/{public libs...}` - публичные модули  

## Internal layout
`/internal/pkg/{private libs...}` - приватные вспомогательные библиотеки  
`/internal/transport/{rest,grpc,...}` - логика для взаимодействия с потребителем  
`/internal/repository` - (storage) логика для доступа к хранилищам данных  

## DDD layout
`/internal/domain`  
`/internal/services`  

## CQS layout
`/internal/commands`  
`/internal/queries`  