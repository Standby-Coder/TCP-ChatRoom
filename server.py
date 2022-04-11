import socket

import threading  #for threading



#define a host address and port for our server

host = '127.0.0.1' #since we will be maintaining and running the server on our local host we use the local host address as host address


port = 5552

details = (host,port)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(details)

server.listen()  #server starts listening for new connections


clients = []

names = []


#broadcast method

def broadcast(message):
	for client in clients:	
		client.send(message)


#handle client

def handle(client):
	while True:
		try:
			msg = message = client.recv(1024)
			if msg.decode('ascii').startswith('KICK'):
				if names[clients.index(client)] == 'admin':
					kickname = msg.decode('ascii')[5:]
					kickuser(kickname)
				else:
					client.send("Command refused!".encode('ascii'))
			elif msg.decode('ascii').startswith('BAN'):
				if names[clients.index(client)] == 'admin':
					banname = msg.decode('ascii')[4:]
					kickuser(banname)
					with open('banned.txt','a') as f:
						f.write(f'{banname}\n')
					print(f'{banname} was banned!')
				else:
					client.send("Command refused!".encode('ascii'))
			else:
				broadcast(message)
		
		except : #disconnect the client if something unexpected happen
			if client in clients:
				index = clients.index(client)
				clients.remove(client)
				broadcast(f'{name} left the chat\n'.encode('ascii'))
				client.close()
				name = names[index]
				names.remove(name)
				break



#integrating the above methods

def receive():
	while True:
		client , address = server.accept()
		print(f"A client connected with {str(address)}\n")
		client.send('NAME'.encode('ascii'))
		name = client.recv(1024).decode('ascii')
		with open('banned.txt','r') as f:
			bans = f.readlines()

		if name+'\n' in bans:
			client.send('BAN'.encode('ascii'))
			client.close()
			continue

		if name == 'admin':
			client.send('PASS'.encode('ascii'))
			password = client.recv(1024).decode('ascii')

			if password != 'adminpass':
				client.send('ACCESS DENIED'.encode('ascii'))
				client.close()
				continue

		names.append(name)
		clients.append(client)
		print(f'name of the client is {name}\n')
		broadcast(f'{name} joined the chat\n'.encode('ascii'))
		client.send("Connected to the server ! Time to chat\n".encode('ascii'))
		thread = threading.Thread(target= handle, args=(client,))
		thread.start()

def kickuser(kickname):
	if kickname in names:
		idx = names.index(kickname)
		kickclient = clients[idx]
		clients.remove(kickclient)
		kickclient.send("You were kicked by an admin!".encode('ascii'))
		kickclient.close()
		names.remove(kickname)
		broadcast(f'{kickname} was kicked by an admin!'.encode('ascii'))

print("Server is listenting...")

receive()

