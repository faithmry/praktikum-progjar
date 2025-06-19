from socket import *
import socket
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.info(f"Client connected: {self.address}")
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break

                message = data.decode().strip()
                logging.info(f"Received from {self.address}: {repr(message)}")

                if message == "TIME":
                    now = datetime.now()
                    jam = now.strftime("%H:%M:%S")
                    response = f"JAM {jam}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                elif message == "QUIT":
                    logging.info(f"Client {self.address} sent QUIT. Closing connection.")
                    break
                else:
                    logging.info(f"Invalid request from {self.address}: {message}")
        except Exception as e:
            logging.warning(f"Exception from {self.address}: {e}")
        finally:
            self.connection.close()
            logging.info(f"Connection closed: {self.address}")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        server_address = ('0.0.0.0', 45000)
        self.my_socket.bind(server_address)
        self.my_socket.listen(5)
        logging.info(f"Time server listening on {server_address}")

        while True:
            connection, client_address = self.my_socket.accept()
            client_thread = ProcessTheClient(connection, client_address)
            client_thread.start()
            self.the_clients.append(client_thread)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
