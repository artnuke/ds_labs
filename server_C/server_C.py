import socket, json, time
from threading import Thread




def solve_C(conn, data):
    l = data.get('l')
    n = data.get('n')
    C = l + n/2
    server_answer_dict = {"answer" : C}
    time.sleep(2)
    data_json = json.dumps(server_answer_dict)
    conn.sendall(data_json.encode('utf-8'))
    conn.close()
    print("Done")
    return server_answer_dict

def main():
    print("... Is up")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 50003))
    s.listen()
    while(True):
        print("working...")
        conn, addr = s.accept()
        data_json = conn.recv(1024)
        apod_dict = json.loads(data_json.decode())
        if data_json:
            Thread(target = solve_C, args = (conn, apod_dict)).start()

    
if __name__ == "__main__":
    print("Staring Server C")
    main()