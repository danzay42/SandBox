# Docs
- [rust-lang](https://www.rust-lang.org/learn)

## CheatSheets
- [quickref](https://quickref.me/rust)
- [cheats](https://cheats.rs/)
- [infinyon](https://www.infinyon.com/resources/files/rust_cheat_sheet.pdf)
- [mem containers](https://github.com/usagi/rust-memory-container-cs)

# Develop Tools
- [irust](https://github.com/sigmaSd/IRust)
- [Evcxr](https://github.com/evcxr/evcxr)
- [cargo-info](https://gitlab.com/imp/cargo-info)

# Crates
- [serde](https://crates.io/crates/serde): Serde is a framework for serializing and deserializing Rust data structures efficiently and generically.
- [serde_json](https://crates.io/crates/serde_json)
- [anyhow](https://crates.io/crates/anyhow): This library provides anyhow::Error, a trait object based error type for easy idiomatic error handling in Rust applications.
- [thiserror](https://crates.io/crates/thiserror): This library provides a convenient derive macro for the standard library's std::error::Error trait.
- [tokio](https://crates.io/crates/tokio): A runtime for writing reliable, asynchronous, and slim applications with the Rust programming language.
- [log](https://crates.io/crates/log): A Rust library providing a lightweight logging facade.
- [env_logger](https://crates.io/crates/env_logger): Implements a logger that can be configured via environment variables.
- [pretty_env_logger](https://crates.io/crates/pretty_env_logger): A simple logger built on top off env_logger. It is configured via an environment variable and writes to standard error with nice colored output for log levels.
- [tracing](https://crates.io/crates/tracing): Application-level tracing for Rust.
- [chrono](https://crates.io/crates/chrono): Date and Time for Rust.
- [structopt](https://crates.io/crates/structopt): Parse command line arguments by defining a struct. It combines clap with custom derive.
- [egui](https://crates.io/crates/egui): Egui (pronounced "e-gooey") is a simple, fast, and highly portable immediate mode GUI library for Rust. egui runs on the web, natively, and in your favorite game engine (or will soon).

## UI
### desktop
- [slint](https://slint.dev/)
- [tauri](https://tauri.app/)
### web 
- [yew](https://yew.rs/)

## Web
- [Rocket](https://rocket.rs/)

## DB
- [surrealdb](https://surrealdb.com/)
### Database Drivers
- postgres: A native, synchronous PostgreSQL client.
- postgres + tokio: An asinc PostgreSQL client.
- sled: Lightweigt high-performance pure-rust transactional embedded database.
- sqlx: The Rust SQL Toolkit. An async, pure Rust SQL crate featuring compile-time checked queries without DSL. Supports PostgreSQL, MySQL, SQLite.
### ORM
- diesel: A safe, sync, extendable ORM and Query Builder for PostgreSQL, SQLite, and MySQL.
- sea-orm: An async and dynamic ORM.
- seq-query: A dynamic query builder for MySQL, PostgreSQL, and SQLite.
### Connection Pool
- r2d2: A generic connection pool.
