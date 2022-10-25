use std::{collections::HashSet, fs};

fn main() {
    let data = read_data();
}

fn read_data() -> Vec<Claim> {
    fs::read_to_string("input.txt")
        .unwrap()
        .lines()
        .map(|l| Claim::parse(l))
        .collect()
}

#[derive(Debug, PartialEq, Eq)]
struct Claim {
    id: String,
    x: usize,
    y: usize,
    width: usize,
    height: usize,
}

impl Claim {
    // XXX impl FromStr
    /// Parses a str like: `#1 @ 126,902: 29x28`
    fn parse(data: &str) -> Self {
        let (id, data) = data.split_once(" @ ").unwrap();
        let id = (&id[1..]).to_string();

        let (xy, wh) = data.split_once(": ").unwrap();

        let (x, y) = xy.split_once(',').unwrap();
        let x = x.parse().unwrap();
        let y = y.parse().unwrap();

        let (width, height) = wh.split_once('x').unwrap();
        let width = width.parse().unwrap();
        let height = height.parse().unwrap();

        Claim {
            id,
            x,
            y,
            width,
            height,
        }
    }
}

fn collect_overlapping_coords(claims: &[Claim]) -> HashSet<(usize, usize)> {
    let overlapping = HashSet::new();
    todo!();
    overlapping
}

#[test]
fn parse_claim() {
    assert_eq!(
        Claim::parse("#1 @ 126,902: 29x28"),
        Claim {
            id: "1".to_string(),
            x: 126,
            y: 902,
            width: 29,
            height: 28
        }
    )
}
