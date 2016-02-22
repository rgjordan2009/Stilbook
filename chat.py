#!/usr/bin/env python3
# chat.py
# author: Sebastien Combefis
# updater: Jordan Mamanga Lemvo


import socket
import sys
import threading
import time

class Chat():
    def __init__(self, host=socket.gethostname(), port=5000):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s = s
        print('Hearing on {}:{}'.format(host, port))
        print('use for :"/help" for help')
        global username
        username=""

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/nick': self._nick,
            '/help': self._help
        }
        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur lors de l'execution de la commande.")
            else:
                print('Command inconnue:', command)

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (socket.gethostbyaddr(tokens[0])[0], int(tokens[1]))
                print('Connecte a {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")

    def _send(self, param):
        if self.__address is not None:
            try:
                if username=="":
                    name=input("please choose a username to talk in on the chat: ")
                    self._nick(name)
                param = username+" : " + param
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
                print("message sent")
            except OSError:
                print('Erreur lors de la reception du message.')

    def _receive(self):
        while self.__running:
            try:
                localtime = time.asctime( time.localtime(time.time()) )
                data, address = self.__s.recvfrom(1024)

                print("{}  sent at {} from IP:{}".format(data.decode(),localtime,address))
            except socket.timeout:
                pass
            except OSError:
                return
    def _nick(self, param):
        global username
        username=param
    def _help(self):
        print('Possible commands:')
        print('/exit','to exit the chat application')
        print('/quit','to quit a chatroom')
        print('/join','to join a chat room example:"/join 28.12.18.04 5000"')
        print('/send','to send a message to members of the same chatroom example:"/send Hello World')
        print('/nick','to chose a nickname to chat ;) example:"/nick Fayon')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
