import socket
import json
import concurrent.futures
import logging
import time
from random import randint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def server_request(server_request_dict, IP_ADDR, PORT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP_ADDR, PORT))
        logging.info(f'Connecting to server... IP:PORT {IP_ADDR}:{PORT}')
        data_json = json.dumps(server_request_dict)
        s.sendall(data_json.encode('utf-8'))
        data_json = s.recv(1024)
        s.close()
        if data_json:
            logging.info(f'Code 200 from IP:PORT {IP_ADDR}:{PORT}')
            apod_dict = json.loads(data_json.decode())
            return apod_dict
    except Exception as e:
        logging.error(f'Error {e}')

def get_A(x, y):
    server_request_dict = { "x": x,
                        "y": y}
    answer = server_request(server_request_dict = server_request_dict, IP_ADDR = "localhost", PORT = 50000)
    A = answer.get("answer")
    return A

def get_B(k, l, m, n):
    server_request_dict = { "k": k,
                        "l": l,
                        "m": m,
                        "n": n}
    answer = server_request(server_request_dict = server_request_dict, IP_ADDR = "localhost", PORT = 50001)
    B = answer.get("answer")
    return B

def main(x, y, k, l ,m, n, id):
    time.sleep(3)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a = executor.submit(get_A, x, y)
        b = executor.submit(get_B, k, l, m, n)
        logging.info(f'Start Async Threading')
        A = a.result()
        B = b.result()
    f =  A + B
    print(f"id: {id} | Answer: f(A + B) = {f}")

if __name__ == "__main__":
    logging.info('Starting...')

    x = randint(0, 10)
    y = randint(0, 10)
    k = randint(0, 10)
    l = randint(0, 10)
    m = randint(0, 10)
    n = randint(0, 10)

    id = randint(0, 20)
    
    logging.info(f'id = {id} | x = {x}, y = {y}, k = {k}, l = {l}, m = {m}, n = {n}')

    main(x, y, k, l, m, n, id)