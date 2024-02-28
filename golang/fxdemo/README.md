# Uber-FX DI

- [Docs](https://pkg.go.dev/go.uber.org/fx)
- [Git](https://github.com/uber-go/fx)
- [Homepage](https://uber-go.github.io/fx/)

## Lifecycle

```mermaid
flowchart LR
    subgraph "Initialization (fx.New)"
    a[Provide] --> b[Decorate] --> c[Invoke]
    end
    subgraph "Execution (fx.App.Run)"
    c --> d[Start] --> e((Wait)) --> f[Stop]
    end
```

## Modules and Options

```go
// План для посроения графа зависимомтей приложения
options := fx.Options(OtherModulesOrOptions...)
// Именнованные опции
options := fx.Module("name", OtherModulesOrOptions...)

// Огранисения на время запуска (Start) и остановки (Stop) програмы
startOption := fx.StartTimeout(time.Duration)
stopOption := fx.StopTimeout(time.Duration)

// Логирование (для настройки логов fx - необходимо сконфигрурировать zap.Logger)
logOption := fx.WithLogger(func(...) fxevent.Logger {
    zapLogger := ...
    return &fxevent.ZapLogger{Logger: zapLogger}
}),
```


## Constructors

```go
var object Object
options := fx.Provide(
    // Базовые конструкторы
    func (inParams) (outParams, error) {...},
    
    // Конструктор на осонве уже существующего объекта
    fx.Supply(Object{}), // Создает узел графа с типом переданного объекта
    // Аналог Supply, инициализации объекта из графа 
    fx.Populate(&object),
    
    // Аннотация
    fx.Annotate(
        consructor,
        
        // Декораторы
        fx.As(new(Interface)), // от частного к общему
        fx.From(new(*impl)), // от обобщего к частному
        
        // Теги
        fx.ParamTags(`name:"fzz" optional:"true"`, `name:"bzz"`),
        fx.ResultTags(`name:"bar"`, `group:"routes"`),

        // Хуки
        fx.OnStart(fx.HookFunc),
        fx.OnStopt(fx.HookFunc),
    ),
    
    // Оболочка над определенным типом
    fx.Decorate(func (SomeInterface, ...anotherDependencies) (SomeInterface, error)),
    // Замена определенного типа
    fx.Replace(func (SomeInterface, ...anotherDependencies) (SomeInterface, error)),
    
    // Область видимости (опция fx.Provide)
    fx.Private,
    // Обработка ошибок
    fx.ErrorHook(...handlers),
)
```

## Param Objects

```go
type inParams struct {
    fx.In
    inputObject *Object `name:"[name]" group:"[groupname]"`

    // fx.In only
    inputObjects ...Object `group:"[groupname],soft"`
    inputObject *Object `optional:"true"`
}

type outParams struct {
    fx.Out
    outputObject *Object `name:"[name]" group:"[groupname]"`

    // fx.Out only
    outputObjects []Object `group:"[groupname],flatten"`
}

func New(inParams) (outParams, error) {}
```

## Groups & Names
```mermaid
flowchart TD
na[NewA] & nb[NewB] & nc[...] & nz[NewZ] --> r{{"[]Route"}} --> ca[NewConsumerA] & cb[NewConsumerB]
```

`groups` - группируют обекты по признаку  
`name` - выделяют объекты из группы однотипных

### Soft/Hard group

```mermaid
flowchart TD
na1((A)) & nb1((B)) & nc1((C)) --> r1{{"[]Group"}} --hard--> c1[ConsumerA]
na2((A)) & nb2((B)) & nc2((C)) --> r2{{"[]Group"}} -.soft.-> c2[ConsumerB]

style r2 stroke-dasharray: 5 5
style na2 stroke-dasharray: 5 5
style nb2 stroke-dasharray: 5 5
style nc2 stroke-dasharray: 5 5
```

```mermaid
flowchart TD
na((A)) & nb((B)) & nc((C)) --> r{{"[]Group"}}
r --hard--> c1[ConsumerA]
r -.soft.-> c2[ConsumerB]
```