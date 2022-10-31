
#[allow(unused)]
fn main() {
    println!("Hello, world!");

    let range1: i32 = (1i32..=10).sum();
    let range2: i32 = (10i32..10).sum();
    println!("r1 = {:?}\nr2 = {:?}", range1, range2);

    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest_i32(&number_list);
    println!("The largest number is {}", result);

    let number_list = vec![102, 34, 6000, 89, 54, 2, 43, 8];

    let result = largest_i32(&number_list);
    println!("The largest number is {}", result);

    println!("This is block of code, {}", {
        let a = 1;
        let b = 3;
        a + b
    });
    println!("The largest number is {} from block of code", largest_i32({
        let mut origin_vector = vec![-3, 0, 3, 10];
        origin_vector.push(42);
        &origin_vector.clone()
    }));

    struct Point<T1, T2> {
        x: T1,
        y: T2,
    }
    {
        let both_integer = Point { x: 5, y: 10 };
        let both_float = Point { x: 1.0, y: 4.0 };
        let integer_and_float = Point { x: 5, y: 4.0 };
    }

    let number_list = vec![34, 50, 25, 100, 65];

    let result = largest(&number_list);
    println!("The largest number is {}", result);

    let char_list = vec!['y', 'm', 'a', 'q'];

    let result = largest(&char_list);
    println!("The largest char is {}", result);

    struct ImportantExcerpt<'a> {
        part: &'a str,
    }

    unsafe_main();

}

fn largest_i32(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn unsafe_main() {
     
    let mut num = 5;
 
    let n1 = &num as *const i32;
    let n2 = &mut num as *mut i32;
     
    println!("n1={:p}", n1);
    println!("n2={:p}", n2);

//     let addr = 0x38b50ff4usize;
//     let p = addr as *const i32;
//     println!("Address: {:p}", p);
}

fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

#[allow(unused)]
mod parent_module {
    pub mod child_module {
        pub fn test() {
            super::hello(); // обращаемся к функции из родительского модуля
        }
    }
    fn hello() {
        println!("Hello");
    }
}
