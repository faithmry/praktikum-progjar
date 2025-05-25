from socket import *
import socket
import logging
import time
import sys
from concurrent.futures import ThreadPoolExecutor

from file_protocol import FileProtocol
fp = FileProtocol()

def process_client(connection, address):
    buffer = ""
    try: 
        connection.settimeout(1800)
        while True:
            data = connection.recv(134217728)
            if not data:
                break
            buffer += data.decode()
            while "\r\n\r\n" in buffer:
                command, buffer = buffer.split("\r\n\r\n", 1)
                hasil = fp.proses_string(command)
                hasil += "\r\n\r\n"
                connection.sendall(hasil.encode())
    except Exception as e:
        logging.warning(f"Error: {str(e)}")                
    finally:
        logging.warning(f"connection from {address} closed")
        connection.close()

class Server:
    def __init__(self, ipaddress='0.0.0.0', port=8889, pool_size=5):
        self.ipinfo = (ipaddress, port)
        self.pool_size = pool_size
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.my_socket.settimeout(1800) 

    def run(self):
        logging.warning(f"server running on ip address {self.ipinfo} with thread pool size {self.pool_size}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(5)  
        
        with ThreadPoolExecutor(max_workers=self.pool_size) as executor:
            try:
                while True:
                    connection, client_address = self.my_socket.accept()
                    logging.warning(f"connection from {client_address}")
                    executor.submit(process_client, connection, client_address)
            except KeyboardInterrupt:
                logging.warning("Server shutting down")
            finally:
                if self.my_socket:
                    self.my_socket.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python file_server_pool.py <max_workers>")
        sys.exit(1)
    workers = int(sys.argv[1])
    
    svr = Server(ipaddress='0.0.0.0', port=6667, pool_size=workers)
    svr.run()


if __name__ == "__main__":
    main()

