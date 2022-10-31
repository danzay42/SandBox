use std::collections;

pub type Frame = Vec<Vec<i8>>;
type FrameR = Vec<Vec<i32>>;



fn new_cell(state: i8, resources: i32) -> i8 {
    match (state, resources) {
        (1, 2) => 1,
        (_, 3) => 1,
        _ => 0,
    }
}

fn new_frame(old_frame: &Frame, resource_distribution: FrameR) -> Frame {
    old_frame.iter().enumerate()
        .map(|(y, row)| row.iter().enumerate()
            .map(|(x, &state)|
                new_cell(state, resource_distribution[y][x]))
            .collect())
        .collect()
}

fn calculate_resources(frame: &Frame) -> FrameR {
    let mut resources_buffer:FrameR = frame
        .iter()
        .map(|row| vec![0i32; row.len()])
        .collect();

    for (y, row) in frame.iter().enumerate() {
        for (x, _) in row.iter().enumerate().filter(|(_, state)| **state == 1) {
            for dy in [-1, 0, 1] {
                for dx in [-1, 0, 1] {
                    if dx != 0 || dy != 0 {
                        let sx = match x as i32 + dx {
                            -1 => row.len()-1,
                            etc if etc == row.len() as i32 => 0,
                            etc => etc as usize,
                        };
                        let sy = match y as i32 + dy {
                            -1 => frame.len()-1,
                            etc if etc == frame.len() as i32 => 0,
                            etc => etc as usize,
                        };
                        resources_buffer[sy][sx] += 1;
                    }
                }
            }
        }
    }
    resources_buffer
}

pub struct FrameGenerator {
    buffer: collections::VecDeque<Frame>,
    buffer_size_max: usize,
    count: i32,
}

impl FrameGenerator {
    pub fn new(init_frame: Frame, count: Option<i32>, buffered_frames_size: Option<usize>) -> FrameGenerator {
        FrameGenerator {
            buffer: collections::VecDeque::from([init_frame]),
            buffer_size_max: buffered_frames_size.unwrap_or(3),
            count: count.unwrap_or(-1),
        }
    }

    fn loop_control(&mut self, frame: &Frame) {
        if self.buffer.len() > self.buffer_size_max {
            self.buffer.pop_back();
        }
        self.count = if self.buffer.contains(&frame) {println!("looped"); 0}
         else if self.count == -1 {-1}
          else {self.count-1};
        self.buffer.push_front(frame.clone());
    }  
}

impl Iterator for FrameGenerator {
    type Item = Frame;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count > 0 || self.count == -1 {
            let last_frame = self.buffer.get(0).unwrap().clone(); 
            let resource_distribution = calculate_resources(&last_frame);
            let new_frame = new_frame(&last_frame, resource_distribution);
            self.loop_control(&new_frame);
            Some(last_frame)
        }
        else {
            None
        }
    }
}