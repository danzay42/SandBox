use std::collections::HashSet;

macro_rules! nothing_burger {
    () => {
        println!("nothing burger")
    };
    ("ferris") => {
        println!("nothing ferris")
    };
}

macro_rules! hello {
    // $name:type
    ($s:literal) => {
        println!("Hi(l), {}", $s)
    };
    ($s:ident) => {
        println!("Hi(i), {}", $s)
    };
    ($s:expr) => {
        println!("Hi(e), {}", $s)
    };
}

macro_rules! dict {
    ($($s:expr),+) => {HashSet::from([$($s),*])}
}

fn main() {
    nothing_burger!();
    nothing_burger!("ferris");
    // nothing_burger!(1);  // error: no rule '1'
    hello!("foo");
    hello!("bar");
    let Foo = "Foo";
    hello!(Foo);
    let set1 = HashSet::from([1, 2, 3, 4]);
    let set2 = dict!(1, 2, 3, 4);
    dbg!(set1);
    dbg!(set2);
}
