use std::time::{Duration, Instant};
use std::hint::black_box;

fn main() {
    // 1. MyStruct enum
    // 2. black box function (disable compiler optimizations between inside and outside the box)
    bench_push();
    // 3. add 'cargo add/remove [package]'
    // 4. half-open range patterns
    eligible_for_discount(18);
}

#[repr(u8)]
enum MyStruct_new {
    A, // 0
    B, // 1
    C = 42, // 42
    D, // 43
}

#[repr(u8)]
enum MyStruct_old {
    A(u8), // 0
    B(i8), // 1
    C(bool) = 42, // 42
    D(bool), // 43
}

fn push_cap(v: &mut Vec<i32>) {
    for i in 0..4 {
        v.push(i);
        black_box(v.as_ptr()); // add in case blackbox
    }
}

fn bench_push() -> Duration {
    let mut v = Vec::with_capacity(4);
    let now = Instant::now();
    push_cap(&mut v);
    now.elapsed()
}

fn eligible_for_discount(age: u8) -> bool {
    match age {
        ..=17 => true, // new
        18..=64 => false,
        65.. => true
    }
}