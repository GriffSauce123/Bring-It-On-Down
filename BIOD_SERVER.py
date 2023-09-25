# make server not use a seperate thread for every 2 users :(
# MAKE DIRECT CONNECT WORK
# ideally there is one listener thread, and a broadcast thread for every game (clients / 2)

# Sept 24 2023

import socket
import threading

servers = []
open_ports = [10001+x for x in range(250)]
matchmaking = 1
direct_connections = []
direct_id = 1111

class Server(object):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.ip, self.port))
		self.clients = []
		self.team = -1
		
	def recieve(self):
		print('RECIEVING\n')
		global servers, matchmaking, direct_id, direct_connections, open_ports
		while True:
			try:
				self.message, self.addr = self.server.recvfrom(64)
				self.data = self.message.decode()

				if self.data == 'dc':
					if not any(self.addr[0] in sl for sl in direct_connections):
						matchmaking -= len(self.clients)
					
					if any(self.addr[0] in sl for sl in direct_connections):
						for i in range(len(direct_connections)):
							if self.addr[0] in direct_connections[i]:
								del direct_connections[i]
					
					
					if len(self.clients) == 2:
						self.server.sendto(self.message, self.other)
					servers.remove(self)
					open_ports.append(self.port)
					print(f'[ {self.port} DISCONNECTED ]')
					print(matchmaking)
					print(direct_connections)
					break

				self.other = []
				if len(self.clients) == 2:
					for client in self.clients:
						self.server.sendto('go'.encode(), client)
					for x in self.clients:
						self.other.append(x)
					self.other.remove(self.addr)
					self.other = self.other[0]
				
				if len(self.clients) <= 2:
					if self.addr not in self.clients:
						print(f'RECIEVING: {self.data} from {self.addr}')
						self.clients.append(self.addr)

				if self.data == 't':
					self.server.sendto(str(self.team).encode(), self.addr)
					print(f'BROADCASTING: {self.team} To {self.addr}')
					self.team = 1
				
				if '.' in self.data:
					if len(self.clients) == 2:
						self.server.sendto(self.message, self.other)
						print(f'BROADCASTING: {self.data} To {self.other}')

				if self.data == 'tu':
					self.server.sendto(self.message, self.other)
					print(f'BROADCASTING: {self.data} To {self.other}')

				if self.data[0] == 'd' and self.data[1] != 'c':
					self.server.sendto(self.message, self.other)
			
			except Exception as e:
				print(e)
				raise(e)

def main():
	global servers, direct_id, direct_connections, matchmaking
	main_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip = '192.168.0.247' # IP OF THE COMPUTER HOSTING THE SERVER
	port = 10000 # A CLEAR PORT TO USE
	main_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	main_server.bind((ip, port))
	index = 0

	while True:
		try:
			message, addr = main_server.recvfrom(64)
			data = message.decode()			
			if data != 'G':
				print(f'DATA: {data} FROM: {addr}')
				#print(f'MATCHMAKING PLAYERS: {matchmaking - 1}\nSERVERS: {servers}')
			
			# --------------------------------------------------------------------------------------------------------- #
			if 'dir' in data: #request for direct connection
				#sending an id to the user
				if len(data) == 3:
					temp = 'dir' + str(direct_id)	
					main_server.sendto(str(temp).encode(), addr)
					direct_connections.append([addr[0], addr[1], direct_id])
					direct_id += 1

					s = len(servers)
					s1 = Server('192.168.0.247', open_ports[0])
					del open_ports[0]

					servers.append(s1)
					thread = threading.Thread(target=servers[s].recieve)
					thread.daemon = True
					thread.start()
					main_server.sendto((str(servers[s].ip) + '|' + str(servers[s].port)).encode(), addr)

				if len(data) > 3:
					#check if id match in direct_connections
					#print(f'DATA: {data[3:]}\nCHECK: {any(int(data[3:]) in sl for sl in direct_connections)}\nDirect Conn: {direct_connections}')
					if any(int(data[3:]) in sl for sl in direct_connections):
						#print('ID IN CONNECTIONS')
						#print(f'ID: {data[3:]}\nConnections: {direct_connections}')
						for i in range(len(direct_connections)):
							if data[3:] in direct_connections[i]:
								index = i
						print(str(servers[s].ip) + '|' + str(servers[s].port))
						main_server.sendto((str(servers[s].ip) + '|' + str(servers[s].port)).encode(), (direct_connections[index][0], direct_connections[index][1]))
					else:
						main_server.sendto('dc'.encode(), addr)
						
			# --------------------------------------------------------------------------------------------------------- #
			
			if 'G' != data and 'dir' not in data:
				if matchmaking % 2 == 0 and len(servers) > 0:
					#give the current server info (string message will be like '111.111.111.111|4435')
					s = len(servers)
					main_server.sendto((str(servers[s - 1].ip) + '|' + str(servers[s - 1].port)).encode(), addr)
					matchmaking += 1
					
				elif matchmaking % 2 == 1 or len(servers) < 1:
					#create a new server to provide info for and creates a thread to open the server on
					s = len(servers)
					s1 = Server('192.168.0.247', open_ports[0])
					servers.append(s1)
					thread = threading.Thread(target=servers[s].recieve)
					thread.daemon = True
					thread.start()
					main_server.sendto((str(servers[s].ip) + '|' + str(servers[s].port)).encode(), addr)
					matchmaking += 1

		except Exception as e:
			print(e)
			print(f'DISCONNECTED: {addr}')

if __name__ == '__main__':
	main()
