import socket, time, random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIp = socket.gethostbyname(hostName)
print(hostName, hostIp)
server.bind((hostName, 4196))
server.listen(3)

deck = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']*16                 # *4 un deck        *16 cuatro decks
clients = []

game=True

while game:

    connection, address = server.accept()
    clients.append(connection)
    connection, address = server.accept()
    clients.append(connection)
        
    server.settimeout(5)                                                    #CAMBIAR A 30
    connection = None
    try:
        connection, address = server.accept()
    except socket.error as exc:
        pass
    server.settimeout(None)
    if connection is not None:
        clients.append(connection)

    for i, c in enumerate(clients):
        c.send('Welcome to Blackjack!'.encode())
        time.sleep(1)
        msg = 'Se te ha asignado el turno '+str(i+1)
        c.send(msg.encode())
    
    cards = [[]for y in clients]
    #print(cards)

    contCl = 1
    for c in clients:

        for x in range(2):
            rand = int(random.randint(0,(len(deck)-1)))
            card = deck[rand]
            print("Jugador",contCl,": ",card)
            deck.remove(card)
            cards[contCl-1].append(card)
            c.send(card.encode())
            time.sleep(2)
        contCl += 1
        time.sleep(2)

    contCl = 1

    for i, c in enumerate(clients):

        while True:
            try:
                data = c.recv(1024)
            except socket.error as exc:
                print('Jugador se ha desconectado')
                break
            #print("ENTRO A WHILE DATA!=NONE")

            inp = data.decode()
            if inp == 'hit':
                rand = int(random.randint(0,(len(deck)-1)))
                card = deck[rand]
                print('Jugador',contCl,': ',card)
                deck.remove(card)
                cards[contCl-1].append(card)
                c.send(card.encode())
                time.sleep(2)

            else:
                st = 'stay'
                print('El jugador', (i+1), 'se planta.')
                c.send(st.encode())
                #c.close()
                time.sleep(2)
                break

            data = None

        contCl += 1

    puntos = [0 for x in clients]
    for i, c in enumerate(clients):
        if 'A' in cards[i]:
            cards[i].append(cards[i].pop(cards[i].index('A')))

        for card in cards[i]:
            if card == 'J' or card == 'Q' or card == 'K':
                puntos[i] += 10
            elif card == 'A':
                if puntos[i] <= 10:
                    puntos[i] += 11
                else:
                    puntos[i] += 1
            else:
                puntos[i] += int(card)

    print('puntos:',puntos)           ############################
    perd = []
    gan = []
    for x, punt in enumerate(puntos):
        if punt > 21:
            perd.append(x)
        elif punt <= 21:
            gan.append(x)               #ARREGLAR GANADOR

    print('perdedor:',perd)           ############################
    print('ganador:',gan)             ############################

    for x, c in enumerate(clients):
        if x in perd:
            #print(x,c,perdedor)
            c.send('PERDISTE'.encode())
        else:
            c.send('GANADOR'.encode())
            #print('Jugador', (i+1), 'ha ganado!')

    game=False

print("EL JUEGO TERMINÓ")
