use anyhow::{anyhow, Context};
use aoc::locate_data;
use std::{collections::HashSet, str::FromStr};

const INPUT: &str = include_str!(locate_data!("2018", "03"));

fn main() -> anyhow::Result<()> {
    println!("Result: {}", part1()?);

    Ok(())
}

fn part1() -> anyhow::Result<usize> {
    let data = read_data().with_context(|| "Reading data")?;
    Ok(collect_overlapping_coords(&data).len())
}

type Coord = (usize, usize);

#[derive(Debug, PartialEq, Eq)]
struct Claim {
    id: String,
    x: usize,
    y: usize,
    width: usize,
    height: usize,
}

impl Claim {
    pub fn contains(&self, coord: &Coord) -> bool {
        let (x, y) = coord;
        if *x < self.x {
            return false;
        }
        if *y < self.y {
            return false;
        }
        if *x >= self.x + self.width {
            return false;
        }
        if *y >= self.y + self.height {
            return false;
        }
        true
    }

    pub fn corner_down_left(&self) -> Coord {
        (self.x, self.y)
    }

    pub fn corner_up_right(&self) -> Coord {
        (self.x + self.width, self.y + self.height)
    }
}

/// Parses a str like: `#1 @ 126,902: 29x28`
impl FromStr for Claim {
    type Err = anyhow::Error;

    fn from_str(data: &str) -> Result<Self, Self::Err> {
        let (id, data) = data
            .split_once(" @ ")
            .ok_or_else(|| anyhow!("Invalid format in {}", &data))?;
        let id = id[1..].to_string();

        let (xy, wh) = data
            .split_once(": ")
            .ok_or_else(|| anyhow!("Invalid format in {}", &data))?;

        let (x, y) = xy
            .split_once(',')
            .ok_or_else(|| anyhow!("Invalid format in {}", &data))?;
        let x = x.parse()?;
        let y = y.parse()?;

        let (width, height) = wh
            .split_once('x')
            .ok_or_else(|| anyhow!("Invalid format in {}", &data))?;
        let width = width.parse()?;
        let height = height.parse()?;

        Ok(Claim {
            id,
            x,
            y,
            width,
            height,
        })
    }
}

fn read_data() -> anyhow::Result<Vec<Claim>> {
    INPUT.to_string().lines().map(|l| l.parse()).collect()
}

fn collect_overlapping_coords(claims: &[Claim]) -> HashSet<Coord> {
    let mut overlapping = HashSet::new();

    if claims.is_empty() {
        return overlapping;
    }

    let mut global_corner_down_left = claims[0].corner_down_left();
    let mut global_corner_up_right = claims[0].corner_up_right();
    for claim in &claims[1..] {
        let corner_down = claim.corner_down_left();
        if corner_down.0 < global_corner_down_left.0 {
            global_corner_down_left.0 = corner_down.0;
        }
        if corner_down.1 < global_corner_down_left.1 {
            global_corner_down_left.1 = corner_down.1;
        }
        let corner_up = claim.corner_up_right();
        if corner_up.0 > global_corner_up_right.0 {
            global_corner_up_right.0 = corner_up.0;
        }
        if corner_up.1 > global_corner_up_right.1 {
            global_corner_up_right.1 = corner_up.1;
        }
    }

    for j in global_corner_down_left.1..=global_corner_up_right.1 {
        for i in global_corner_down_left.0..=global_corner_up_right.0 {
            let mut count = 0;
            let cur_coord = (i, j);
            for claim in claims {
                if claim.contains(&cur_coord) {
                    count += 1;
                }
                if count > 1 {
                    overlapping.insert(cur_coord);
                    break;
                }
            }
        }
    }

    overlapping
}

#[cfg(test)]
mod day03 {
    use super::*;

    #[test]
    fn parse_claim() {
        assert_eq!(
            Claim::from_str("#1 @ 126,902: 29x28").unwrap(),
            Claim {
                id: "1".to_string(),
                x: 126,
                y: 902,
                width: 29,
                height: 28
            }
        )
    }

    #[test]
    fn claim_contains() {
        let claim = Claim {
            id: "1".to_string(),
            x: 0,
            y: 0,
            width: 1,
            height: 1,
        };
        for (coord, contained) in [((0, 0), true), ((1, 1), false)] {
            assert_eq!(claim.contains(&coord), contained);
        }
    }

    #[test]
    fn test_collect_overlapping_coords() {
        let claim_0 = Claim {
            id: "1".to_string(),
            x: 0,
            y: 0,
            width: 1,
            height: 1,
        };
        let claim_1 = Claim {
            id: "0".to_string(),
            x: 0,
            y: 0,
            width: 2,
            height: 2,
        };
        let claims = vec![claim_0, claim_1];
        let overlapping_coords = collect_overlapping_coords(&claims);
        let mut expected_coords = HashSet::new();
        expected_coords.insert((0, 0));

        assert_eq!(overlapping_coords, expected_coords);
    }

    #[ignore] // XXX: very slow
    #[test]
    fn test_part1() {
        assert_eq!(part1().unwrap(), 118858);
    }
}
