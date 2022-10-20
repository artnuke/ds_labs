import socket
import json
import concurrent.futures
# import time
import logging

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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a = executor.submit(server_request, server_request_dict, IP_ADDR = "localhost", PORT = 50000)
        answer = a.result()
    A = answer.get("answer")
    return A

def get_B(k, l, m, n):
    server_request_dict = { "k": k,
                        "l": l,
                        "m": m,
                        "n": n}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        b = executor.submit(server_request, server_request_dict, IP_ADDR = "localhost", PORT = 50001)
        answer = b.result()
    B = answer.get("answer")
    return B

def main(x, y, k, l ,m, n):
    A = get_A(x, y)
    B = get_B(k,l,m,n)
    f =  A + B
    print(f"Answer: f(A + B) = {f}")



if __name__ == "__main__":
    logging.info('Starting...')

    x = 1
    y = 2
    k = 1
    l = 2
    m = 3
    n = 4

    logging.info(f'x = {x}, y = {y}, k = {k}, l = {l}, m = {m}, n = {n}')

    main(x, y, k, l, m, n)