use std::collections::HashSet;

use aoc::include_data;

const DATA: &str = include_data!("2022", "06");

fn detect_start_of_packet_marker(msg: &str) -> Option<usize> {
    let mut start = 4;

    let chars: Vec<_> = msg.chars().collect();
    for batch in chars.windows(4) {
        let mut set = HashSet::with_capacity(4);
        for x in batch {
            if !set.insert(x) {
                // repeated element
                break;
            }
        }
        if set.len() == 4 {
            return Some(start);
        }
        start += 1;
    }

    None
}

fn part1(data: &str) -> usize {
    detect_start_of_packet_marker(data).expect("Result not found")
}

fn part2(data: &str) -> usize {
    todo!()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d06 {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(1275, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(0usize, part2(DATA));
    }
}
