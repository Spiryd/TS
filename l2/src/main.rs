mod network;
use network::*;

fn print_vec(vec: &Vec<Vec<usize>>){
    for row in vec {
        println!("{:?}", row);
    }
}

fn main() {
    let edges = vec![(1, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 15), (15, 20), (20, 19), (19, 18), (18, 17), (17, 16), (16, 11), (11, 6), (6, 1), (10, 9), (9, 8), (8, 7), (7, 6), (15, 14), (14, 13), (13, 12), (12, 11), (3, 8), (8, 13), (13, 18)];
    let network = Network::new(Kind::Duplex, 20, edges);
    println!("{:?}", network);
    print_vec(&network.gen_random_intensity_matrix());
}
