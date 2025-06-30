Дополнительная информация о запросе и способе его выполнения, пример с буфферами
```sql
EXPLAIN (analyze, buffers) <SQL>
```
# Советы
- Не следует в sql запросах использовать под-запросы, т.к. это может быть не так эффективно как join-ы из-за оптимизаций СУБД
- используюй bigserial вместо serial

# Полезные истчники
- https://www.youtube.com/watch?v=gA3A_epB3So
- https://www.youtube.com/watch?v=Pk125DazUyI
- https://www.youtube.com/watch?v=VC9KbAA_5rE