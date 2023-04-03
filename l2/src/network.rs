use rand::prelude::*;
use rand_pcg::Pcg64;

#[derive(Debug, PartialEq, Clone)]
pub enum Kind {
    Simplex,
    Duplex
}

#[derive(Debug)]
pub struct Network{
    kind: Kind,
    node_quantity: usize,
    edges: Vec<(usize, usize)>,
    capacity: Vec<usize>
}

impl Network {
    pub fn new(kind: Kind, node_quantity: usize, edges: Vec<(usize, usize)>, capacity: Vec<usize>) -> Self {
        Self {kind, node_quantity, edges, capacity}
    }

    pub fn flow(&self, intensity_matrix: Vec<Vec<usize>>) {
        for i in 0..(self.edges.len()) {
            println!("{:?}", self.edges[i]);
            println!("{:?}", self.capacity[i]);
        }
    }

    pub fn gen_random_intensity_matrix(&self) -> Vec<Vec<usize>>{
        let mut intensity_matrix: Vec<Vec<usize>> = vec![vec![0 ; self.node_quantity]; self.node_quantity];
        let mut rng: Pcg64 = Pcg64::from_entropy();
        for i in 0..self.node_quantity {
            for j in 0..self.node_quantity {
                intensity_matrix[i][j] = (rng.gen_range(0..=(u8::MAX / 4))) as usize;
            }
        }
        return intensity_matrix;
    }
}

impl Default for Network {
    fn default() -> Self {
        let edges = vec![(1, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 15), (15, 20), (20, 19), (19, 18), (18, 17), (17, 16), (16, 11), (11, 6), (6, 1), (10, 9), (9, 8), (8, 7), (7, 6), (15, 14), (14, 13), (13, 12), (12, 11), (3, 8), (8, 13), (13, 18)];
        let capacity: Vec<usize> = vec![255; edges.len()];
        Self { kind: Kind::Duplex, node_quantity: 20, edges, capacity }
    }
}
