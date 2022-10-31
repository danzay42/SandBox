use std::process::Command;

pub fn render(frame: Vec<Vec<i8>>, refresh: Option<bool>) {
    let image = frame
        .iter()
        .map(|vec| vec
            .iter()
            .map(|&state| if state == 1i8 {"██"} else {"  "})
            .collect::<Vec<&str>>()
            .join(""))
        .collect::<Vec<String>>()
        .join("\n");
    
    if refresh.unwrap_or_default() {
        Command::new("clear").status().unwrap();
    }

    println!("\x1b[{}A", frame.len()+1);
    println!("{}", image);
}

// pub fn render_res(frame: Vec<Vec<i32>>) {
//     let image = frame
//         .iter()
//         .map(|vec| vec
//             .iter()
//             .map(|&state| if state != 0 {state.to_string()+ " "} else {"  ".to_string()})
//             .collect::<Vec<String>>()
//             .join(""))
//         .collect::<Vec<String>>()
//         .join("\n");

//     println!("{}", image);
// }