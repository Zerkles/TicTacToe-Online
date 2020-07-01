import json
import socket as socket
import turn_game_server as engine


from Player import Player
from logic import find_player_by_sign, check_wins, display_table, socket_input_to_dict, assign_field

if __name__ == "__main__":
    # setting server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 2137))
    server_socket.listen(True)

    table = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    players_list = engine.wait_for_players(server_socket, 2)

    players_list[0].sign='X'
    players_list[1].sign='O'

    players_list[1].socket.send(json.dumps({"table": table, "token": 0, "msg": "Wait for other player"}).encode())

    while check_wins(table, players_list) == -1:

        display_table(table)
        engine.make_move(table,players_list[0])


        if check_wins(table, players_list) != -1:
            break

        display_table(table)
        engine.make_move(table,players_list[1])

    display_table(table)
    end_code = check_wins(table, players_list)
    
    if end_code == 3:
        players_list[0].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you both tied!"}).encode('utf-8'))
        players_list[1].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you both tied!"}))
        print("Game ended, you both tied!")
    elif end_code == 0:
        players_list[0].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you won!"}).encode('utf-8'))
        players_list[1].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you lost!"}).encode('utf-8'))
        print("Game ended, player" + players_list[0].nickname + " won!")
    else:
        players_list[1].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you won!"}).encode('utf-8'))
        players_list[0].socket.send(json.dumps({"table": table, "token": 3, "msg": "Game ended, you lost!"}).encode('utf-8'))
        print("Game ended, player" + players_list[1].nickname + " won!")


    players_list[0].socket.close()
    players_list[1].socket.close()
