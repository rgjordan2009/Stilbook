#!/usr/bin/env python3
# chat.py
# author: Sebastien Combefis
# updater: Jordan Mamanga Lemvo


import socket
import sys
import threading
import time

SERVERADDRESS = (socket.gethostname(), 6000) #Declaration de l'adresse du serveur pour EchoClient


class Chat():
    def __init__(self, host=socket.gethostname(), port=5000):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s = s
        print('Hearing on {}:{}'.format(host, port))
        print('use for :"/help" for help')
        global muter #Variable globale pour pouvoir ignorer un utilisaeur
        global muted #garde en memoire les utilisateurs qui sont bloque
        global CLIENTADDRESS #variable qui garde l'adresse de l'utilisateur
        CLIENTADDRESS = (s.getsockname())
        muted=[]
        muter=0
        global username
        username=""

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/nick': self._nick,
            '/help': self._help,
            '/mute':self._mute,
            '/unmute':self._unmute,
            '/mutelist':self._mutelist,
            '/list':self._list
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
                    print("Error during command execution.")
            else:
                print('Unknown Command:', command)

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
                print('Connected to {}:{}'.format(*self.__address))
                self._joining(" {} joined the port".format(username))
            except OSError:
                print("Error during command execution.")
        else:
            print("Join command could not be executed")

    def _joining(self,param): #indique a l'utilisateur auquel on se connecte qu'on s'est connecte a lui
        if self.__address is not None:
            try:
                param = param
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Error 404')

    def _send(self, param):
        if self.__address is not None:
            try:
                if username=="": #oblige a d'abord choisi un pseudo avant de pouvoir envoyer un message
                    print("please choose a username to talk in on the chat use methode ''/nick'' to choose a username ")
                    print("example: /nick Quentin")

                else:
                    param = username+" : " + param
                    message = param.encode()
                    totalsent = 0
                    print(self.__address)
                    while totalsent < len(message):
                        sent = self.__s.sendto(message[totalsent:], self.__address)
                        totalsent += sent
                    print("message sent")
            except OSError:
                print('AError during command execution.')
        else:
            print("No port joined yet")

    def _receive(self):
        while self.__running:
            try:
                localtime = time.asctime( time.localtime(time.time()) ) #heure et date qui sera envoye avec le msg
                data, address = self.__s.recvfrom(1024)
                if muter ==1:

                    x=data.decode().split(':')
                    print(x)
                    x[0]=x[0].rstrip()
                    if str(x[0]) in muted:
                        pass
                    else:
                        print("{}  sent at {} from IP:{}".format(data.decode(),localtime,address))

                else:
                    print("{}  sent at {} from IP:{}".format(data.decode(),localtime,address))
            except socket.timeout:
                pass
            except OSError:
                return
    def _mute(self,param):
        global muted
        global muter
        muter=1
        muted.append(param)
    def _unmute(self,param):
        if param not in muted:
            print('{} not on the blacklist'.format(param))
            pass
        else:
            if muted == []:
                print('No one is on the blacklist')
            else:
                muted.remove(param)
                print('{} was deleted from blacklist'.format(param))
    def _mutelist(self):
        if muted == []:
            print('No one is on the blacklist')
        else:
            print('Blacklist:')
            for i in muted:
                print(i)
    def _nick(self, param):
       try:
        global username
        username=param
        User=str(param)+str(CLIENTADDRESS) #envoi le pseudo et addresse du client au serveur
        EchoClient(str(User).encode()).run()
       except:
        print("No active server, sorry")
    def _help(self):
        print('Possible commands:')
        print('/exit','to exit the chat application')
        print('/quit','to quit a chatroom')
        print('/join','to join a chat room example:"/join 28.12.18.04 5000"')
        print('/send','to send a message to members of the same chatroom example:"/send Hello World')
        print('/nick','to chose a nickname to chat ;) example:"/nick Fayon')
        print('/mute','to mute an other user example:"/mute Test')
        print('/unmute','to unmute an other user example:"/unmute Test')
        print('/mutelist','to show Blacklist "example:"/mutelist"')
        print('/list','to show online users "example:"/list"')
    def _list(self):
        command=":list:"+str(CLIENTADDRESS)
        EchoClient(str(command).encode()).run()

class EchoClient(): #gere communication avec le serveur
    def __init__(self, message):
        self.__message = message
        self.__s = socket.socket()

    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            self._send()
            self.__s.close()
        except OSError:
            print('ERROR: SERVER SEEMS TO BE NOT JOINABLE')

    def _send(self):
        totalsent = 0
        msg = self.__message
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Error, couldn't send message")

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()

