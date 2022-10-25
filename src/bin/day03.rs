use anyhow::{anyhow, Context};
use std::{collections::HashSet, fs, str::FromStr};

const INPUT: &str = include_str!("../../data/day03.txt");

fn main() -> anyhow::Result<()> {
    let data = read_data().with_context(|| format!("asdf"))?;
    let x = collect_overlapping_coords(&data);

    Ok(())
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
    fn contains(&self, coord: &Coord) -> bool {
        todo!();
    }
}

/// Parses a str like: `#1 @ 126,902: 29x28`
impl FromStr for Claim {
    type Err = anyhow::Error;

    fn from_str(data: &str) -> Result<Self, Self::Err> {
        let (id, data) = data
            .split_once(" @ ")
            .ok_or(anyhow!("Invalid format in {}", &data))?;
        let id = (&id[1..]).to_string();

        let (xy, wh) = data
            .split_once(": ")
            .ok_or(anyhow!("Invalid format in {}", &data))?;

        let (x, y) = xy
            .split_once(',')
            .ok_or(anyhow!("Invalid format in {}", &data))?;
        let x = x.parse()?;
        let y = y.parse()?;

        let (width, height) = wh
            .split_once('x')
            .ok_or(anyhow!("Invalid format in {}", &data))?;
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
    let overlapping = HashSet::new();

    todo!();
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
}
