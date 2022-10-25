use std::{collections::HashMap, fs};

fn main() {
    let data = read_input();
    println!("{}", part1(&data));
    println!("{}", part2(&data).unwrap());
}

fn read_input() -> String {
    fs::read_to_string("data/day02.txt").unwrap()
}

fn part1(data: &str) -> i32 {
    let mut repeated_2 = 0;
    let mut repeated_3 = 0;
    for line in data.lines() {
        if has_repeated(line, 2) {
            repeated_2 += 1;
        }
        if has_repeated(line, 3) {
            repeated_3 += 1;
        }
    }

    repeated_2 * repeated_3
}

/// Determines if `word` contains a char repeated exactly `n` times
fn has_repeated(word: &str, n: i32) -> bool {
    let mut counter = HashMap::new();

    for c in word.chars() {
        let count = counter.entry(c).or_insert(0);
        *count += 1;
    }

    counter.values().any(|&count| count == n)
}

fn part2(data: &str) -> Option<String> {
    for w1 in data.lines() {
        for w2 in data.lines() {
            if w1 == w2 {
                continue;
            }
            if !differ_in_one_char(w1, w2) {
                continue;
            }
            let mut common = String::with_capacity(w1.len());
            for (c1, c2) in w1.chars().zip(w2.chars()) {
                if c1 == c2 {
                    common.push(c1);
                }
            }
            return Some(common);
        }
    }
    None
}

// Determines if two words has only one char different
fn differ_in_one_char(a: &str, b: &str) -> bool {
    assert_eq!(a.len(), b.len(), "a and b must have same length.");

    let mut n_diffs = 0_usize;
    for (ac, bc) in a.chars().zip(b.chars()) {
        if ac == bc {
            continue;
        }
        n_diffs += 1;
        if n_diffs > 1 {
            return false;
        }
    }
    n_diffs == 1
}

#[test]
fn test_part1() {
    assert_eq!(4920, part1(&read_input()));
}

#[test]
fn test_part2() {
    assert_eq!(
        Some("fonbwmjquwtapeyzikghtvdxl".to_string()),
        part2(&read_input())
    );
}
