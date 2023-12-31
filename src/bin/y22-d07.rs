use std::{borrow::Borrow, cell::RefCell, collections::VecDeque, rc::Rc};

use aoc::include_data;

const DATA: &str = include_data!("2022", "07");

type NodeRef = Rc<RefCell<Node>>;

struct Node {
    parent: Option<NodeRef>,
    children: Vec<NodeRef>,
    name: String,
    size: usize,
}

impl Node {
    fn add_child(&mut self, node: NodeRef) {
        self.children.push(node)
    }

    fn parent(&self) -> Option<NodeRef> {
        self.borrow().parent.clone()
    }
}

fn build_fs_tree(data: &str) -> NodeRef {
    let root = Rc::new(RefCell::new(Node {
        parent: None,
        name: "/".to_owned(),
        size: 0,
        children: vec![],
    }));
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
                // Backfill every parent. This is probably suboptimal if the number of nodes is
                // big.
                let mut tmp_cd = cd.clone();
                let mut parent_node = (*tmp_cd).borrow().parent.clone();
                while parent_node.is_some() {
                    // XXX: unwraps are not needed as parent_node is checked to be some
                    (*parent_node.clone().unwrap()).borrow_mut().size += size;
                    tmp_cd = parent_node.clone().unwrap().clone();
                    parent_node = (*tmp_cd).borrow().parent.clone();
                }
            }
        }
    }

    root
}

fn part1(data: &str) -> usize {
    let root = build_fs_tree(&data);
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

const AVAILABLE_DISK_SPACE: usize = 70_000_000;
const UPDATE_REQUIRED_DISK_SPACE: usize = 30_000_000;

fn part2(data: &str) -> usize {
    let root = build_fs_tree(&data);
    let unused_space = AVAILABLE_DISK_SPACE - (*root).borrow().size;

    if UPDATE_REQUIRED_DISK_SPACE < unused_space {
        panic!("Enough space for the update.")
    }
    let required_space = UPDATE_REQUIRED_DISK_SPACE - unused_space;

    // BFS
    let mut stack = VecDeque::new();
    stack.push_back(root.clone());
    let mut res = (*root).borrow().size;

    while let Some(node) = stack.pop_back() {
        if (*node).borrow().size >= required_space {
            res = std::cmp::min(res, (*node).borrow().size);
            dbg!(&(*node).borrow().name);
            dbg!(&(*node).borrow().size);
        }
        for child in (*node).borrow().children.iter() {
            stack.push_front((*child).clone());
        }
    }

    res
}

fn main() {
    println!("Result 1: {}", part1(DATA));
    println!("Result 2: {}", part2(DATA));
}

#[cfg(test)]
mod y22_d07 {
    use super::*;

    const EXAMPLE: &str = "\
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

    #[test]
    fn test_example1() {
        assert_eq!(95437, part1(&EXAMPLE));
    }

    #[test]
    fn test_part1() {
        assert_eq!(1543140, part1(DATA));
    }

    #[test]
    fn test_example2() {
        assert_eq!(24933642, part2(&EXAMPLE));
    }

    #[test]
    fn test_part2() {
        assert_eq!(1117448, part2(DATA));
    }
}
