import socket, json, time
from threading import Thread
import logging
from queue import Queue
import concurrent.futures




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
thraed_queue = Queue()

def solve_C(conn, data):
    l = data.get('l')
    n = data.get('n')
    C = l + n/2
    server_answer_dict = {"answer" : C}
    time.sleep(2)
    data_json = json.dumps(server_answer_dict)
    conn.sendall(data_json.encode('utf-8'))
    conn.close()
    logger.info(f"Request processed")
    return server_answer_dict

def listen():
    logger.info("Running...")
    PORT = 50002
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
            newThread = Thread(target = solve_C, args = (conn, apod_dict))
            thraed_queue.put(newThread)
        
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(listen)
            while True:
                if thraed_queue.qsize() > 0:
                    logger.info(f"Number of threads (Queue lengths): {thraed_queue.qsize()}")
                    thraed_queue.get().start()
    
if __name__ == "__main__":
    print("Staring Server C")
    main()