import socket


class Player:
    socket: socket = None
    nickname = ""
    sign = ""
    token = 0

    def __init__(self, nickname: str, sck: socket, sign:str):
        self.nickname = nickname
        self.socket = sck
        self.sign = sign
