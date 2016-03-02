#!/usr/bin/env python3
# echo.py
# author: Sebastien Combefis
# updater: Jordan Mamanga Lemvo


import socket
import sys

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        print("Utilisateur en ligne")
        global Clientlist # contient les utilisateurs en ligne
        global ADDRESS #contient l'addresse de l'utilsateurs
        Clientlist=[]

    def run(self):
        self.__s.listen(0)
        while True:
            client, addr = self.__s.accept()
            global Clientlist
            try:
                user=self._receive(client).decode().rstrip() # contient l'instruction de l'utilisateur
                if ":list:" in user: #repere la fonction liste à l'aide de la chaine de caractere :list:
                    global ADDRESS
                    ADDRESS=str(user.rsplit(':')[2])
                    self._send() #renvoi la liste des clients en ligne
                if user not in Clientlist and ":list:" not in user : #pas de doublons dans la liste des clients en ligne(meme addresse et IP)
                     Clientlist.append(user)
                client.close()
            except OSError:
                print('Erreur lors de la reception du message.')

    def _receive(self, client):
        chunks = []
        finished = False

        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def _send(self):
        totalsent = 0
        if len(Clientlist)==0: #aucun client en lige
            msg="Online Users: None"
        else:
            msg="Online Users:\n"
        for i in Clientlist:
            msg+=i+"\n"

        t=socket.socket(type=socket.SOCK_DGRAM)
        t.bind(SERVERADDRESS)
        #Traitement de l'address, on extrait l'addresse de la requete du client et on separe port et ip
        x=ADDRESS
        x=x[1:]
        a=x[:-1]
        Ip=a.split(',')[0]
        Ip=Ip[1:]
        Ip=Ip[:-1]
        port=int(a.split(',')[1])
        ad=(Ip,port) #tuple avec port et ip

        #boucle d'envoi a tout les clients actifs...
        try:
            while totalsent < len(msg):
                sent = t.sendto(msg[totalsent:], ad)
                totalsent += sent
            t.close()
        except OSError:
            print("Erreur lors de l'envoi du message.")
            t.close()




EchoServer().run()