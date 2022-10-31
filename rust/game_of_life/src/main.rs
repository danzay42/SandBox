use std::fs;
use std::io::{Result, Read, BufReader};
use std::{thread, time};

use serde_json;
mod core;
mod cli_display;

fn main() -> Result<()> {
    let example_frame = get_first_frame_from_file("../../patterns_examples.json")?;
    for new_frame in core::FrameGenerator::new(example_frame, None, None)  {
        cli_display::render(new_frame, Some(false));
        thread::sleep(time::Duration::from_millis(200));
    }
    Ok(())
}

fn get_first_frame_from_file(file_name: &str) -> Result<core::Frame> {
    let file = fs::File::open(file_name)?;
    let mut data_io = BufReader::new(file);

    let mut data = String::new();
    data_io.read_to_string(&mut data)?;
    let mut json_data: serde_json::Value = serde_json::from_str(&data)?;
    
    let example_frame: core::Frame = json_data["Oscillators"]["Penta-decathlon"]
    // let example_frame: core::Frame = json_data["Oscillators"]["Pulsar"]
        .as_array_mut()
        .unwrap()
        .iter_mut()
        .map(|vec| vec
            .as_array_mut()
            .unwrap()
            .iter()
            .map(|value| value.as_i64().unwrap() as i8)
            .collect())
        .collect();
    
    Ok(example_frame)
}