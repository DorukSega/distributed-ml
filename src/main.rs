// This is reserved to test the ML library without distribution
pub mod ml;

use::ml::MLP;
use::ml::Layer;

fn main() {
    // Example usage
    let mut mlp = MLP::new(vec![
        Layer::new("relu", 4, 2),
        Layer::new("relu", 4, 4),
        Layer::new("sigmoid", 1, 4),
    ]);

    let x_train = vec![
        vec![0.0, 0.0],
        vec![0.0, 1.0],
        vec![1.0, 0.0],
        vec![1.0, 1.0],
    ];

    let y_train = vec![
        vec![0.0],
        vec![1.0],
        vec![1.0],
        vec![0.0],
    ];

    mlp.train(&x_train, &y_train, 0.1, 10000);

    for test in x_train{
        let prediction = mlp.predict(&test);
        println!("Prediction for {:?}: {:?}", test, prediction.iter().map(|&x| if x > 0.5 {1} else {0}).collect::<Vec<i32>>());
    }
   
}
