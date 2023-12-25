use std::{borrow::{Borrow, BorrowMut}, cell::RefCell, rc::Rc, usize};

use aoc::include_data;

const DATA: &str = include_data!("2022", "07");

struct Node {
    parent: Option<Rc<RefCell<Node>>>,
    children: Vec<Rc<RefCell<Node>>>,
    name: String,
    size: usize,
}

impl Default for Node {
    fn default() -> Self {
        Self {
            parent: None,
            children: vec![],
            name: String::new(),
            size: usize::default(),
        }
    }
}

impl Node {
    // fn new() -> Self {
    // }
    fn add_child(&mut self, node: Rc<RefCell<Node>>) {
        self.children.push(node)
    }

    fn parent(&self) -> Option<Rc<RefCell<Node>>> {
        self.borrow().parent.clone()
    }
}

fn part1(data: &str) -> usize {
    let root = Rc::new(RefCell::new(Node::default()));
    let mut cd = root.clone();
    for line in data.lines().skip(1) {
        if line == "$ ls" {
            continue;
        }
        if let Some((_, dir)) = line.split_once("dir ") {
            let tmp = Rc::new(RefCell::new(Node {
                parent: Some(cd.clone()),
                name: dir.to_owned(),
                size: 0,
                children: vec![],
            }));
            (*cd).borrow_mut().add_child(tmp);
        } else if let Some((_, dir)) = line.split_once("$ cd ") {
            if dir == ".." {
                let tmp = cd.clone();
                cd = (*tmp).borrow().parent().expect("The only node without parent is root, and a cd .. is not possible when cd is /");
            } else {
                let tmp = Rc::new(RefCell::new(Node {
                    parent: Some(cd.clone()),
                    name: dir.to_owned(),
                    size: 0,
                    children: vec![],
                }));
                (*cd).borrow_mut().add_child(tmp.clone());
                cd = tmp;
            }
        } else {
            if let Some((size, _)) = line.split_once(" ") {
                let size: usize = size.parse().expect(&format!("Expected file in line: {}", line));
                (*cd).borrow_mut().size += size;
            }
        }
    }
    todo!();
    0
}

fn part2(data: &str) -> usize {
    todo!()
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d07 {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(0usize, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(0usize, part2(DATA));
    }
}
