use tokio::net::TcpStream;
use tokio::io::{AsyncBufReadExt, BufReader};
use ml::Message;

#[tokio::main]
async fn main() {
    let mut input = String::new();
    let mut reader = BufReader::new(tokio::io::stdin());

    println!("Enter 'c' to connect to the server:");
    reader.read_line(&mut input).await.unwrap();

    if input.trim() == "c" {
        let stream = TcpStream::connect("127.0.0.1:8080").await.expect("Failed to connect");
   
        
        let client_addr = stream.local_addr().unwrap();
        let mut reader = BufReader::new(stream);
        let mut buffer = String::new();

        loop {
            buffer.clear();
            match reader.read_line(&mut buffer).await {
                Ok(0) => {
                    println!("Connection closed by server.");
                    break;
                }
                Ok(_) => {
                    match serde_json::from_str::<Message>(&buffer.trim()) {
                        Ok(message) => {
                            if client_addr == message.receiver{
                                println!("content: {} \nfor: {}", message.content, message.receiver)
                            }
                        },
                        Err(e) => eprintln!("Failed to parse JSON: {}", e),
                    }
                }
                Err(e) => {
                    eprintln!("Failed to read from stream: {}", e);
                    break;
                }
            }
        }
    }
}
