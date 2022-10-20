import socket, json, time
from threading import Thread


def solve_A(conn, data):
    x = data.get('x')
    y = data.get('y')
    A = x * y
    server_answer_dict = {"answer" : A}
    time.sleep(2)
    data_json = json.dumps(server_answer_dict)
    conn.sendall(data_json.encode('utf-8'))
    conn.close()
    print("Done")
    return server_answer_dict

def main():
    print("... Is up")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 50000))
    s.listen()
    while(True):
        print("working...")
        conn, addr = s.accept()
        data_json = conn.recv(1024)
        apod_dict = json.loads(data_json.decode())
        if data_json:
            Thread(target = solve_A, args = (conn, apod_dict)).start()
    
if __name__ == "__main__":
    print("Staring Server A")
    main()

