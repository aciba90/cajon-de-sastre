use std::{collections::HashSet, fs, io};

const FILENAME: &str = "data/day01.txt";

fn main() -> io::Result<()> {
    let data = fs::read_to_string(FILENAME)?;

    println!("{:?}", part1(&data)?);
    println!("{:?}", part2(&data)?);
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
        let data = fs::read_to_string(FILENAME).unwrap();
        assert_eq!(538, part1(&data).unwrap());
    }

    #[test]
    fn test_part2() {
        let data = fs::read_to_string(FILENAME).unwrap();
        assert_eq!(77271, part2(&data).unwrap());
    }
}
