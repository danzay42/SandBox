fn main() {
    assert_eq!(two_sum(vec![2, 7, 11, 15], 9), [0, 1]);
}

fn two_sum_sucks(nums: Vec<i32>, target: i32) -> Vec<i32> {
    for i in 0..nums.len() {
        for j in i + 1..nums.len() {
            if nums[i] + nums[j] == target {
                return vec![i as i32, j as i32];
            }
        }
    }
    vec![]
}

use std::collections::{HashMap, HashSet};

fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
    let mut set = HashMap::new();

    for i in 0..nums.len() {
        if let Some(j) = set.get(&nums[i]) {
            return vec![*j, i as i32];
        }
        set.insert(target - nums[i], i as i32);
    }
    vec![]
}
