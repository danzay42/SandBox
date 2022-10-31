use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    println!("Hello, world!");
    async_function(-1).await;

    let mut handlers = vec![];

    for i in 0..10 {
        let handle = tokio::spawn(async move {
            async_function(i).await;
        });
        handlers.push(handle);
    }

    for handle in handlers {
        handle.await.unwrap();
    }
}

async fn async_function(i: i32) {
    println!("[{i}] async func inside");
    let s1 = read_from_database().await;
    println!("[{i}] First Result: {s1}");
    let s2 = read_from_database().await;
    println!("[{i}] Second Result: {s2}");
}

async fn read_from_database() -> String {
    sleep(Duration::from_millis(1000)).await;
    "DB_result".to_owned()
}

// trait Future {
//     type Output;
//     fn poll(&mut self, wakr: fn ()) -> Poll<Self::Output>;
// }

// enum Poll<T> {
//     Ready(T),
//     Pending,
// }

// fn async_function_true() -> impl Future<Output = ()> {
//     println!("async func inside")
// }
