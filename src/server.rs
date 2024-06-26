use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::Mutex;

use ml::Message;

use ::ml::Layer;
use ::ml::MLP;

async fn handle_connection(
    stream: TcpStream,
    clients: Arc<Mutex<HashMap<String, TcpStream>>>,
    mut mlp: MLP,
    x_train: Vec<Vec<f64>>,
    y_train: Vec<Vec<f64>>,
) {
    let peer_addr = stream.peer_addr().unwrap().to_string();

    clients.lock().await.insert(peer_addr.clone(), stream);

    loop {
        let mut input = String::new();
        let mut reader = BufReader::new(tokio::io::stdin());
        reader.read_line(&mut input).await.unwrap();

        if input.trim() == "sm" {
            let clients = clients.lock().await;
            mlp.train_dist(&x_train, &y_train, 0.1, 10000, &clients);
            for (addr, client_stream) in clients.iter() {
                let message = Message {
                    content: "Hello from the server!".to_string(),
                    receiver: addr.parse().unwrap(),
                };
                let json_message = serde_json::to_string(&message).unwrap();
                if let Err(e) = client_stream.try_write((json_message.clone() + "\n").as_bytes()) {
                    eprintln!("Failed to write to stream {}: {}", addr, e);
                }
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:8080").await.unwrap();
    println!("Server listening on port 8080");

    let clients = Arc::new(Mutex::new(HashMap::new()));
    let mlp = MLP::new(vec![
        Layer::new("relu", 4, 2),
        Layer::new("relu", 4, 4),
        Layer::new("sigmoid", 1, 4),
    ]);

    let x_train: Vec<Vec<f64>> = vec![
        vec![0.0, 0.0],
        vec![0.0, 1.0],
        vec![1.0, 0.0],
        vec![1.0, 1.0],
    ];

    let y_train = vec![vec![0.0], vec![1.0], vec![1.0], vec![0.0]];

    loop {
        let (stream, addr) = listener.accept().await.unwrap();
        println!("Client connected: {}", addr);

        let clients = Arc::clone(&clients);
        let mlpcl = MLP::clone(&mlp);
        let x_train_c = x_train.clone();
        let y_train_c = y_train.clone();
        tokio::spawn(async move {
            handle_connection(stream, clients, mlpcl, x_train_c, y_train_c).await;
        });
    }
}
