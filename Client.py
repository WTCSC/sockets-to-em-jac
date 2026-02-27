
import socket 

def client_connection(host='10.103.1.47', port=5000):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"Connecion Success, {host}:{port}")
        
        while True:
            msg = input("Client: ")
            if not msg:
                break
            
            client.send(msg.encode())
            response = client.recv(1024).decode()
            print(response)
        
        client.closed()
        
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    client_connection()