mod network;
use network::*;

fn main() {
    let network = Network::default();
    println!("{:?}", network);
    network.flow(network.gen_random_intensity_matrix());
}
