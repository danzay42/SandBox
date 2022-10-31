use std::{
    fs, io, num,
    str::{self, FromStr},
};

fn main() {
    // 1. Unnecessary indirection
    let s = "some str".to_owned();
    fancy_print(&s);
    let s = "some str";
    fancy_print(s);

    // 2. Overusing slice indexing
    // indexing();

    // 3. Using sentinel values (values with special meaning: -1, "", null)
    get_username(1);

    // 4. Not using enums
    can_publish_blog(Role::Admin);

    // 5. Error handling
    assert_eq!(Ok(4), parse_then_add("2", "2"));
    assert!(parse_then_add("5", "a1").is_err());

    // 6. Standard library traits
    let p1 = Player::default();
    let p2 = Player {
        level: 0,
        items: vec![],
        special_power: None,
    };
    println!("p1 = {p1:?}, p2 = {p2:?}");
    open_and_parse_file("Ccargo.toml");
    let p2 = Point::from_str("(1,2)");
    assert_eq!(p2.unwrap(), Point { x: 1, y: 2 });

    // 7. Standart library macros
    // todo! macro
    // let s = MyDb;
    // s.connect("Database URL");
    // s.query()
    // concat! macro
    let s = concat!("test", 10, 'b', true);
    assert_eq!(s, "test10btrue");
    let s1 = "hello".to_owned();
    let s2 = "world";
    let s3 = format!("{} {}", s1, s2);
    assert_eq!(s3, "hello world".to_owned());

    // 8. Use tools
    // cargo fmt -> format code 
    // cargo clippy - rust linter
}

// fn fancy_print(s: &String) {  // wrong
fn fancy_print(s: &str) {
    println!("*******************");
    println!("{s}");
    println!("*******************");
}

// fn indexing() {
//     let points: Vec<Coordinate> = ...;
//     let mut differences = Vec::new();
//     // // wrong solution
//     // for i in 1..points.len() {
//     //     let curr = points[i];
//     //     let prev = points[i-1];
//     //     differences.push(curr - prev)
//     // }
//     // one way
//     for [prev, curr] in points.array_windows().copied() {
//         differences.push(curr - prev)
//     }
//     // another way
//     let differences: Vec<_> = points
//         .array_windows()
//         .copied()
//         .map(|[prev, curr]| curr-prev)
//         .collect();
// }

// // wrong
// fn get_username(id: i32) -> String {
//     if id == 1 {
//         return "rust_user_123".to_owned();
//     }
//     "".to_owned()
// }
fn get_username(id: i32) -> Option<String> {
    if id == 1 {
        return Some("rust_user_123".to_owned());
    }
    None
}

// // bad solution
// fn can_publish_blog(role: String) -> bool {
//     if role == "Admin" || role == "Writer" {
//         return true;
//     }
//     false
// }
enum Role {
    Admin,
    Reader,
    Writer,
}
fn can_publish_blog(role: Role) -> bool {
    match role {
        Role::Admin | Role::Writer => true,
        _ => false,
    }
}

fn parse_then_add(a: &str, b: &str) -> Result<i32, num::ParseIntError> {
    // // wrong
    // let a = a.parse::<i32>();
    // if let Err(e) = a {
    //     return Err(e);
    // }
    // let b = b.parse::<i32>();
    // if let Err(e) = b {
    //     return Err(e);
    // }
    // Ok(a.unwrap() + b.unwrap())

    let a: i32 = a.parse()?;
    let b: i32 = b.parse()?;
    Ok(a + b)
}

#[derive(Debug, Default)]
struct Player {
    level: i8,
    items: Vec<i32>,
    special_power: Option<String>,
}

enum CliError {
    IOError(io::Error),
    ParseError(num::ParseIntError),
}
impl From<io::Error> for CliError {
    fn from(value: io::Error) -> Self {
        CliError::IOError(value)
    }
}
impl From<num::ParseIntError> for CliError {
    fn from(value: num::ParseIntError) -> Self {
        CliError::ParseError(value)
    }
}
fn open_and_parse_file(file_name: &str) -> Result<i32, CliError> {
    let mut contents = fs::read_to_string(&file_name)?;
    let num: i32 = contents.trim().parse()?;
    Ok(num)
}

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}
impl str::FromStr for Point {
    type Err = num::ParseIntError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let coords: Vec<&str> = s
            .trim_matches(|p| p == '(' || p == ')')
            .split(",")
            .collect();
        let x_fromstr = coords[0].parse::<i32>()?;
        let y_fromstr = coords[1].parse::<i32>()?;
        Ok(Point {
            x: x_fromstr,
            y: y_fromstr,
        })
    }
}

struct MyDb;
// impl Database for MyDb {
//     fn connect(&self, url: &str) {
//         // ...
//     }
//     fn query(&self) -> QueryResult {
//         todo!()
//     }
// }
