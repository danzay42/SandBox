fn main() {
    break_from_labled_blocks();
    assert_eq!(let_else_example("2 chairs"), (2, "chairs"));
}

fn let_else_example(s: &str) -> (i32, &str) {
    let mut it = s.split(" ");
    let (Some(count_str), Some(item)) = (it.next(), it.next()) else {
        panic!("Can't segment: '{s}'");
    };
    let Ok(count) = count_str.parse() else {
        panic!("Can't parse '{count_str}'");
    };
    (count, item)
}

fn break_from_labled_blocks() {
    let result = 'my_block: {
        if false {
            break 'my_block 1;
        }
        if true {
            break 'my_block 2;
        }
        3
    };
    println!("result={result}");
}
