use unicode_segmentation::UnicodeSegmentation;

fn main() {
    // initialization();
    // manipulation();
    // cancatination();
    // formating();
    // indexing();
    // indexing_iteration();

    
}

fn indexing() {
    let s1 = "🦀🦀🦀🦀🦀";
    // let s2 = s1[2];  // give second byte? not crab!!! it even doesnt work
    let s3 = &s1[0+4..4+4]; // give second crab
    
    println!("{s1} -> s2 -> {s3}");
}

fn indexing_iteration() {
    for b in "नमस्ते!".bytes() {
        print!("{b}-");
    };
    println!("नमस्ते!");
    for c in "नमस्ते!".chars() {
        print!("[  {c}  ]-");
    };
    println!("नमस्ते!");
    for cg in "नमस्ते!".graphemes(true) {
        print!("[{cg}]-");
    }
    println!("नमस्ते!");
}

fn manipulation() {
    let mut str_m = String::from("foo");
    str_m.push_str("bar");
    println!("{str_m}");

    str_m.replace_range(.., "baz");
    println!("{str_m}");
}

fn cancatination() {
    let s1 = String::from("Hello");
    let s1_copy = s1.clone();
    let s2 = String::from("World");
    let s3 = s1 + &s2;
    println!("{s3}");

    let s4 = ["first", "second"].concat();
    let s5 = format!("{}{}", "first", "second");
    let s6 = concat!("first", "second");
    let s7 = s1_copy + " WORLD!";

    println!("{s7}");
}

fn formating() {
    let s1 = "tic".to_string();
    let s3 = "tac".to_string();
    let s2 = "toe".to_string();


    let s = format!("{}-{}-{}", s1,s2,s3);
    println!("{s}");

    let s = format!("{s1}-{s2}-{s3}");
    println!("{s}");

    let s = format!("{s1}-{s2}-{}", "toe2");
    println!("{s}");
}

fn initialization() {
    // cannot manipulate data -> sort of static or constant -> use for immutable data
    let str1 = "test string 🦀";  // string slice

    // can manipulate data -> useful for mutable operation
    let str2 = String::from("test string 🦀");  // string
    let str3 = "test string 🦀".to_string();
    let str4 = "test string 🦀".to_owned();

    let str5 = &str4[..];
}
