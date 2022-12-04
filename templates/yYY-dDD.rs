use aoc::include_data;

const DATA: &str = include_data!("20YY", "DD");

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
mod yYY_dDD {
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
