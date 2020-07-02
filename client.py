import socket

from game_logic import display_table
from multiplayer_logic import read_socket_to_dict, write_socket_from_dict

if __name__ == "__main__":
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect(('127.0.0.1', 2137))

    messages_buffer = b''

    # connecting to server and setting nickname
    data_dict = {"token": 1}
    while data_dict["token"] == 1:
        write_socket_from_dict(sck, {"nickname": input("Type in nickname: ")})
        messages_buffer, data_dict = read_socket_to_dict(sck, messages_buffer)
        print(data_dict["msg"])

    while data_dict["token"] != 3:
        messages_buffer, data_dict = read_socket_to_dict(sck, messages_buffer)

        if data_dict["token"] == 0:
            print(data_dict["msg"])
        elif data_dict["token"] == 1:
            print(data_dict["msg"])
            display_table(data_dict["table"])
            while data_dict["token"] == 1:
                write_socket_from_dict(sck, {"move": input("Type in move: ")})
                messages_buffer, data_dict = read_socket_to_dict(sck, messages_buffer)
                display_table(data_dict["table"])
                print(data_dict["msg"])

    display_table(data_dict["table"])
    print(data_dict["msg"])
    sck.close()
