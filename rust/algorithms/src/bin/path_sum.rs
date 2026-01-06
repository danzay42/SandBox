// Definition for a binary tree node.
#[derive(Debug, PartialEq, Eq)]
pub struct TreeNode {
    pub val: i32,
    pub left: Option<Rc<RefCell<TreeNode>>>,
    pub right: Option<Rc<RefCell<TreeNode>>>,
}

impl TreeNode {
    #[inline]
    pub fn new(val: i32) -> Self {
        TreeNode {
            val,
            left: None,
            right: None,
        }
    }
}
use std::cell::RefCell;
use std::rc::Rc;

// fn main() {
//     // let root = vec![5, 4, 8, 11, Option(None), 13, 4, 7, 2, None, None, 5, 1];
//     let output = vec![[5, 4, 11, 2], [5, 8, 4, 5]];
//     let target_sum = 22;
//     let input = Rc::new(RefCell::new(TreeNode::new(root)));
//     // assert_eq!(path_sum(root, target_sum), output);
// }

struct Solution {}
impl Solution {
    pub fn path_sum(root: Option<Rc<RefCell<TreeNode>>>, target_sum: i32) -> Vec<Vec<i32>> {
        match root {
            Some(r) => {
                let r = r.borrow();
                let new_sum = target_sum - r.val;
                let paths = [
                    Self::path_sum(r.left.clone(), new_sum),
                    Self::path_sum(r.right.clone(), new_sum),
                ]
                .concat();

                let paths = paths
                    .into_iter()
                    .filter(|p| !p.is_empty())
                    .map(|mut p| {
                        p.insert(0, r.val);
                        p
                    })
                    .collect();

                match (new_sum, r.left.is_none(), r.right.is_none()) {
                    (0, true, true) => vec![vec![r.val]],
                    _ => paths,
                }
            }
            None => vec![],
        }
    }
}

fn main() {}