use std::collections::{HashMap, HashSet};

fn main() {}

fn contains_duplicate(nums: Vec<i32>) -> bool {
    let mut set = HashSet::new();

    for num in nums {
        if set.contains(&num) {
            return true;
        }
        set.insert(num);
    }
    return false;
}

pub fn is_anagram1(s: String, t: String) -> bool {
    if s.len() != t.len() {
        return false;
    }

    let mut sc = HashMap::with_capacity(s.len());
    let mut tc = HashMap::with_capacity(t.len());

    s.chars().for_each(|c| *sc.entry(c).or_insert(0) += 1);
    t.chars().for_each(|c| *tc.entry(c).or_insert(0) += 1);

    sc == tc
}

fn is_anagram(s: String, t: String) -> bool {
    if s.len() != t.len() {
        return false;
    }

    let mut c = HashMap::new();

    for (sc, tc) in s.chars().zip(t.chars()) {
        *c.entry(sc).or_insert(0) += 1;
        *c.entry(tc).or_insert(0) -= 1;
    }
    c.into_values().all(|x| x == 0)
}

pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
    let mut sums: HashMap<i32, usize> = HashMap::new();

    for (i, &num) in nums.iter().enumerate() {
        match sums.get(&(target - num)) {
            Some(&j) => return vec![i as i32, j as i32],
            None => { sums.insert(num, i); }
        }
    }
    return vec![];
}


pub fn group_anagrams(strs: Vec<String>) -> Vec<Vec<String>> {
    let mut groups = std::collections::HashMap::new();
    for s in strs {
        let mut freq = [0u8; 26];
        for c in s.bytes() {
            freq[(c - b'a') as usize] += 1;
        }
        groups.entry(freq).or_insert(Vec::new()).push(s)
    }
    groups.into_values().collect()

    // strs.into_iter().fold(HashMap::<[u8; 26], Vec<String>>::new(), |mut map, s| {
    //     let freqs = s.bytes().map(|b| (b - b'a') as usize).fold([0; 26], |mut freqs, bin| {
    //         freqs[bin] += 1;
    //         freqs
    //     });
    //     map.entry(freqs).or_default().push(s);
    //     map
    // }).into_values().collect()
}