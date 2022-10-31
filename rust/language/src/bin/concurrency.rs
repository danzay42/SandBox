use std::sync::mpsc;
use std::time::Duration;
use std::{thread, vec};

fn main() {
    println!("Hello, world!");
    // example_1();
    // example_2();
    example_3();
}

fn example_3() {
    let (tx, rx) = mpsc::channel();
    let tx_2 = tx.clone();

    thread::spawn(move || {
        let vals = vec![
            String::from("[orig] hi"),
            String::from("[orig] from"),
            String::from("[orig] the"),
            String::from("[orig] thread"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        let vals = vec![
            String::from("[clone] hi"),
            String::from("[clone] from"),
            String::from("[clone] the"),
            String::from("[clone] thread"),
        ];

        for val in vals {
            tx_2.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {received}");
    }
}

fn example_2() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {received}");
    }
}

fn example_1() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let msg = String::from("test message....");

        tx.send(msg).unwrap();
    });

    let received = rx.recv().unwrap();
    println!("Got: {}", received);
}
