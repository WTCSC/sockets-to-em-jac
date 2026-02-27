import socket
import sys

def startServer():
    server = None
    client = None

    try:
        # Create socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(("0.0.0.0", 5000))
        server.listen(1)

        print(f"Server listening on 0.0.0.0:{5000}")

        while True:
            try:
                client, addr = server.accept()
                print(f"Connected to {addr}")

                # Set timeout for client
                client.settimeout(120)

                while True:
                    try:
                        msg = client.recv(1024)

                        # Client disconnected cleanly
                        if not msg:
                            print(f"Client {addr} disconnected.")
                            break

                        try:
                            msg = msg.decode().strip()
                        except UnicodeDecodeError:
                            print("Invalid message format received.")
                            client.send(b"Error: Invalid message format.\n".encode())
                            continue

                        print(f"Client: {msg}")

                        # Server input handling
                        try:
                            response = input("Server: ").strip()
                        except EOFError:
                            response = "Server input error."

                        if not response:
                            response = "(empty message)"

                        client.send(f"Server: {response}\n".encode())

                    except socket.timeout:
                        print("Client connection timed out.")
                        client.send(b"Error: Connection timed out.\n".encode())
                        break

                    except ConnectionResetError:
                        print("Client connection reset unexpectedly.")
                        break

                    except BrokenPipeError:
                        print("Broken pipe. Client likely disconnected.")
                        break

                    except Exception as e:
                        print(f"Unexpected client error: {e}")
                        try:
                            client.send(b"Error: Internal server error.\n".encode())
                        except:
                            pass
                        break

                # Always close client cleanly
                client.close()
                print("Client connection closed.")
                print("Waiting for next client\n")

            except socket.error as e:
                print(f"Error accepting connection: {e}")

    except OSError as e:
        print(f"Server startup failed: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nServer shutting down")

    finally:
        if client:
            try:
                client.close()
            except:
                pass

        if server:
            try:
                server.close()
            except:
                pass

        print("Server closed.")


if __name__ == "__main__":
    startServer()