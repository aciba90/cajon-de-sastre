#!/bin/bash

set -eux

year=${1:-22}
day=${2-00}

fn="./src/bin/y${year}-d${day}.rs"
echo "generating file: ${fn}"

cat > "${fn}" <<EOF
use aoc::include_data;

const DATA: &str = include_data!("20${year}", "${day}");

fn part1(data: &str) -> usize {
    todo!()
}

fn part2(data: &str) -> usize {
    todo!()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y${year}_d${day} {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(0usize, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(0usize, part2(DATA));
    }
}
EOF