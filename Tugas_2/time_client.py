import socket
import logging

logging.basicConfig(level=logging.INFO)

def main():
    server_address = ('127.0.0.1', 45000)  

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"Connecting to {server_address}")
        sock.connect(server_address)

        time_request = "TIME\r\n"
        logging.info(f"Sending request: {repr(time_request)}")
        sock.sendall(time_request.encode())

        response = sock.recv(1024)
        logging.info(f"Received: {response.decode().strip()}")

        quit_request = "QUIT\r\n"
        logging.info(f"Sending request: {repr(quit_request)}")
        sock.sendall(quit_request.encode())

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logging.info("Closing socket")
        sock.close()

if __name__ == "__main__":
    main()
