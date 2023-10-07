# Usage
```shell
awk 'pattern {action}' input_file
cat input_file | awk 'pattern {action}'
awk -f awk_script input_file
```


# Flow
`pattern { action }`

```mermaid
stateDiagram-v2

line: Line of Awk \n code
pattern: Pattern \n matches?
action: Execute Action
next: Go next line

line --> pattern
pattern --> action: yes
pattern --> next: no
action --> next
next --> line
```

# Patterns (Types) 
Pattern | Summary
--- | ---
`BEGIN { statements }` | The `statements` are executed once before any input has been read
`END { statements }` | The `statements` are executed once after all input has been read
`expression { statements }` | The `statements` are executed at each input line where the expression is true, that i, nonzero or nonnull
`/regex/ { statements }` |  The `statements` are executed at each input line that contains a string matched by the [[Regular Expressions]], implies `$0 ~ /regex/`
`compound pattern { statements }` | A `compound pattern` combines expressions with `&&`, `||`, `!` and `()` for grouping
`pattern1, pattern2 { statements }` | A `range pattern` matches each input line from a line matched by first pattern to the next line matched by second pattern, inclusive; the `statements` are executed at each matching line

# Operators
Type | Operators | Example
--- | --- | ---
Assignment | `=` `+=` `-=` `*=` `/=` `%=` `^=`
conditional expression | `?:` | `x?y:z` mean: if `x` than `y` else `z`
logical | \|\| `&&` `!` `in`
matching | `~` `!~`
relational | `<` `<=` `==` `!=` `>=` `>`
arithmetic | `+` `-` `*` `/` `%` `^`
increment | `++i` `--i` `i++` `i--`
grouping | `( )`
concatenation | ` ` | `"a" "bc"` equal `"abc"`
field | `$`


# Actions
The statements in actions can include:
-  `_expressions_`, with constants, variables, assignments, function calls, etc
- `{ _statements_ }`
- `print _expression-list_`
- `if (_expression_) _statement_`
- `if (_expression_) _statement_ else _statement_`
- `while (_expression_) _statement_`
- `do _statement_ while (_expression_)`
- `for (_expression1_; _expression2_; _expression3_) _statement_` equal `_expression1_ ; while (_expression2_) { _statement_ ; _expression3_}`
- `for (_variable_ in _array_) _statement_`
- `break`
- `continue`
- `next`
- `exit`
- `exit _status_`

# Function
```shell
function _name_ (_argumetns_) {
	return _arguments_
}
```

# Built-in 
## Variables
Variable | Meaning | Default
:-- | --- | :-:
`ARGC` | number of command-line arguments
`ARGV` | array of command-line arguments
`FILENAME` | name of current input file
`FNR` | record number in current file
`FS` | controls the input field separator | ` `
`NF` | number of fields in current record
`NR` | number of records read so far
`OFMT` | output format for numbers | `%.6g`
`OFS` | output field separator | ` `
`ORS` | output record separator | `\n`
`RLENGTH` | length of string matched by match function
`RS` | controls the input record separator | `\n`
`RSTART` | start of sting matched by match function
`SUBSEP` | subscript separator | `\034`

## Math Functions
- `atan2(y,x)`
- `cos(x)`
- `exp(x)` equal $e^x$ 
- `int(x)`
- `log(x)` equal $log_e(x)$
- `rand()`
- `sin(x)`
- `sqrt(x)`
- `srand(x)` set new seed `x` for `rand()`

## String Function
- `gsub(r, s)`
- `gsub(r, s, t)`
- `index(s, t)`
- `length(s)`
- `match(s, r)`
- `split(s, a)`
- `split(s, a, fs)`
- `printf(fmt, expr-list)`
- `sprintf(fmt, expr-list)`
- `sub(r, s)`
- `sub(r, s, t)`
- `substr(s, p)`
- `substr(s, p, n)`