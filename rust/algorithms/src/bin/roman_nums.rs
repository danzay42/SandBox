fn main() {
    let roman = "MCMXCIV".to_string();
    let val = roman_to_int(roman.clone());
    println!("{roman} = {val}");
    let roman = int_to_roman(val);
    println!("{val} = {roman}");
}

fn roman_to_int(s: String) -> i32 {
    let mut res = 0;
    let mut last = 1;
    for ch in s.chars().rev() {
        let num = match ch {
            'I' => 1,
            'V' => 5,
            'X' => 10,
            'L' => 50,
            'C' => 100,
            'D' => 500,
            'M' => 1000,
            _ => 0,
        };
        res += if num >= last {
            last = num;
            num
        } else {
            -num
        };
    }
    res
}

fn int_to_roman(num: i32) -> String {
    let mut num = num.clone();
    let mut res = "".to_string();

    for (ch, ch_5, base, next) in [
        ("M", "", 1000, ""),
        ("C", "D", 100, "CM"),
        ("X", "L", 10, "XC"),
        ("I", "V", 1, "IX"),
    ] {
        let c = (num / base) as usize;
        let res_oreder = match c {
            0 => continue,
            1..=3 => ch.repeat(c),
            4 => ch.to_string() + &ch_5.to_string(),
            5..=8 => ch_5.to_string() + &ch.repeat(c - 5),
            9 => next.to_string(),
            _ => ch.repeat(c),
        };
        res.push_str(&res_oreder);
        num %= base;
    }
    format!("{res}")
}
