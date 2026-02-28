// #[derive(PartialEq, Eq, Clone, Debug)]
// pub struct ListNode {
//     pub val: i32,
//     pub next: Option<Box<ListNode>>,
// }
//
// impl ListNode {
//     #[inline]
//     fn new(val: i32) -> Self {
//         ListNode { next: None, val }
//     }
// }
//
// impl Solution {
//     pub fn partition(mut head: Option<Box<ListNode>>, x: i32) -> Option<Box<ListNode>> {
//         let mut below_head = ListNode::new(0);
//         let mut below_tail = &mut below_head;
//         let mut above_head = ListNode::new(0);
//         let mut above_tail = &mut above_head;
//
//         while let Some(mut node) = head {
//             head = node.next.take();
//             if node.val < x {
//                 below_tail.next = Some(node);
//                 below_tail = below_tail.next.as_mut().unwrap();
//             } else {
//                 above_tail.next = Some(node);
//                 above_tail = above_tail.next.as_mut().unwrap();
//             }
//         }
//
//         below_tail.next = above_head.next.take();
//         above_tail.next = None;
//
//         below_head.next
//     }
// }

use std::error::Error;
use std::string::ParseError;

fn main() -> Result<(), Box<dyn Error>> {
    let result = "a".parse::<i32>().map_err(|e| { Err("err1").into::<dyn Error>() })? + "13".parse::<i32>()?;
    println!("result: {}", result);
    Ok(())
}
