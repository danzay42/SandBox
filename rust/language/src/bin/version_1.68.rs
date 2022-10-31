use tokio::pin as t_pin;
use std::pin::pin as s_pin;

#[tokio::main]
async fn main() {
    // 1. Cargo sparse: (defaulf since 1.70)
    // CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse
    // or Crago.toml:
    // [registries.crates-io]
    // protocol = "sparse"

    // Future trait and Pin structure
    let future = my_async_fn();
    future.await;
    // or
    let mut future = my_async_fn();
    (&mut future).await;
    // or 
    let future = my_async_fn();
    t_pin!(future);
    (&mut future).await;
    // or 
    let future = my_async_fn();
    let future = s_pin!(future);
    future.await;

    // Default alloc error handler
    let five = Box::new(5);
    let mut vec = Vec::new();
    vec.push(1);
    // std     ->   print to stderr and abort 
    // no-std  ->   panic  (#![no_std])
}

async fn my_async_fn() {
    // async logic here
}