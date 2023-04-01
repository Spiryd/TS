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
    adj: Vec<Vec<usize>>,

}

impl Network {
    pub fn new(kind: Kind, node_quantity: usize, edges: Vec<(usize, usize)>) -> Self {
        let mut adj: Vec<Vec<usize>> = Vec::new();
        for _ in 1..=node_quantity {
            adj.push(Vec::new());
        }
        match kind {
            Kind::Simplex => {
                for edge in edges {
                    adj[edge.0 - 1].push(edge.1);
                }
            },
            Kind::Duplex => {
                for edge in edges {
                    adj[edge.0 - 1].push(edge.1);
                    adj[edge.1 - 1].push(edge.0);
                }
            }
        }
        Self { kind, node_quantity, adj}
    }

    pub fn capacity(&self) {
        todo!();
    }

    pub fn flow(&self, intensity_matrix: Vec<Vec<usize>>) {
        todo!();
    }

    pub fn gen_random_intensity_matrix(&self) -> Vec<Vec<usize>>{
        let mut intensity_matrix: Vec<Vec<usize>> = vec![vec![0 ; self.node_quantity]; self.node_quantity];
        let mut rng: Pcg64 = Pcg64::from_entropy();
        for i in 0..self.node_quantity {
            for j in 0..self.node_quantity {
                intensity_matrix[i][j] = (rng.next_u32()/8) as usize;
            }
        }
        return intensity_matrix;
    }
}