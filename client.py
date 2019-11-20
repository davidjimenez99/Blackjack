import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.32.152.32'
port = 4196
try:
    client.connect((host, port))
except socket.error as exc:
    print("En este momento no se puede conectar al juego")
    exit()

data = client.recv(1024)
print(data.decode())

data = client.recv(1024)
print(data.decode())

cards=[]

for x in range(2):
    data=client.recv(1024)
    cards.append(data.decode())
    print(data.decode())

while True:

    puntos=0

    if 'A' in cards:
        cards.append(cards.pop(cards.index('A')))

    for card in cards:
        if card == 'J' or card == 'Q' or card == 'K':
            puntos += 10
        elif card == 'A':
            if puntos <= 10:
                puntos += 11
            else:
                puntos += 1
        else:
            puntos += int(card)

    print("Tus cartas son: ", cards, " = ", puntos)

    if puntos < 17:
        client.send("hit".encode())
    else:
        client.send("stay".encode())

    data=client.recv(1024)
    data=data.decode()

    if data=="stay":
        #print("Tus cartas son: ", cards, "= ", puntos)                      #QUITAR
        #exit()                                                              #Recibir info si ganó o perdió
        break
    else:
        cards.append(data)
        print(data)

data=client.recv(1024)
print(data.decode())
    
    
client.close()