#[tokio::main]
async fn main() {
    print_int().await
}

async fn get_int_1() -> u32 {
    1
}

#[must_use] // raise warning without usage
async fn get_int_2() -> u32 {
    2
}

async fn print_int() {
    get_int_1().await;
    get_int_2().await;

    let res = get_int_2().await;
    println!("{res}")
}
