def game_finished(table: list, players_list: list) -> int:  # 0-win p0; 1-win p1; 3-tie; 4-not finished
    for i in range(3):
        if table[i][0] != "." and table[i][0] == table[i][1] == table[i][2]:
            return player_id_by_sign(players_list, table[i][0])

    for i in range(3):
        if table[0][i] != "." and table[0][i] == table[1][i] == table[2][i]:
            return player_id_by_sign(players_list, table[0][i])

    if ((table[0][0] != "." and table[0][0] == table[1][1] == table[2][2]) or (
            table[0][2] != "." and table[0][2] == table[1][1] == table[2][0])):
        return player_id_by_sign(players_list, table[1][1])

    for i in range(3):
        for j in range(3):
            if table[i][j] == ".":
                return -1

    return 3


def assign_field(table: list, players_sign: str, field_str: str):
    letters_dict = {"a": 0, "b": 1, "c": 2}

    if len(field_str) > 2 or field_str[0] not in letters_dict.keys() or int(field_str[1]) not in letters_dict.values():
        return False

    field_str = field_str.lower()
    table_pos = {"x": letters_dict[field_str[0]], "y": int(field_str[1])}

    if table[table_pos["x"]][table_pos["y"]] != ".":
        return False

    table[table_pos["x"]][table_pos["y"]] = players_sign
    return True


def display_table(table: list):
    print("__________")
    print("  0 1 2")
    for i in range(0, 3):
        if i == 0:
            print("A " + table[i][0] + " " + table[i][1] + " " + table[i][2])
        elif i == 1:
            print("B " + table[i][0] + " " + table[i][1] + " " + table[i][2])
        elif i == 2:
            print("C " + table[i][0] + " " + table[i][1] + " " + table[i][2])
    print("__________")


def player_id_by_sign(players_list: list, sign: str) -> int:
    for player in players_list:
        if player.sign == sign:
            return players_list.index(player)
