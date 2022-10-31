fn main() {
    example_1();
    example_2();
    example_3();
    example_4();
    example_5();
}

// ---------------------------------------------------------------------------

fn example_5() {
    // let reference_to_nothing = dangle();
}

// fn dangle() -> &String { // error: cannot return reference to free memory
//     let s = String::from("some string");
//     &s
// }

// ---------------------------------------------------------------------------

fn example_4() {
    let mut s = String::from("some string");
    change(&mut s);
    println!("{s}");
    let r1 = &mut s;
    // let r2 = &mut s;  // error: only ONE mutable reference (&mut) can exist
    println!("r1={r1}");

    let s = String::from("some string");
    let r1 = &s;
    let r2 = &s; // its ok to have multiply immutable reference
    println!("r1={r1}, r2={r2}");

    let mut s = String::from("some string");
    let r1 = &s;
    let r2 = &s;
    // let r3 = &mut s; // error: cannot use mut reference while immutable exists (r1, r2)
    println!("r1={r1}, r2={r2}");

    let r3 = &mut s; // its ok: after free immutable reference (r1, r2)
    println!("r3={r3}")
}

fn change(s: &mut String) {
    // to change value it must be mutable reference
    s.push_str("[pushed string]");
}

// ---------------------------------------------------------------------------

fn example_3() {
    let s = String::from("some string");
    let len = calculate_len(&s); // &-reference don't get ownership
    println!("len of '{}' is {}", s, len);
}

fn calculate_len(s: &String) -> usize {
    // s - borrow value, is immutable by default
    let l = s.len();
    l
}

// ---------------------------------------------------------------------------

fn example_2() {
    let s1 = gives_ownership();
    let s2 = String::from("some string");
    let s3 = takes_and_gives_back_ownership(s2);
    println!("s1={s1}, s3={s3}");
}

fn gives_ownership() -> String {
    let s = String::from("some gived string");
    println!("{}", s);
    s
}

fn takes_and_gives_back_ownership(some_srting: String) -> String {
    println!("{}", some_srting);
    some_srting
}

// ---------------------------------------------------------------------------

fn example_1() {
    let s = String::from("some string");
    take_ownership(s);
    // println!("{}", s);  // This is borrow error

    let x = 5;
    makes_copy(x);
    println!("{}", x);
}

fn take_ownership(some_srting: String) {
    println!("{}", some_srting);
}

fn makes_copy(some_integer: i32) {
    println!("{}", some_integer);
}

// ---------------------------------------------------------------------------
