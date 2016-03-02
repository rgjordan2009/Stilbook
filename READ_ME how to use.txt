1) Lancer script du serveur
2) Lancer script du chat avec le port, sinon port 5000 par défaut
exemple: chat.py localhost 6000
 (sur deux terminal different pour pouvoir chatter à 2 ou plus )
3) choisir nom d’utilisateur avec méthode « /nick » exemple /nick sébastien.      n.b: Pas d’accent Python à du mal avec les accents sorry.
4) utiliser méthode /list obtenir liste des utilisateurs en ligne
5) se connecter a un autre utilisateur avec /join localhost  example: /join localhost 4242
6) Chatter avec méthode /send

en cas de problème utiliser la méthode /help

Le protocole de communication utiliser entre le serveur et le client est en TCP,
adéquat pour la communication entre serveur et client. n.b: Une parti du serveur « echo.py » est en UDP par facilité (parti envoi)

Caractéristiques du Transmission Control Protocol:	Transfert fiable (réception et ordre garantis)	Avec connexion (protocole lourd)	Adapté à l’architecture client/serveur

Le protocole de communication utiliser entre entre utilisateur et le utilisateur est en UDP adéquat pour la communication entre ordinateur surtout en local:
Caractéristiques du User Datagram Protocol:
	Transfert non fiable (réception et ordre non garantis)	Sans connexion (protocole léger)	Adapté à l’architecture peer-to-peer


Credits: Sébastien Combéfis(squelette du code)
	  Jordan Mamanga Lemvo (update)
	  Julien Stilmant(update)