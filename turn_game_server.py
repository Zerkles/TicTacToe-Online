import socket
import json
from Player import Player
from logic import *

def make_move(table, player):
    print(player.nickname + " turn:")
    player.socket.send(json.dumps({"table": table, "token": 1, "msg": "Make a move"}).encode('utf-8'))

    response = socket_input_to_dict(player.socket)
    while not assign_field(table, player.sign, response["move"]):
        player.socket.send(json.dumps({"table": table, "status": "NOK", "msg": "This field is already assigned!"}).encode('utf-8'))
        response = socket_input_to_dict(player.socket)
        print("This field is already assigned!\n")
    player.socket.send(json.dumps({"table": table, "status": "OK", "token":0, "msg": "Wait for other player!"}).encode('utf-8'))

def wait_for_players(server_socket:socket, players_count: int) -> dict:
    players_dict= dict()

    while len(players_dict) < players_count:
        sck, addr = server_socket.accept()
        received_data = sck.recv(1024)
        if received_data == b'':
            sck.close()
            continue

        msg_dict = socket_input_to_dict(sck)

        while msg_dict["nickname"] in players_dict.keys():
            sck.send(json.dumps({"msg": "This nickname is already taken!", "status": "NOK"}).encode())
            msg_dict = socket_input_to_dict(sck.recv(1024))
        
        players_dict[msg_dict["nickname"]] = Player(msg_dict["nickname"], sck, "-1")
        sck.send(json.dumps({"msg": "Waiting for other player!", "token": 0, "status": "OK"}).encode())

    print(list(players_dict.values()))
    return list(players_dict.values())
