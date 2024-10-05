use aoc::include_data;

#[derive(Debug, PartialEq, Eq)]
struct Section(usize, usize);

impl Section {
    #[allow(dead_code)]
    fn new(start: usize, end: usize) -> Self {
        Self(start, end)
    }

    fn intersects(&self, other: &Self) -> bool {
        (other.0 <= self.0 && self.0 <= other.1) || (self.0 <= other.0 && other.0 <= self.1)
    }

    fn is_contained_in(&self, other: &Section) -> bool {
        other.0 <= self.0 && self.1 <= other.1
    }
}

#[derive(Debug, PartialEq, Eq)]
struct UnknownParsingError;

impl TryFrom<&str> for Section {
    type Error = UnknownParsingError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value.split_once('-') {
            Some((start, end)) => {
                let start: usize = match start.parse() {
                    Ok(x) => x,
                    Err(_) => return Err(UnknownParsingError),
                };
                let end: usize = match end.parse() {
                    Ok(x) => x,
                    Err(_) => return Err(UnknownParsingError),
                };
                Ok(Section(start, end))
            }
            None => Err(UnknownParsingError),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct AssigmentPair(Section, Section);

impl AssigmentPair {
    fn new(section_0: Section, section_1: Section) -> Self {
        Self(section_0, section_1)
    }

    fn full_overlap(&self) -> bool {
        self.0.is_contained_in(&self.1) || self.1.is_contained_in(&self.0)
    }

    fn partial_overlap(&self) -> bool {
        self.0.intersects(&self.1)
    }
}

impl TryFrom<&str> for AssigmentPair {
    type Error = UnknownParsingError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value.split_once(',') {
            Some((sec_0, sec_1)) => {
                let sec_0 = match Section::try_from(sec_0) {
                    Ok(x) => x,
                    Err(_) => return Err(UnknownParsingError),
                };
                let sec_1 = match Section::try_from(sec_1) {
                    Ok(x) => x,
                    Err(_) => return Err(UnknownParsingError),
                };
                Ok(AssigmentPair::new(sec_0, sec_1))
            }
            None => Err(UnknownParsingError),
        }
    }
}

const DATA: &str = include_data!("2022", "04");

fn part1(data: &str) -> usize {
    data.lines()
        .map(|l| {
            AssigmentPair::try_from(l)
                .expect("bogus input")
                .full_overlap() as usize
        })
        .sum()
}

fn part2(data: &str) -> usize {
    data.lines()
        .map(|l| {
            AssigmentPair::try_from(l)
                .expect("bogus input")
                .partial_overlap() as usize
        })
        .sum()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d04 {
    use super::*;

    #[test]
    fn example_1() {
        assert_eq!(Ok(Section::new(2, 4)), Section::try_from("2-4"));
        assert_eq!(Ok(Section::new(226, 431)), Section::try_from("226-431"));

        assert_eq!(
            Ok(AssigmentPair::new(Section::new(2, 4), Section::new(6, 8))),
            AssigmentPair::try_from("2-4,6-8")
        );

        assert!(!Section::new(2, 8).is_contained_in(&Section::new(3, 7)));
        assert!(Section::new(3, 7).is_contained_in(&Section::new(2, 8)));
        assert!(AssigmentPair::new(Section::new(3, 7), Section::new(2, 8)).full_overlap());

        let input = r#"2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"#;
        assert_eq!(2, part1(input));
        assert_eq!(4, part2(input));
    }

    #[test]
    fn test_part1() {
        assert_eq!(571, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(917, part2(DATA));
    }
}
