import json
import socket

from logic import socket_input_to_dict, display_table

if __name__ == "__main__":
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect(('127.0.0.1', 2137))
    
    # connecting to server and setting nickname
    data_dict = {"status":"NOK"}
    while data_dict["status"] == "NOK":
        sck.sendall(json.dumps({"nickname": input("Type in nickname: ")}).encode('utf-8'))
        data_dict = socket_input_to_dict(sck)
        print(data_dict["msg"])

    print(data_dict)
    while data_dict["token"] != 3:
        data_dict = socket_input_to_dict(sck)
        print(data_dict["msg"])
        display_table(data_dict["table"])

        if data_dict["token"] == 0 or data_dict["token"] == 3:
            continue

        sck.sendall(json.dumps({"move": input("Type in move: ")}).encode('utf-8'))
        data_dict = socket_input_to_dict(sck)
        while data_dict["status"] == "NOK":
            data_dict = socket_input_to_dict(sck)
            sck.sendall(json.dumps({"move": input("Type in move: ")}).encode('utf-8'))
        display_table(data_dict["table"])

    print(data_dict["msg"])

    sck.close()

