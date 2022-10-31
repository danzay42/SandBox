// use std::io;
// use std::io::prelude::*;
// use std::fs::File;
use std::{sync::atomic::*, str::FromStr};
use ipaddress::IPAddress;


fn main() {
    // Variables
    let usual_var = 10;
    let mut mut_var = 20;
    mut_var = 5;
    println!("\nVariables:\n\tusual = {usual_var}, mutable = {mut_var}");

    // Uninitilized variables
    let mut x: i32;
    println!("\nUninitilized variables:\n\tx");
    x = 5;

    // Struct
    struct Rectangle {
        lenght: f64,
        width: f64,
    }
    impl Rectangle {
        fn area(&self) -> f64 {
            self.lenght * self.width
        }
    }
    let r = Rectangle {lenght: 2., width: 5.}.area();
    println!("\nStruct:\n\tarea = {r}");

    // Traits
    trait Shape {
        fn area(&self) -> f64;
        fn perimeter(&self) -> f64;
    }
    impl Shape for Rectangle {
        fn area(&self) -> f64 { self.lenght * self.width }
        fn perimeter(&self) -> f64 { 2. * self.lenght + 2. * self.width }
    }
    let r = Rectangle { lenght: 3., width: 4. };
    println!("\nTrait:\n\tarea = {}, perimeter = {}", r.area(), r.perimeter());

    // Generics & Polimorphism
    fn describe_1<T: Shape>(shape: &T) {
        println!("\tArea:      {}", shape.area());
        println!("\tPerimeter: {}", shape.perimeter());
    }
    println!("\nGenerics & Polymorphism:");
    describe_1(&r);

    // Trait Objects & Runtime Polymorphism
    fn describe_2(shape: &dyn Shape) {
        println!("\tArea:      {}", shape.area());
        println!("\tPerimeter: {}", shape.perimeter());
    }
    println!("\nTrait Objects & Runtime Polymorphism:");
    describe_2(&r);

    // Enums
    enum OverCommitPolicy {
        Heuristic,
        Always,
        Never,
    }
    // let overcommit_okey = match policy {
    //     OverCommitPolicy::Heuristic => size < heuristic_limit(),
    //     OverCommitPolicy::Always => true,
    //     OverCommitPolicy::Never => size < remaining_memory(),
    // };
    
    // Emums with data
    enum Address {
        IP {host: IPAddress, port: i32},
        UNIX {name: String},
        Raw,
    }
    // match address {
    //     Address::IP { host, port } => ...,
    //     Address::UNIX { name } => ...,
    //     Address::Raw => ...,
    // };
    
    // // Option & Result
    // enum Option<T> {
    //     None,
    //     Some<T>
    // }
    // enum Result<T, E> {
    //     Ok(T),
    //     Err(E),
    // }
    // if let Some(x) = potential_x { processing };

    // // Error handling
    // foo?
    // Ok(foo)? => foo
    // Err(bar)? => {return Err(From::from(bar));}
    // fn read_data() -> Result<MyData, MyError> {
    //     let file = File::open("data.txt")?;
    //     let msg = file.read_to_string(...)?;
    //     let data = parse(msg)?;
    //     Ok(data)
    // }

    // // Panics and unwinding
    // 1/0 
    // [3,4,5][10]
    // [3,4,5].get(10) == None
    // panic!("everything went wrong")
    
    // References
    let x = 10;
    let y = &x;
    println!("\nReferences:\n\ty = {}", *y);
    fn my_print(a: &i32) {
        println!("\ta = {}", a);
    }
    my_print(&x);

    // // Dangling references
    // let mut y: &i32;
    // for i in 1..5 {
    //     y = &i;
    // }
    // println!("\nDangling references:\n\t{}", y);

    // // Mutable references
    // let mut x = 5;
    // let y = &x;
    // *y = 10;
    // println!("\Mutable references:\n\t{}", x);

    // // Mutable references and unique references
    // let mut x = 5;
    // let y = &mut x;
    // let z = &x;
    // *y = 10;
    // println!("\nMutable references and unique references:\n\tx = {}", x);
    
    // Atomics
    // struct AtomicU32 {
    //     v: UnsafeCell<u32>
    // }
    // impl AtomicU32 {
    //     fn store(&self, val: u32, oreder: Ordering) { unsafe { atomic_store(self.v.get(), val, oreder) }}
    // }
    let x = AtomicU32::new(1);
    let y = &x;
    let z = &x;
    y.store(4, Ordering::SeqCst);
    println!("\nAtomics:\n\tz = {}", z.load(Ordering::SeqCst));


    // Safe and unsafe Rust
    fn zero_1(x: *mut u8) { unsafe { *x = 0; } }
    unsafe fn zero_2(x: *mut u8) { *x = 0; }
    let mut x = vec![3u8, 4, 5];
    let p = &mut x[0];
    zero_1(p);
    unsafe {zero_2(p);}
    println!("\nSafe and unsafe Rust:\n\tx = {:?}", x);

    // Explicit lifetimes
    fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
        if x.len() > y.len()    {x}
        else                    {y}
    }
    let x = String::from("foo");
    let y = "zoobar".to_string();
    println!("\nExplicit lifetimes:\n\tlongest = {}", longest(&x, &y))
}