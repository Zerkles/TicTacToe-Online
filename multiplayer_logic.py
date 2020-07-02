import json
import socket

from Player import Player
from game_logic import *


def make_move(table, player, messages_buffer: bytes):
    write_socket_from_dict(player.socket, {"table": table, "token": 1, "msg": "Your turn!"})

    messages_buffer, response = read_socket_to_dict(player.socket, messages_buffer)
    while not assign_field(table, player.sign, response["move"]):
        write_socket_from_dict(player.socket, {"table": table, "token": 1, "msg": "Illegal move!"})
        messages_buffer, response = read_socket_to_dict(player.socket, messages_buffer)

    write_socket_from_dict(player.socket, {"table": table, "token": 0, "msg": "Wait for the other player."})


def wait_for_players(server_socket: socket, players_count: int, messages_buffer: bytes) -> list:
    players_dict = dict()

    while len(players_dict) < players_count:
        sck, addr = server_socket.accept()
        messages_buffer, msg_dict = read_socket_to_dict(sck, messages_buffer)

        while msg_dict["nickname"] in players_dict.keys():
            write_socket_from_dict(sck, {"msg": "This nickname is already taken!", "token": 1})
            messages_buffer, msg_dict = read_socket_to_dict(sck, messages_buffer)

        players_dict[msg_dict["nickname"]] = Player(msg_dict["nickname"], sck, "-1")
        write_socket_from_dict(sck, {"msg": "Waiting for the other player.", "token": 0})

    players_list = list(players_dict.values())
    write_socket_from_dict(players_list[0].socket,
                           {"msg": f"{players_list[1].nickname} will be your opponent!", "token": 0})
    write_socket_from_dict(players_list[1].socket,
                           {"msg": f"{players_list[0].nickname} will be your opponent!", "token": 0})

    return players_list


def read_socket_to_dict(sck: socket, buffer: bytes) -> [bytes, dict]:
    if buffer == b'':
        buffer = sck.recv(1024)

    end_of_json = buffer.find(b'}') + 1
    msg = buffer[0:end_of_json]
    buffer = buffer[end_of_json:]
    return buffer, dict(json.loads(msg))


def write_socket_from_dict(sck: socket, data: dict):
    sck.send(json.dumps(data).encode('utf-8'))
