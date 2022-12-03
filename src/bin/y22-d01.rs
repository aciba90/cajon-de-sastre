use aoc::locate_data;

const DATA: &str = include_str!(locate_data!("2022", "01"));

fn part1(data: &str) -> usize {
    data.split("\n\n")
        .map(|elf| {
            elf.split('\n')
                .map(|calorie| calorie.parse::<usize>().unwrap_or_default())
                .sum::<usize>()
        })
        .max()
        .unwrap()
}

fn part2(data: &str) -> usize {
    let mut calories: Vec<_> = data
        .split("\n\n")
        .map(|elf| {
            elf.split('\n')
                .map(|calorie| calorie.parse::<usize>().unwrap_or_default())
                .sum::<usize>()
        })
        .collect();
    calories.sort();

    calories.iter().rev().take(3).sum::<usize>()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d01 {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(69795usize, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(208437usize, part2(DATA));
    }
}
