use std::hash::Hash;
use std::{
    borrow::{Borrow, BorrowMut},
    cell::RefCell,
    collections::{HashSet, VecDeque},
    rc::Rc,
    usize,
};

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
                let child_size = (*cd).borrow().size;
                let tmp = cd.clone();
                cd = (*tmp).borrow().parent().expect("The only node without parent is root, and a cd .. is not possible when cd is /");
                (*cd).borrow_mut().size += child_size;
            } else {
                // TODO: check if we do re-enter to a dir. Not checking this does not make invalid
                // the result of part1.
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
            // Example: '14848514 b.txt'
            if let Some((size, _name)) = line.split_once(" ") {
                let size: usize = size
                    .parse()
                    .expect(&format!("Expected file in line: {}", line));
                (*cd).borrow_mut().size += size;
            }
        }
    }

    // DFS sum
    let mut res = 0_usize;
    let mut stack = VecDeque::new();
    stack.push_back(root);

    while let Some(node) = stack.pop_back() {
        dbg!("Visiting node: ", &(*node).borrow().name);
        dbg!(&(*node).borrow().size);
        if (*node).borrow().size < 100_000 {
            res += (*node).borrow().size;
        }
        for child in (*node).borrow().children.iter() {
            stack.push_back((*child).clone());
        }
    }

    res
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
    fn test_example1() {
        let data = "\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
";
        assert_eq!(95437, part1(&data));
    }

    #[test]
    fn test_part1() {
        assert_eq!(1543140, part1(DATA));
    }

    #[test]
    fn test_part2() {
        assert_eq!(0usize, part2(DATA));
    }
}
