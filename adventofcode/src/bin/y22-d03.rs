use std::collections::HashSet;

use aoc::include_data;

struct Rucksack(String);

type Compartment = str;

impl Rucksack {
    fn new(data: &str) -> Self {
        Self(data.to_string())
    }

    fn compartment_1(&self) -> &Compartment {
        &self.0[..(self.0.len() / 2)]
    }

    fn compartment_2(&self) -> &Compartment {
        &self.0[(self.0.len() / 2)..]
    }

    fn compartments(&self) -> (&Compartment, &Compartment) {
        (self.compartment_1(), self.compartment_2())
    }

    fn common_item(&self) -> Item {
        let (c1, c2) = self.compartments();

        first_common_item(&[c1, c2]).expect("expected one common item per compartment")
    }

    fn total_priority(&self) -> usize {
        self.common_item().priority()
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
#[allow(non_camel_case_types)]
enum Item {
    a,
    b,
    c,
    d,
    e,
    f,
    g,
    h,
    i,
    j,
    k,
    l,
    m,
    n,
    o,
    p,
    q,
    r,
    s,
    t,
    u,
    v,
    w,
    x,
    y,
    z,
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    U,
    V,
    W,
    X,
    Y,
    Z,
}

impl Item {
    fn priority(&self) -> usize {
        match self {
            Self::a => 1,
            Self::b => 2,
            Self::c => 3,
            Self::d => 4,
            Self::e => 5,
            Self::f => 6,
            Self::g => 7,
            Self::h => 8,
            Self::i => 9,
            Self::j => 10,
            Self::k => 11,
            Self::l => 12,
            Self::m => 13,
            Self::n => 14,
            Self::o => 15,
            Self::p => 16,
            Self::q => 17,
            Self::r => 18,
            Self::s => 19,
            Self::t => 20,
            Self::u => 21,
            Self::v => 22,
            Self::w => 23,
            Self::x => 24,
            Self::y => 25,
            Self::z => 26,
            Self::A => 27,
            Self::B => 28,
            Self::C => 29,
            Self::D => 30,
            Self::E => 31,
            Self::F => 32,
            Self::G => 33,
            Self::H => 34,
            Self::I => 35,
            Self::J => 36,
            Self::K => 37,
            Self::L => 38,
            Self::M => 39,
            Self::N => 40,
            Self::O => 41,
            Self::P => 42,
            Self::Q => 43,
            Self::R => 44,
            Self::S => 45,
            Self::T => 46,
            Self::U => 47,
            Self::V => 48,
            Self::W => 49,
            Self::X => 50,
            Self::Y => 51,
            Self::Z => 52,
        }
    }
}

#[derive(Debug)]
struct UnkownParsingError;

impl TryFrom<char> for Item {
    type Error = UnkownParsingError;

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            'a' => Ok(Item::a),
            'b' => Ok(Item::b),
            'c' => Ok(Item::c),
            'd' => Ok(Item::d),
            'e' => Ok(Item::e),
            'f' => Ok(Item::f),
            'g' => Ok(Item::g),
            'h' => Ok(Item::h),
            'i' => Ok(Item::i),
            'j' => Ok(Item::j),
            'k' => Ok(Item::k),
            'l' => Ok(Item::l),
            'm' => Ok(Item::m),
            'n' => Ok(Item::n),
            'o' => Ok(Item::o),
            'p' => Ok(Item::p),
            'q' => Ok(Item::q),
            'r' => Ok(Item::r),
            's' => Ok(Item::s),
            't' => Ok(Item::t),
            'u' => Ok(Item::u),
            'v' => Ok(Item::v),
            'w' => Ok(Item::w),
            'x' => Ok(Item::x),
            'y' => Ok(Item::y),
            'z' => Ok(Item::z),
            'A' => Ok(Item::A),
            'B' => Ok(Item::B),
            'C' => Ok(Item::C),
            'D' => Ok(Item::D),
            'E' => Ok(Item::E),
            'F' => Ok(Item::F),
            'G' => Ok(Item::G),
            'H' => Ok(Item::H),
            'I' => Ok(Item::I),
            'J' => Ok(Item::J),
            'K' => Ok(Item::K),
            'L' => Ok(Item::L),
            'M' => Ok(Item::M),
            'N' => Ok(Item::N),
            'O' => Ok(Item::O),
            'P' => Ok(Item::P),
            'Q' => Ok(Item::Q),
            'R' => Ok(Item::R),
            'S' => Ok(Item::S),
            'T' => Ok(Item::T),
            'U' => Ok(Item::U),
            'V' => Ok(Item::V),
            'W' => Ok(Item::W),
            'X' => Ok(Item::X),
            'Y' => Ok(Item::Y),
            'Z' => Ok(Item::Z),
            _ => Err(UnkownParsingError),
        }
    }
}

fn build_item_set(comp: &str) -> HashSet<Item> {
    let mut set = HashSet::new();
    for c in comp.chars() {
        set.insert(c.try_into().expect("Bogus input data"));
    }
    set
}

impl<'a> FromIterator<&'a Item> for HashSet<Item> {
    fn from_iter<T: IntoIterator<Item = &'a Item>>(iter: T) -> Self {
        let mut set = HashSet::new();

        for item in iter {
            set.insert(item.clone());
        }

        set
    }
}

fn first_common_item(item_groups: &[&str]) -> Option<Item> {
    let set = item_groups
        .iter()
        .map(|i| build_item_set(i))
        .reduce(|acc, s| acc.intersection(&s).collect())
        .unwrap();
    set.into_iter().next()
}

const DATA: &str = include_data!("2022", "03");

fn part1(data: &str) -> usize {
    data.lines()
        .map(|l| Rucksack::new(l).total_priority())
        .sum()
}

fn part2(data: &str) -> usize {
    let lines: Vec<_> = data.lines().collect();
    lines
        .chunks(3)
        .map(|group| {
            first_common_item(group)
                .expect("expected one common item per group")
                .priority()
        })
        .sum()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d03 {
    use super::*;

    #[test]
    fn example_1() {
        let sack = Rucksack::new("vJrwpWtwJgWrhcsFMMfFFhFp");
        assert_eq!(("vJrwpWtwJgWr", "hcsFMMfFFhFp"), sack.compartments());

        let common_items = sack.common_item();
        assert_eq!(Item::p, common_items);
        assert_eq!(16usize, sack.total_priority());
    }

    #[test]
    fn example_2() {
        let data = r#"vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"#;
        assert_eq!(157, part1(data));
        assert_eq!(70, part2(data));
    }

    #[test]
    fn test_part1() {
        assert_eq!(7845, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(2790, part2(DATA));
    }
}
