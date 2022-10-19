import socket, json, time

def server_request(server_request_dict, IP_ADDR, PORT):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_ADDR, PORT))
    data_json = json.dumps(server_request_dict)
    s.sendall(data_json.encode('utf-8'))
    data_json = s.recv(1024)
    s.close()
    if data_json:
        apod_dict = json.loads(data_json.decode())
        return apod_dict
    else:
        print("No Answer") 


def solve_B(data):
    k = data.get('k')
    m = data.get('m')
    l = data.get("l")
    n = data.get("n")
    server_request_dict = {"l": l, 
                            "n" : n}
    c = server_request(server_request_dict=server_request_dict, IP_ADDR = "10.1.0.5", PORT = 50003).get('answer')

    B = c + k * (2 + m)
    server_answer_dict = {"answer" : B}
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
            server_answer_dict = solve_B(data = apod_dict)
            print(server_answer_dict)
            time.sleep(2)
            
            data_json = json.dumps(server_answer_dict)
            conn.sendall(data_json.encode('utf-8'))
            print("Done")
        conn.close()

    
if __name__ == "__main__":
    print("Staring Server B")
    main()