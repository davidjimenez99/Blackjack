import socket, time, random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIp = socket.gethostbyname(hostName)
print(hostName, hostIp)
server.bind((hostName, 4196))
server.listen(3)

deck=['A','2','3','4','5','6','7','8','9','10','J','Q','K']*16                 # *4 un deck        *16 cuatro decks
clients=[]

game=True

while game:

    connection, address = server.accept()
    clients.append(connection)
    connection, address = server.accept()
    clients.append(connection)

    server.settimeout(1)                                                    #CAMBIAR A 30
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

    
 


    cards=[[]for y in clients]
    #print(cards)


    contCl=1
    for c in clients:

        for x in range(2):
            rand=int(random.randint(0,(len(deck)-1)))
            card=deck[rand]
            print("Jugador",contCl,": ",card)
            deck.remove(card)

            cards[contCl-1].append(card)

            c.send(card.encode())
            time.sleep(1)
        contCl+=1

        time.sleep(1)



    #print(cards)

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
                cards[contCl-1].append(card)
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


    puntos=[0 for x in clients]
    contCl=1
    for c in clients:
        if 'A' in cards[contCl-1]:
            cards[contCl-1].append(cards[contCl-1].pop(cards[contCl-1].index('A')))

        for card in cards[contCl-1]:
            if card=='J' or card=='Q' or card=='K':
                puntos[contCl-1]+=10
            elif card=='A':
                if puntos[contCl-1]<=10:
                    puntos[contCl-1]+=11
                else:
                    puntos[contCl-1]+=1
            else:
                puntos[contCl-1]+=int(card)


    #print(puntos)
    perd=[]
    gan=[]
    for x, punt in enumerate(puntos):
        if punt > 21:
            perd.append(x)
        elif punt <= 21:
            gan.append(x)               #ARREGLAR GANADOR

    perdedor="PERDISTE"
    ganador="GANADOR"
    for x, c in enumerate(clients):
        if x in perd:
            #print(x,c,perdedor)
            c.send(perdedor.encode())
        else:
            c.send(ganador.encode())


    print("SALIO DEL WHILE")                                            #COMPARAR PUNTOS DE JUGADORES Y DECIR GANADOR

    #print(cards)

    game=False


print("ACABÓ")
