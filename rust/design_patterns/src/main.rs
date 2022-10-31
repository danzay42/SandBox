fn main() {
    println!("Hello, world!");
    let test = vec![1,2,3,4,5];
    let test = &test[1..4];
    println!("{test:#?}")
}
