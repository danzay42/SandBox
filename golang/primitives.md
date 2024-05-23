# Channels
- gorutine-safe (hchan.mutex)
- храненние элементов в FIFO (hchan.buf)
- передача данных между горутинами (sendDirect, операции с hchan.buf)
- блокировка горутин (hchan.sendq/hchan.recvq, gopark/goready)

```go
type hchan struct {
	qcount   uint           // total data in the queue
	dataqsiz uint           // size of the circular queue
	buf      unsafe.Pointer // points to an array of dataqsiz elements
	elemsize uint16
	closed   uint32
	elemtype *_type // element type
	sendx    uint   // send index
	recvx    uint   // receive index
	recvq    waitq  // list of recv waiters
	sendq    waitq  // list of send waiters

	// lock protects all fields in hchan, as well as several
	// fields in sudogs blocked on this channel.
	//
	// Do not change another G's status while holding this lock
	// (in particular, do not ready a G), as this can deadlock
	// with stack shrinking.
	lock mutex
}
```

# Map
- разбиение данных по бакетам
- индекс бакета = hash(key)
  - равномероность (записи равномерно распределенны по бакетам)
  - быстрота (обеспечение работы за константное время)
  - детерминированость (один и тот же результат на определенный ключ)
  - криптоустойчивость (невозможность подобрать ключ)
- вместо generic-ов используются **type_descriptor**, предоставляющий предостовляющий базовые операции над типом:
  - hash
  - equal
  - copy

```go
type hmap struct {
	// Note: the format of the hmap is also encoded in cmd/compile/internal/reflectdata/reflect.go.
	// Make sure this stays in sync with the compiler's definition.
	count     int // # live cells == size of map.  Must be first (used by len() builtin)
	flags     uint8
	B         uint8  // log_2 of # of buckets (can hold up to loadFactor * 2^B items)
	noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
	hash0     uint32 // hash seed

	buckets    unsafe.Pointer // array of 2^B Buckets. may be nil if count==0.
	oldbuckets unsafe.Pointer // previous bucket array of half the size, non-nil only when growing
	nevacuate  uintptr        // progress counter for evacuation (buckets less than this have been evacuated)

	extra *mapextra // optional fields
}
```

заключение:
- заранее аллоцировать размер map (из-за дорогого процесса эвакуации бакетов)
- учитывать случайный обход map
- map растет при достжении определенного значения loadFactor (~6.5)
- нельзя брать указатель на эдемент map

# Slice

```go
type slice struct {
	array unsafe.Pointer
	len   int
	cap   int
}
```

- оболочка над массивом (последовательность постоянной длины)
- передается всегда по указателю

Рекомендации:
- проверять на пустоту с помощью `len`
- по возможности аллоцировать память заранее
- при изменении переданного слайса - делаем его копию
- результат `append` присваивать тойже переменной