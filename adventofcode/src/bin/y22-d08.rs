use aoc::include_data;

const DATA: &str = include_data!("2022", "08");

fn parse(data: &str) -> Vec<Vec<u32>> {
    let mut forest = Vec::new();
    for line in data.lines() {
        let mut row = Vec::new();
        for h in line.chars() {
            row.push(h.to_digit(10).expect("Invalid digit"));
        }
        forest.push(row);
    }
    forest
}

fn part1(data: &str) -> usize {
    let forest = parse(data);
    let max_width = forest.len() - 1;
    let max_height = forest[0].len() - 1;

    let visited = forest
        .iter()
        .enumerate()
        .map(|(i, row)| {
            row.iter()
                .enumerate()
                .map(|(j, tree)| {
                    if i == 0 || i == max_width || j == 0 || j == max_height {
                        1
                    // left path
                    } else if (0..i).all(|ii| tree > &forest[ii][j]) {
                        1
                    // rigth path
                    } else if (i + 1..=max_width).all(|ii| tree > &forest[ii][j]) {
                        1
                    // down path
                    } else if (0..j).all(|jj| tree > &forest[i][jj]) {
                        1
                    // up path
                    } else if (j + 1..=max_height).all(|jj| tree > &forest[i][jj]) {
                        1
                    } else {
                        0
                    }
                })
                .sum::<usize>()
        })
        .sum();
    visited
}

fn part2(data: &str) -> usize {
    let forest = parse(data);
    let max_width = forest.len() - 1;
    let max_height = forest[0].len() - 1;

    let scenic_score = forest
        .iter()
        .enumerate()
        .map(|(i, row)| {
            row.iter()
                .enumerate()
                .map(|(j, tree)| {
                    if i == 0 || i == max_width || j == 0 || j == max_height {
                        return 0;
                    }
                    dbg!(i, j, tree);
                    let mut score = 1;
                    // TODO: the score is not the same if the end is an edge or a tree
                    score *= (0..i)
                        .rev()
                        .enumerate()
                        .take_while(|(_, ii)| tree > &forest[*ii][j])
                        .last()
                        .map_or(1, |(c, i)| c + 1);
                    dbg!(score);
                    score *= (i + 1..=max_width)
                        .enumerate()
                        .take_while(|(_, ii)| tree > &forest[*ii][j])
                        .last()
                        .map_or(1, |(c, _)| c + 1);
                    dbg!(score);
                    score *= (0..j)
                        .rev()
                        .enumerate()
                        .take_while(|(_, jj)| tree > dbg!(&forest[i][*dbg!(jj)]))
                        .last()
                        .map_or(1, |(c, _)| c + 1);
                    dbg!(score);
                    score *= (j + 1..=max_height)
                        .enumerate()
                        .take_while(|(_, jj)| tree > &forest[i][*jj])
                        .last()
                        .map_or(1, |(c, _)| c + 1);
                    dbg!(score);
                    score
                })
                .sum::<usize>()
        })
        .max()
        .unwrap_or(0);
    scenic_score
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d08 {
    use super::*;

    const EXAMPLE: &str = "\
30373
25512
65332
33549
35390";

    #[test]
    fn test_example1() {
        assert_eq!(21, part1(EXAMPLE));
    }

    #[test]
    fn test_part1() {
        assert_eq!(1854, part1(DATA));
    }

    #[test]
    fn test_example2() {
        assert_eq!(8, part2(EXAMPLE));
    }

    #[test]
    fn test_part2() {
        assert_eq!(0usize, part2(DATA));
    }
}
