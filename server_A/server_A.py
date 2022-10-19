import socket, json, time



def solve_A(data):
    x = data.get('x')
    y = data.get('y')
    A = x * y
    server_answer_dict = {"answer" : A}
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
       
        if data_json:
            print("Processing request")
            apod_dict = json.loads(data_json.decode())
            print(apod_dict)
            server_answer_dict = solve_A(data = apod_dict)
            print(server_answer_dict)
            time.sleep(2)
            
            data_json = json.dumps(server_answer_dict)
            conn.sendall(data_json.encode('utf-8'))
            print("Done")
        conn.close()

    
if __name__ == "__main__":
    print("Staring Server A")
    main()

