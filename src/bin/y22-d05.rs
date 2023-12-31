use std::str::FromStr;

use aoc::include_data;

const DATA: &str = include_data!("2022", "05");

struct Step {
    n: usize,
    source: usize,
    target: usize,
}

impl FromStr for Step {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // parses a line containing: `move 2 from 6 to 4`
        let re = regex::Regex::new(r"^move (\d+) from (\d+) to (\d+)$").unwrap();
        let caps = re.captures(s).unwrap();

        let n = caps.get(1).unwrap().as_str().parse().unwrap();
        let source = caps.get(2).unwrap().as_str().parse().unwrap();
        let target = caps.get(3).unwrap().as_str().parse().unwrap();

        Ok(Self { n, source, target })
    }
}

fn read_data(input: &str) -> Vec<Step> {
    input
        .lines()
        .filter(|line| !line.starts_with('#'))
        .map(|line| line.parse().expect("valid step"))
        .collect()
}

struct Ship {
    stacks: Vec<String>,
}

impl Ship {
    pub fn from_vec(v: Vec<String>) -> Self {
        Self { stacks: v }
    }

    fn r#move(&mut self, quantity: usize, from: usize, to: usize, reversed: bool) {
        debug_assert!(from != 0 && to != 0);
        let mut crate_mover = Vec::with_capacity(quantity);

        for _ in 0..quantity {
            let crate_ = self.stacks[from - 1]
                .pop()
                .expect("not enough crates to move");
            crate_mover.push(crate_)
        }
        if reversed {
            crate_mover.reverse();
        }
        self.stacks[to - 1].extend(crate_mover);
    }

    fn move9000(&mut self, quantity: usize, from: usize, to: usize) {
        self.r#move(quantity, from, to, false)
    }

    fn move9001(&mut self, quantity: usize, from: usize, to: usize) {
        self.r#move(quantity, from, to, true)
    }

    pub fn crates_on_top(&self) -> String {
        self.stacks
            .iter()
            .map(|s| s.chars().last().expect("not enough chars"))
            .collect()
    }
}

fn part1(data: &str) -> String {
    let v = vec![
        String::from("HRBDZFLS"),
        String::from("TBMZR"),
        String::from("ZLCHNS"),
        String::from("SCFJ"),
        String::from("PGHWRZB"),
        String::from("VJZGDNMT"),
        String::from("GLNWFSPQ"),
        String::from("MZR"),
        String::from("MCLGVRT"),
    ];
    let mut ship = Ship::from_vec(v);
    let steps = read_data(data);
    for step in steps.into_iter() {
        ship.move9000(step.n, step.source, step.target);
    }
    ship.crates_on_top()
}

fn part2(data: &str) -> String {
    let v = vec![
        String::from("HRBDZFLS"),
        String::from("TBMZR"),
        String::from("ZLCHNS"),
        String::from("SCFJ"),
        String::from("PGHWRZB"),
        String::from("VJZGDNMT"),
        String::from("GLNWFSPQ"),
        String::from("MZR"),
        String::from("MCLGVRT"),
    ];
    let mut ship = Ship::from_vec(v);
    let steps = read_data(data);
    for step in steps.into_iter() {
        ship.move9001(step.n, step.source, step.target);
    }
    ship.crates_on_top()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d05 {
    use super::*;

    #[test]
    fn test_step_parsing() {
        let step: Step = "move 2 from 6 to 4".parse().unwrap();
        assert_eq!(step.n, 2);
        assert_eq!(step.source, 6);
        assert_eq!(step.target, 4);
    }

    #[test]
    fn example1() {
        let data = r#"move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"#;
        let v = vec![String::from("ZN"), String::from("MCD"), String::from("P")];
        let mut ship = Ship::from_vec(v);
        let steps = read_data(data);
        for step in steps.into_iter() {
            ship.move9000(step.n, step.source, step.target);
        }
        assert_eq!(ship.crates_on_top(), "CMZ");
    }

    #[test]
    fn test_part1() {
        assert_eq!("RNZLFZSJH", part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!("CNSFCGJSM", part2(DATA));
    }
}
