
use rand::Rng;
use tokio::{net::TcpStream, sync::MutexGuard};
use std::f64::consts::E;
use std::collections::HashMap;


// Define the activation functions and their derivatives
fn relu(x: f64) -> f64 {
    x.max(0.0)
}

fn relu_derivative(x: f64) -> f64 {
    if x > 0.0 { 1.0 } else { 0.0 }
}

fn sigmoid(x: f64) -> f64 {
    1.0 / (1.0 + E.powf(-x))
}

fn sigmoid_derivative(x: f64) -> f64 {
    x * (1.0 - x)
}

// Define the forward pass function
pub fn forward_pass(weights: &[f64], inputs: &[f64], bias: f64, activation: &str) -> f64 {
    let z: f64 = weights.iter().zip(inputs).map(|(w, x)| w * x).sum::<f64>() + bias;
    match activation {
        "relu" => relu(z),
        "sigmoid" => sigmoid(z),
        _ => panic!("Unsupported activation function"),
    }
}

// Define the Neuron struct
#[derive(Debug, Clone)]
struct Neuron {
    weights: Vec<f64>,
    bias: f64,
    activation_type: String,
    output: f64,
    inputs: Vec<f64>,
}

impl Neuron {
    fn new(n_inputs: usize, activation: &str) -> Neuron {
        let mut rng = rand::thread_rng();
        Neuron {
            weights: (0..n_inputs).map(|_| rng.gen()).collect(),
            bias: rng.gen(),
            activation_type: activation.to_string(),
            output: 0.0,
            inputs: vec![],
        }
    }

    fn backward(&mut self, dvalue: f64, learning_rate: f64) -> Vec<f64> {
        let dactivation = match self.activation_type.as_str() {
            "relu" => relu_derivative(self.output) * dvalue,
            "sigmoid" => sigmoid_derivative(self.output) * dvalue,
            _ => panic!("Unsupported activation function"),
        };
        let dweights: Vec<f64> = self.inputs.iter().map(|x| x * dactivation).collect();
        let dbias = dactivation;
        let dinputs: Vec<f64> = self.weights.iter().map(|w| w * dactivation).collect();
        self.weights = self.weights.iter().zip(&dweights).map(|(w, dw)| w - learning_rate * dw).collect();
        self.bias -= learning_rate * dbias;
        dinputs
    }
}

// Define the Layer struct
#[derive(Clone)]
pub struct Layer {
    neurons: Vec<Neuron>,
    activation: String,
    inputs: Vec<f64>,
    outputs: Vec<f64>,
}

impl Layer {
    pub fn new(activation: &str, n_neurons: usize, input_shape: usize) -> Layer {
        Layer {
            neurons: (0..n_neurons).map(|_| Neuron::new(input_shape, activation)).collect(),
            activation: activation.to_string(),
            inputs: vec![],
            outputs: vec![],
        }
    }

    fn forward(&mut self, inputs: &[f64]) -> Vec<f64> {
        self.inputs = inputs.to_vec();
        self.outputs = self.neurons.iter_mut().map(|neuron| {
            neuron.inputs = inputs.to_vec();
            neuron.output = forward_pass(&neuron.weights, inputs, neuron.bias, &self.activation);
            neuron.output
        }).collect();
        self.outputs.clone()
    }

    fn backward(&mut self, dvalues: &[f64], learning_rate: f64) -> Vec<f64> {
        let mut dinputs = vec![0.0; self.inputs.len()];
        for (i, neuron) in self.neurons.iter_mut().enumerate() {
            let dinput = neuron.backward(dvalues[i], learning_rate);
            dinputs.iter_mut().zip(dinput.iter()).for_each(|(d, di)| *d += di);
        }
        dinputs
    }
}

// Define the MLP struct
#[derive(Clone)]
pub struct MLP {
    layers: Vec<Layer>,
}

impl MLP {
    pub fn new(layers: Vec<Layer>) -> MLP {
        MLP { layers }
    }

    fn forward(&mut self, inputs: &[f64]) -> Vec<f64> {
        let mut result = inputs.to_vec();
        for layer in self.layers.iter_mut() {
            result = layer.forward(&result);
        }
        result
    }

    fn backward(&mut self, y_true: &[f64], learning_rate: f64) {
        let mut dvalue: Vec<f64> = self.layers.last().unwrap().outputs.iter().zip(y_true.iter()).map(|(o, y)| o - y).collect();
        for layer in self.layers.iter_mut().rev() {
            dvalue = layer.backward(&dvalue, learning_rate);
        }
    }

    pub fn train(&mut self, x_train: &[Vec<f64>], y_train: &[Vec<f64>], learning_rate: f64, epochs: usize) {
        for epoch in 0..epochs {
            let mut total_loss = 0.0;
            for (inputs, y_true) in x_train.iter().zip(y_train.iter()) {
                let output = self.forward(inputs);
                let loss = output.iter().zip(y_true).map(|(o, y)| (o - y).powi(2)).sum::<f64>() / y_true.len() as f64;
                total_loss += loss;
                self.backward(y_true, learning_rate);
            }
            let avg_loss = total_loss / x_train.len() as f64;
            if epoch % 100 == 0 {
                println!("Epoch {}, Loss: {:.4}", epoch, avg_loss);
            }
        }
    }

    pub fn train_dist(&mut self, x_train: &[Vec<f64>], y_train: &[Vec<f64>], learning_rate: f64, epochs: usize, clients:&MutexGuard<HashMap<String, TcpStream>>) {
        for epoch in 0..epochs {
            let mut total_loss = 0.0;
            for (inputs, y_true) in x_train.iter().zip(y_train.iter()) {
                let output = self.forward(inputs);
                let loss = output.iter().zip(y_true).map(|(o, y)| (o - y).powi(2)).sum::<f64>() / y_true.len() as f64;
                total_loss += loss;
                self.backward(y_true, learning_rate);
            }
            let avg_loss = total_loss / x_train.len() as f64;
            if epoch % 100 == 0 {
                println!("Epoch {}, Loss: {:.4}", epoch, avg_loss);
            }
        }
    }

    pub fn predict(&mut self, inputs: &[f64]) -> Vec<f64> {
        self.forward(inputs)
    }
}


use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Message {
    pub content: String,
    pub receiver: std::net::SocketAddr
}
