import socket, time, random, threading
'''
def threadCountdown(name):
    tiempo = 30
    for x in range(30):
        print('El juego comienza en', tiempo, 'segundos')
        tiempo -= 1
        time.sleep(1)
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIp = socket.gethostbyname(hostName)
print(hostName, hostIp)
server.bind((hostName, 8080))
server.listen(3)

deck = ['A♦','2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♣','2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♥','2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♠','2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠']*4
clients = []

game=True

while game:

    connection, address = server.accept()
    clients.append(connection)
    connection, address = server.accept()
    clients.append(connection)

    #t = threading.Thread(target=threadCountdown, args=(1,))
    #t.start()

    server.settimeout(30)                                                    #CAMBIAR A 30
    connection = None
    try:
        connection, address = server.accept()
    except socket.error as exc:
        pass
    server.settimeout(None)
    if connection is not None:
        clients.append(connection)
        #DETENER THREAD

    for i, c in enumerate(clients):
        msg = 'Se te ha asignado el turno '+str(i+1)
        c.send(msg.encode())
    
    cards = [[]for y in clients]

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
        time.sleep(1)

    contCl = 1

    for i, c in enumerate(clients):

        while True:

            c.send("?".encode())

            try:
                data = c.recv(1024)
            except socket.error as exc:
                print('Jugador se ha desconectado')
                break

            inp = data.decode()
            if inp == 'hold':
                print('El jugador', (i+1), 'se planta.')
                #c.close()
                time.sleep(2)
                break

            else:
                rand = int(random.randint(0,(len(deck)-1)))
                card = deck[rand]
                print('Jugador',contCl,': ',card)
                deck.remove(card)
                cards[contCl-1].append(card)
                c.send(card.encode())
                time.sleep(2)

            data = None

        contCl += 1

    puntos = [0 for x in clients]
    for i, c in enumerate(clients):
        if 'A♦' in cards[i]:
            cards[i].append(cards[i].pop(cards[i].index('A♦')))
        elif 'A♣' in cards[i]:
            cards[i].append(cards[i].pop(cards[i].index('A♣')))
        elif 'A♥' in cards[i]:
            cards[i].append(cards[i].pop(cards[i].index('A♥')))
        elif 'A♠' in cards[i]:
            cards[i].append(cards[i].pop(cards[i].index('A♠')))

        for card in cards[i]:
            if card[:-1] == 'J' or card[:-1] == 'Q' or card[:-1] == 'K':
                puntos[i] += 10
            elif card[:-1] == 'A':
                if puntos[i] <= 10:
                    puntos[i] += 11
                else:
                    puntos[i] += 1
            else:
                puntos[i] += int(card[:-1])

    perd = []
    gan = []
    for x, punt in enumerate(puntos):
        if punt > 21:
            perd.append(x)
        elif punt <= 21:
            gan.append(x)               #ARREGLAR GANADOR

    #print('perdedor:',perd)                          ############################
    #print('ganador:',gan)                            ############################

    for x, c in enumerate(clients):
        if x in perd:
            #print(x,c,perdedor)
            c.send('HAS PERDIDO!'.encode())
            #print('Jugador', (i+1), 'ha perdido!')
        else:
            c.send('HAS GANADO!'.encode())
            #print('Jugador', (i+1), 'ha ganado!')
        c.send('kill'.encode())


    game=False

print('El jugador ### ha ganado!')