import json
import socket

import multiplayer_logic as engine
from game_logic import game_finished, display_table

if __name__ == "__main__":
    # setting server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 2137))
    server_socket.listen(True)
    print("Server started!")

    table = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    messages_buffer = b''
    players_list = engine.wait_for_players(server_socket, 2, messages_buffer)

    players_list[0].sign = 'X'
    players_list[1].sign = 'O'

    while game_finished(table, players_list) == -1:

        display_table(table)
        engine.make_move(table, players_list[0], messages_buffer)

        if game_finished(table, players_list) != -1:
            break

        display_table(table)
        engine.make_move(table, players_list[1], messages_buffer)

    display_table(table)
    end_code = game_finished(table, players_list)

    if end_code == 3:
        players_list[0].socket.send(
            json.dumps({"table": table, "token": 3, "msg": "Game ended, you both tied!"}).encode('utf-8'))
        players_list[1].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you both tied!"}))
        print("Game ended, you both tied!")
    elif end_code == 0:
        players_list[0].socket.send(
            json.dumps({"table": table, "token": 3, "msg": "Game ended, you won!"}).encode('utf-8'))
        players_list[1].socket.send(
            json.dumps({"table": table, "token": 3, "msg": "Game ended, you lost!"}).encode('utf-8'))
        print("Game ended, player " + players_list[0].nickname + " won!")
    else:
        players_list[1].socket.send(
            json.dumps({"table": table, "token": 3, "msg": "Game ended, you won!"}).encode('utf-8'))
        players_list[0].socket.send(
            json.dumps({"table": table, "token": 3, "msg": "Game ended, you lost!"}).encode('utf-8'))
        print("Game ended, player " + players_list[1].nickname + " won!")

    players_list[0].socket.close()
    players_list[1].socket.close()
