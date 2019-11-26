import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.0.13"
port = 8080
#port = 8080

try:
    client.connect((host, port))
except socket.error as exc:
    print("En este momento no se puede conectar al juego")
    exit()

cards=[]

def sortCards(cards):
    if 'A♦' in cards:
        cards.append(cards.pop(cards.index('A♦')))
    elif 'A♣' in cards:
        cards.append(cards.pop(cards.index('A♣')))
    elif 'A♥' in cards:
        cards.append(cards.pop(cards.index('A♥')))
    elif 'A♠' in cards:
        cards.append(cards.pop(cards.index('A♠')))

def count():
    puntos=0
    sortCards(cards)
    for card in cards:
        if 'J' in card or 'Q' in card or 'K' in card:
            puntos += 10
        elif 'A' in card:
            if puntos <= 10:
                puntos += 11
            else:
                puntos += 1
        else:
            puntos += int(card[:-1])
    return puntos

def decide(puntos, client):
    if puntos < 17:
        client.send("hit".encode())
    else:
        client.send("hold".encode())


while True:
    data = client.recv(1024).decode()
    if '?' in data:
        puntos = count()                                    #Método para contar los puntos que tiene
        #print("Tus cartas son: ", cards, " = ", puntos)
        decide(puntos, client)                              #Método para decidir si se queda o pide otra
        #break
    elif '♦' in data or '♣' in data or '♥' in data or '♠' in data:
        cards.append(data)
        #print(data)
        puntos = count() 
        print("Tus cartas son: ", cards, " = ", puntos)
    elif 'kill' in data:
        break
    else:
        print(data)
        
    
client.close()