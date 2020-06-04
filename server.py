import json
import socket

from Player import Player
from logic import find_player_by_sign, check_wins, display_table, socket_input_to_dict, assign_field

if __name__ == "__main__":
    # setting server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 2137))
    server_socket.listen(True)

    table = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    players_dict: dict = {}

    # connect client section
    while len(players_dict.keys()) == 0:
        sck, addr = server_socket.accept()
        received_data = sck.recv(1024)
        if received_data == b'':
            sck.close()
            continue

        msg_json = json.loads(received_data)
        players_dict[msg_json["nickname"]] = Player(msg_json["nickname"], sck, "X")
        sck.send(json.dumps({"msg": "Waiting for other player!", "token":0, "status": "OK"}).encode())

    while len(players_dict) < 2:
        sck, addr = server_socket.accept()
        received_data = sck.recv(1024)
        if received_data == b'':
            sck.close()
            continue

        msg_json = json.loads(received_data)

        if msg_json["nickname"] in players_dict.keys():
            sck.send(json.dumps({"msg": "This nickname is already taken!", "token":0, "status": "NOK"}).encode())
            sck.close()
        else:
            players_dict[msg_json["nickname"]] = Player(msg_json["nickname"], sck, "O")
            sck.send(json.dumps({"msg": "Waiting for other player!", "token": 0, "status": "OK"}).encode())

    print(players_dict.keys())

    player1 = find_player_by_sign(players_dict, "X")
    player2 = find_player_by_sign(players_dict, "O")

    while check_wins(table, players_dict) != "none":

        display_table(table)

        print(player1.nickname + " turn:")
        player1.socket.send(json.dumps({"table": table, "token": 1, "msg": "Make a move"}))
        player2.socket.send(json.dumps({"table": table, "token": 0, "msg": "Wait for other player"}))

        response = socket_input_to_dict(player1.socket)
        while not assign_field(table, player1.sign, response["move"]):
            player1.socket.send(json.dumps({"table": table, "status": "NOK", "msg": "This field is already assigned!"}))
            response = socket_input_to_dict(player1.socket)
            print("This field is already assigned!\n")
        player1.socket.send(json.dumps({"table": table, "status": "OK", "msg": "Wait for other player!"}))


        if check_wins(table, players_dict) != "none":
            break

        display_table(table)

        print(player2.nickname + " turn:")
        player2.socket.send(json.dumps({"table": table, "token": 1, "msg": "Make a move"}))
        player1.socket.send(json.dumps({"table": table, "token": 0, "msg": "Wait for other player"}))

        response = socket_input_to_dict(player1.socket)
        while not assign_field(table, player2.sign, response["move"]):
            player2.socket.send(json.dumps({"table": table, "status": "NOK", "msg": "This field is already assigned!"}))
            response = socket_input_to_dict(player1.socket)
            print("This field is already assigned!\n")
        player1.socket.send(json.dumps({"table": table, "status": "OK", "msg": "Wait for other player!"}))

    display_table(table)
    end_cause = check_wins(table, players_dict)
    if end_cause != "tie":
        player2.socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, player" + end_cause + " won!"}))
        player1.socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, player" + end_cause + " won!"}))
        print("Game ended, player" + end_cause + " won!")
    else:
        player2.socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you both tied!"}))
        player1.socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you both tied!"}))
        print("Game ended, you both tied!")

    player1.socket.close()
    player2.socket.close()
