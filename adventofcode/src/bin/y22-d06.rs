use std::collections::HashSet;

use aoc::include_data;

const DATA: &str = include_data!("2022", "06");

fn detect_start_of_packet_with_distinct_chars(msg: &str, distinct_chars: usize) -> Option<usize> {
    let mut start = distinct_chars;

    let chars: Vec<_> = msg.chars().collect();
    for batch in chars.windows(distinct_chars) {
        let mut set = HashSet::with_capacity(distinct_chars);
        for x in batch {
            if !set.insert(x) {
                // repeated element
                break;
            }
        }
        if set.len() == distinct_chars {
            return Some(start);
        }
        start += 1;
    }

    None
}

fn detect_start_of_packet_marker(msg: &str) -> Option<usize> {
    detect_start_of_packet_with_distinct_chars(msg, 4)
}

fn detect_start_of_message_marker(msg: &str) -> Option<usize> {
    detect_start_of_packet_with_distinct_chars(msg, 14)
}

fn part1(data: &str) -> usize {
    detect_start_of_packet_marker(data).expect("Result not found")
}

fn part2(data: &str) -> usize {
    detect_start_of_message_marker(data).expect("Result not found")
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
        assert_eq!(3605, part2(DATA));
    }
}
