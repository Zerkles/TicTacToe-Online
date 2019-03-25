import socket
from random import randint

def check_wins():
    for i in range(3):
       if(table[i][0]!= "." and table[i][0]==table[i][1]==table[i][2]):
           if(table[i][0]=="X"):
               return nick1
           else:
               return nick2

    for i in range(3):
       if(table[0][i]!="." and table[0][i]==table[1][i]==table[2][i]):
           if (table[0][i] == "X"):
               return nick1
           else:
               return nick2

    if((table[0][0]!="." and table[0][0]==table[1][1]==table[2][2]) or (table[0][2]!="." and table[0][2]==table[1][1]==table[2][0])):
        if (table[1][1] == "X"):
            return nick1
        else:
            return nick2

    for i in range(3):
        for j in range(3):
            if (table[i][j]=="."):
                return "none"

    return "tie"

def assign_field(player,field):
    if (player == nick1):
        sign = "X"
    else:
        sign = "O"

    if ("A" in field or "a" in field):
        if ("0" in field):
            if(table[0][0] == "."):
                table[0][0] = sign
                return True
            else:
                return False
        elif ("1" in field):
            if(table[0][1] == "."):
                table[0][1] = sign
                return True
            else:
                return False
        elif ("2" in field):
            if(table[0][2] == "."):
                table[0][2] = sign
                return True
            else:
                return False

    elif ("B" in field or "b" in field):
        if ("0" in field):
            if(table[1][0] == "."):
                table[1][0] = sign
                return True
            else:
                return False
        elif ("1" in field):
            if(table[1][1] == "."):
                table[1][1] = sign
                return True
            else:
                return False
        elif ("2" in field):
            if(table[1][2] == "."):
                table[1][2] = sign
                return True
            else:
                return False

    elif ("C" in field or "c" in field):
        if ("0" in field):
            if(table[2][0] == "."):
                table[2][0] = sign
                return True
            else:
                return False
        elif ("1" in field):
            if(table[2][1] == "."):
                table[2][1] = sign
                return True
            else:
                return False
        elif ("2" in field):
            if(table[2][2] == "."):
                table[2][2] = sign
                return True
            else:
                return False
    return False

def display_table():
    print("  0 1 2")
    for i in range(0,3):
       if(i==0):
           print("A "+table[i][0] + " " + table[i][1] + " " + table[i][2])
       elif (i == 1):
           print("B " + table[i][0] + " " + table[i][1] + " " + table[i][2])
       elif (i == 2):
           print("C " + table[i][0] + " " + table[i][1] + " " + table[i][2])
    print("\n")





table=[[".",".","."],[".",".","."],[".",".","."],]
nick1=input("Enter nick one:")
nick2=input("Enter nick two:")

while(check_wins()=="none" or check_wins=="tie"):

    display_table()
    print(nick1+" turn:")

    while(not assign_field(nick1,input())):
        print("This field is already assigned!\n")

    if(check_wins()!="none"):
        break

    display_table()
    print(nick2 + " turn:")
    while(not assign_field(nick2, input())):
        print("This field is already assigned!\n")


display_table()
if(check_wins()!="tie"):
    print("Game ended, "+check_wins()+" won!")
else:
    print("Game ended, you both tied!")