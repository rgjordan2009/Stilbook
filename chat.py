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
        global muter
        global muted
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
            '/mutelist':self._mutelist
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

    def _joining(self,param): #indique la presence dans un chatroom/join
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
                #if username=="":
                    #name=input("please choose a username to talk in on the chat: ")
                    #self._nick(name)
                param = username+" : " + param
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
                print("message sent")
            except OSError:
                print('Error during command execution.')
        else:
            print("No port joined yet")

    def _receive(self):
        while self.__running:
            try:
                localtime = time.asctime( time.localtime(time.time()) )
                data, address = self.__s.recvfrom(1024)
                if muter ==1:
                    x=data.decode().split(':')
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
        global username
        username=param

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

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
