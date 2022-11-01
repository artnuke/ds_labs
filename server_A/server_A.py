from concurrent.futures import thread
import socket, json, time
from threading import Thread
import logging
from queue import Queue
import concurrent.futures
import signal
import sys



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
thraed_queue = Queue()

def terminateProcess(signalNumber, frame):
    logger.warning('(SIGTERM) terminating the process')
    sys.exit(0)

def solve_A(conn, data):
    x = data.get('x')
    y = data.get('y')
    A = x * y
    server_answer_dict = {"answer" : A}
    time.sleep(2)
    data_json = json.dumps(server_answer_dict)
    conn.sendall(data_json.encode('utf-8'))
    conn.close()
    logger.info(f"Request processed")
    return server_answer_dict

def listen():
    logger.info("Running...")
    PORT = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', PORT))
    s.listen()
    logger.info(f"Server listening on port {PORT}")
    while True:
        logger.info(f"Running...")
        conn, addr = s.accept()
        item = (conn, addr)
        thraed_queue.put(item)

def proceed(conn_obj):
    (conn, addr) = conn_obj
    data_json = conn.recv(1024)
    apod_dict = json.loads(data_json.decode())
    if data_json:
        logger.info(f"Recive request, creating thread...")
        Thread(target = solve_A, args = (conn, apod_dict)).start()
        
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.submit(listen)
            while True:
                if thraed_queue.qsize() > 3:
                    logger.info(f"Number of threads (Queue lengths): {thraed_queue.qsize()}")
                    proceed(thraed_queue.get())

if __name__ == "__main__":
    signal.signal(signal.SIGINT, terminateProcess)
    logger.info(f"SERVER A")
    main()