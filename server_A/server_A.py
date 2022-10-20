import socket, json, time
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


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

def main():
    logger.info("Running...")
    PORT = 50000
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
            Thread(target = solve_A, args = (conn, apod_dict)).start()
    
if __name__ == "__main__":
    logger.info(f"SERVER A")
    main()

