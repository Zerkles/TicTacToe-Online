letters_dict = {"a": 0, "b": 1, "c": 2}


def check_wins(table: list, players_dict: dict):
    for i in range(3):
        if table[i][0] != "." and table[i][0] == table[i][1] == table[i][2]:
            return players_dict[table[i][0]]

    for i in range(3):
        if table[0][i] != "." and table[0][i] == table[1][i] == table[2][i]:
            return players_dict[table[0][i]]

    if ((table[0][0] != "." and table[0][0] == table[1][1] == table[2][2]) or (
            table[0][2] != "." and table[0][2] == table[1][1] == table[2][0])):
        return players_dict[table[1][0]]

    for i in range(3):
        for j in range(3):
            if table[i][j] == ".":
                return "none"

    return "tie"


def assign_field(table: list, players_sign: str, field_str: str):
    global letters_dict

    field_str = field_str.lower()
    table_pos = {"x": letters_dict[field_str[0]], "y": int(field_str[1])}

    if table[table_pos["x"]][table_pos["y"]] != ".":
        return False

    table[table_pos["x"]][table_pos["y"]] = players_sign
    return True


def display_table(table: list):
    print("  0 1 2")
    for i in range(0, 3):
        if i == 0:
            print("A " + table[i][0] + " " + table[i][1] + " " + table[i][2])
        elif i == 1:
            print("B " + table[i][0] + " " + table[i][1] + " " + table[i][2])
        elif i == 2:
            print("C " + table[i][0] + " " + table[i][1] + " " + table[i][2])
    print("\n")


if __name__ == "__main__":
    table_glob = [[".", ".", "."], [".", ".", "."], [".", ".", "."], ]
    players_dict_glob = {"X": input("Enter nick one:"), "O": input("Enter nick two:")}

    while check_wins(table_glob, players_dict_glob) != "none":

        display_table(table_glob)
        print(players_dict_glob["X"] + " turn:")

        while not assign_field(table_glob, "X", input()):
            display_table(table_glob)
            print("This field is already assigned!\n")

        if check_wins(table_glob, players_dict_glob) != "none":
            break

        display_table(table_glob)
        print(players_dict_glob["O"] + " turn:")
        while not assign_field(table_glob, "O", input()):
            print("This field is already assigned!\n")

    display_table(table_glob)
    end_cause = check_wins(table_glob, players_dict_glob)
    if end_cause != "tie":
        print("Game ended, " + end_cause + " won!")
    else:
        print("Game ended, you both tied!")
