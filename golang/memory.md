# GC

- https://tip.golang.org/doc/gc-guide
- https://betterprogramming.pub/memory-optimization-and-garbage-collector-management-in-go-71da4612a960
- https://medium.com/@souravchoudhary0306/exploring-the-inner-workings-of-garbage-collection-in-golang-tricolor-mark-and-sweep-e10eae164a12

Escape analysis:
- массивы >10MB
- слайсы >64KB

Aлгоритме MARK & SWEP

Физическая память <-> процессорное время

Управление GC:
- **COGC**: живая куча == новой куче * GOGC
- **GOMEMLIMIT**
- `sync.Pool` (threadsafe)
- `arena` (no threadsafe)