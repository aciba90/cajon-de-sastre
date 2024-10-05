use aoc::include_data;
use std::str::FromStr;

#[derive(Debug, PartialEq, Clone)]
enum Gamble {
    Rock,
    Paper,
    Scissors,
}

impl Gamble {
    fn score(&self) -> usize {
        match self {
            Self::Rock => 1,
            Self::Paper => 2,
            Self::Scissors => 3,
        }
    }

    fn win(&self) -> Self {
        match self {
            Self::Rock => Self::Paper,
            Self::Paper => Self::Scissors,
            Self::Scissors => Self::Rock,
        }
    }

    fn lose(&self) -> Self {
        match self {
            Self::Rock => Self::Scissors,
            Self::Paper => Self::Rock,
            Self::Scissors => Self::Paper,
        }
    }

    fn draw(&self) -> Self {
        self.clone()
    }
}

#[derive(Debug)]
struct UnkownParsingError;

impl FromStr for Gamble {
    type Err = UnkownParsingError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" | "X" => Ok(Gamble::Rock),
            "B" | "Y" => Ok(Gamble::Paper),
            "C" | "Z" => Ok(Gamble::Scissors),
            _ => Err(UnkownParsingError),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Round {
    oponent: Gamble,
    you: Gamble,
}

impl Round {
    fn _score(&self) -> usize {
        if self.oponent == self.you {
            return GameResult::Draw.score();
        }
        match &self {
            Round {
                oponent: Gamble::Rock,
                you: Gamble::Paper,
            }
            | Round {
                oponent: Gamble::Paper,
                you: Gamble::Scissors,
            }
            | Round {
                oponent: Gamble::Scissors,
                you: Gamble::Rock,
            } => GameResult::Win,
            _ => GameResult::Lose,
        }
        .score()
    }

    fn score(&self) -> usize {
        self._score() + self.you.score()
    }
}

impl FromStr for Round {
    type Err = UnkownParsingError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.lines().take(1).next().unwrap().split_once(' ') {
            Some((oponent, you)) => Ok(Round {
                oponent: oponent.parse().unwrap(),
                you: you.parse().unwrap(),
            }),
            None => Err(UnkownParsingError),
        }
    }
}

#[derive(Debug, PartialEq)]
enum GameResult {
    Win,
    Draw,
    Lose,
}

impl GameResult {
    fn score(&self) -> usize {
        match self {
            Self::Win => 6,
            Self::Draw => 3,
            Self::Lose => 0,
        }
    }
}

impl FromStr for GameResult {
    type Err = UnkownParsingError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "X" => Ok(GameResult::Lose),
            "Y" => Ok(GameResult::Draw),
            "Z" => Ok(GameResult::Win),
            _ => Err(UnkownParsingError),
        }
    }
}

#[derive(Debug, PartialEq)]
struct RoundSuggestion {
    oponent: Gamble,
    suggestion: GameResult,
}

impl From<RoundSuggestion> for Round {
    fn from(round_suggestion: RoundSuggestion) -> Self {
        let you = match round_suggestion.suggestion {
            GameResult::Draw => round_suggestion.oponent.draw(),
            GameResult::Win => round_suggestion.oponent.win(),
            GameResult::Lose => round_suggestion.oponent.lose(),
        };
        Round {
            oponent: round_suggestion.oponent,
            you,
        }
    }
}

impl FromStr for RoundSuggestion {
    type Err = UnkownParsingError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.lines().take(1).next().unwrap().split_once(' ') {
            Some((oponent, suggestion)) => Ok(RoundSuggestion {
                oponent: oponent.parse().unwrap(),
                suggestion: suggestion.parse().unwrap(),
            }),
            None => Err(UnkownParsingError),
        }
    }
}

fn parse_input_1(buf: &str) -> Vec<Round> {
    buf.lines().map(|line| line.parse().unwrap()).collect()
}

fn parse_input_2(buf: &str) -> Vec<Round> {
    buf.lines()
        .map(|line| line.parse::<RoundSuggestion>().unwrap().into())
        .collect()
}

const DATA: &str = include_data!("2022", "02");

fn part1(data: &str) -> usize {
    let rounds = parse_input_1(data);
    rounds.iter().map(|r| r.score()).sum()
}

fn part2(data: &str) -> usize {
    let rounds = parse_input_2(data);
    rounds.iter().map(|r| r.score()).sum()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d02 {
    use super::*;

    #[test]
    fn test_parse_line() {
        let input_line = "A X\nB Z\nC Y\n";
        let expected_result = vec![
            Round {
                oponent: Gamble::Rock,
                you: Gamble::Rock,
            },
            Round {
                oponent: Gamble::Paper,
                you: Gamble::Scissors,
            },
            Round {
                oponent: Gamble::Scissors,
                you: Gamble::Paper,
            },
        ];
        assert_eq!(expected_result, parse_input_1(input_line));
    }

    #[test]
    fn example_1() {
        let data = "A Y\nB X\nC Z";
        assert_eq!(15, part1(data))
    }

    #[test]
    fn test_part1() {
        assert_eq!(13924, part1(DATA));
    }

    #[test]
    fn example_2() {
        let data = "A Y\nB X\nC Z";
        assert_eq!(12, part2(data))
    }

    #[test]
    fn test_part2() {
        assert_eq!(13448, part2(DATA));
    }
}
