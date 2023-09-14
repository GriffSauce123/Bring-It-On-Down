# So Far So Good

# make waiting for connection screen work

import socket
import threading

clients = [] # a list of lists of addrs linked in games Example [('192.111.111.4', '222.222.222.6'), ('182.1151.331.4', '236.482.291.6')]

def main():
	global clients
	listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip = 'localhost'#'192.168.0.247' # IP OF THE COMPUTER HOSTING THE SERVER
	port = 10003 # A CLEAR PORT TO USE
	
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listener.bind((ip, port))
	temp_ls = []

	while True:
		try:
			message, addr = listener.recvfrom(1024)
			data = message.decode()			
			print(f'Total Clients: {clients})')

			#adding the client to the list to determine each game. Checking if the addr is in the list already because this is the main listener thread
			#checks if client is in the nested list
			if not any(addr in sl for sl in clients):
				
				if len(temp_ls) < 2:
					temp_ls.append(addr)
					if len(temp_ls) == 2:
						clients.append(temp_ls)
						temp_ls = []

			elif any(addr in sl for sl in clients):
				
				#finds the indecies of the client within the lsit (outer index, inner index)
				indecies = [(i, el.index(addr)) for i, el in enumerate(clients) if 2 in el]
				temp_client = addr
				#the paired client (player "2")
				temp_opp = clients[indecies[0]][indecies[1]]

				#checking for disonnections
				if data == 'disconnect':
					clients.remove(indecies[0])
					print(f'[ {addr} and {temp_opp} DISCONNECTED ]')
					listener.sendto(message, temp_opp)

				#client asks for team assignment - the one who connected first is always team -1 and the second is always 1
				if data == 'team':
					listener.sendto(str(indecies[1] - 1).encode(), addr)
					print(f'BROADCASTING: {indecies[1] - 1} To {addr}')

				#updating the game board for the other clients screen
				if '.' in data:
					listener.sendto(message, temp_opp)
					print(f'BROADCASTING: {data} To {temp_opp}')
		
				#change turn request
				if data == 'turn':
					listener.sendto(message, temp_opp)
					print(f'BROADCASTING: {data} To {temp_opp}')
					
				#updating the dice to display on the other clients screen
				if 'dice' in data:
					listener.sendto(message, temp_opp)
					print(f'BROADCASTING: {data} To {temp_opp}')

		except Exception as e:
			print(e)
			print(f'DISCONNECTED: {addr}')
			for ls in clients:
				if addr in ls:
					clients.remove(ls)

if __name__ == '__main__':
	main()
