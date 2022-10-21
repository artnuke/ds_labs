import socket, json, time
from threading import Thread
import concurrent.futures
import logging
from queue import Queue




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
thraed_queue = Queue()

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

def solve_B(conn, data):
    k = data.get('k')
    m = data.get('m')
    l = data.get("l")
    n = data.get("n")
    server_request_dict = {"l": l, 
                            "n" : n}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        a = executor.submit(server_request, server_request_dict, IP_ADDR = "10.5.0.5", PORT = 50002)
        C = a.result().get('answer')
    B = C + k * (2 + m)
    server_answer_dict = {"answer" : B}
    time.sleep(2)
    data_json = json.dumps(server_answer_dict)
    conn.sendall(data_json.encode('utf-8'))
    conn.close()
    logger.info(f"Request processed")
    return server_answer_dict

def listen():
    logger.info("Running...")
    PORT = 50001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', PORT))
    s.listen()
    logger.info(f"Server listening on port {PORT}")
    while(True):
        logger.info(f"Running...")
        conn, addr = s.accept()
        data_json = conn.recv(1024)
        apod_dict = json.loads(data_json.decode())
        if data_json:
            logger.info(f"Recive request, creating thread...")
            newThread = Thread(target = solve_B, args = (conn, apod_dict))
            thraed_queue.put(newThread)
            

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(listen)
            while True:
                if thraed_queue.qsize() > 0:
                    logger.info(f"Number of threads (Queue lengths): {thraed_queue.qsize()}")
                    thraed_queue.get().start()

if __name__ == "__main__":
    logger.info(f"SERVER B")
    main()
