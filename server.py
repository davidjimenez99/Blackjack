import socket, time, random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIp = socket.gethostbyname(hostName)
print(hostName, hostIp)
server.bind((hostName, 4196))
server.listen(3)

deck=['A','2','3','4','5','6','7','8','9','10','J','Q','K']*16               # *4 un deck        *16 cuatro decks
clients=[]
#puntos=[]
#cards=[]

game=True

while game:

    connection, address = server.accept()
    clients.append(connection)
    connection, address = server.accept()
    clients.append(connection)

    server.settimeout(10)                                                    #CAMBIAR A 30
    connection=None
    try:
        connection, address = server.accept()
    except socket.error as exc:
        pass
    server.settimeout(None)

    if connection is not None:
        clients.append(connection)

    st='Welcome to Blackjack!'

    for c in clients:
        c.send(st.encode())

    contCl=1

    for c in clients:

        for x in range(2):
            rand=int(random.randint(0,(len(deck)-1)))
            card=deck[rand]
            print("Jugador",contCl,": ",card)
            deck.remove(card)
            c.send(card.encode())
            time.sleep(1)
        contCl+=1

        time.sleep(1)


        #data=connection.recv(1024)
        #while data is not None:
    contCl=1
    for c in clients:

        while True:
            try:
                data=c.recv(1024)
            except socket.error as exc:
                print("Jugador se ha desconectado")
                break
            #print("ENTRO A WHILE DATA!=NONE")

            inp=data.decode()
            if inp=="hit":
                rand=int(random.randint(0,(len(deck)-1)))
                card=deck[rand]
                print("Jugador",contCl,": ",card)
                deck.remove(card)
                c.send(card.encode())
                time.sleep(1)

            elif inp=="stay":
                st="stay"
                c.send(st.encode())
                #c.close()
                break
                #time.sleep(1)

            else:
                st="Acción incorrecta"
                c.send(st.encode())
                time.sleep(1)

            data=None
        contCl+=1

    print("SALIO DEL WHILE")                                            #COMPARAR PUNTOS DE JUGADORES Y DECIR GANADOR
    game=False


print("ACABÓ")
