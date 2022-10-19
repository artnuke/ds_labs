import socket
import json

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

def main(x, y, k, l ,m, n):
    a = get_A(x, y)
    print (f"A: {a}")
    b = get_B(k,l,m,n)
    print (f"B: {b}")
    f =  a + b 
    print(f"Answer: f(A + B) = {f}")

x = 1
y = 1

k = 1
l = 2
m = 3
n = 4
print("Start")
main(x, y, k, l ,m, n)