import socket

import threading

import time

from datetime import datetime #for printing date and time of message 


name = input("Choose a name: ")

if name == 'admin':
	password = input("Enter password for admin : ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5552

details = (host,port)

client.connect(details)

#define two methods
stop_thread = False
def receive():
	while True:
		global stop_thread
		if stop_thread:
			break
		try:
			message = client.recv(1024).decode('ascii')

			if(message == "NAME"):
				client.send(name.encode('ascii'))
				next_message = client.recv(1024).decode('ascii')
				
				if next_message == 'PASS':
					client.send(password.encode('ascii'))
					
					if(client.recv(1024).decode('ascii')) == 'ACCESS DENIED':
						print('Connection refused by server! Wrong Password!')
						stop_thread = True
				
				elif next_message == "BAN":
					print('Connection refused! User Banned!')
					client.close()
					stop_thread = True
			
			else:
				print(message)
		
		except:
			print("An error occured")
			client.close()
			break

def write():

	while 1:
		if stop_thread:
			break
		second = time.time()
		date_time = datetime.fromtimestamp(second)
		message = f'{"["+str(date_time)[:19]+"]"} {name} : {input("")}'

		if message[(len(name)+25):].startswith('/'):
			
			if name == 'admin':
				
				if message[(len(name)+25):].startswith('/kick'):
					client.send(f'KICK {message[(len(name)+31):]}'.encode('ascii'))
				
				elif message[(len(name)+25):].startswith('/ban'):
					client.send(f'BAN {message[(len(name)+30):]}'.encode('ascii'))
			
			else:
				print('Commands can be executed by admin only')
		
		else:
			client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=  write)
write_thread.start()





