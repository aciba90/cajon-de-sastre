use std::{collections::HashSet, io};

const DATA: &str = aoc::include_data!("2018", "01");

fn main() -> io::Result<()> {
    println!("{:?}", part1(DATA)?);
    println!("{:?}", part2(DATA)?);
    Ok(())
}

fn part1(data: &str) -> io::Result<i128> {
    let result: i128 = data.lines().map(|line| line.parse::<i128>().unwrap()).sum();

    Ok(result)
}

fn part2(data: &str) -> io::Result<i128> {
    let mut seen = HashSet::<i128>::new();
    let mut freq = 0_i128;

    loop {
        for change in data.lines().map(|line| line.parse::<i128>().unwrap()) {
            freq += change;
            if seen.contains(&freq) {
                return Ok(freq);
            }
            seen.insert(freq);
        }
    }
}

#[cfg(test)]
mod day01 {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(538, part1(DATA).unwrap());
    }

    #[test]
    fn test_part2() {
        assert_eq!(77271, part2(DATA).unwrap());
    }
}
