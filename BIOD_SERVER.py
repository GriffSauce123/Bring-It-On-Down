# So Far So Good

# make server not use a seperate thread for every 2 users :(
# make waiting for connection screen work

import socket
import threading

servers = []
total_clients = []
counter = 1

class Server(object):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port + counter
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.bind((self.ip, self.port))
		self.clients = []
		self.team = -1
		
	def recieve(self):
		print('RECIEVING\n')
		global servers, total_clients, counter
		while True:
			try:
				self.message, self.addr = self.server.recvfrom(1024)
				self.data = self.message.decode()

				self.other = []
				if len(self.clients) == 2:
					for x in self.clients:
						self.other.append(x)
					self.other.remove(self.addr)
					self.other = self.other[0]
				
				if self.data == 'disconnect':
					total_clients.remove(self.addr)
					self.clients.remove(self.addr)
					print(f'[ {self.addr} DISCONNECTED ]')
					if len(self.clients) == 2:
						self.server.sendto(self.data.encode(), self.other)
					elif len(self.clients) == 1:
						counter -= 1
					servers.remove(self)
					break				

				if len(self.clients) <= 2:
					if self.addr not in self.clients:
						print(f'RECIEVING: {self.data} from {self.addr}')
						self.clients.append(self.addr)

				if self.data == 'team':
					self.server.sendto(str(self.team).encode(), self.addr)
					print(f'BROADCASTING: {self.team} To {self.addr}')
					self.team = 1
				
				if '.' in self.data:
					if len(self.clients) == 2:
						self.server.sendto(self.message, self.other)
						print(f'BROADCASTING: {self.data} To {self.other}')

				if self.data == 'turn':
					if len(self.clients) == 2:
						self.server.sendto(self.message, self.other)
						print(f'BROADCASTING: {self.data} To {self.other}')
					else:
						print('ONLY ONE CLIENT CONNECTED')
			
			except Exception as e:
				print(e)

def main():
	global servers, total_clients, counter
	main_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip = '192.168.0.247' # IP OF THE COMPUTER HOSTING THE SERVER
	port = 10003 # A CLEAR PORT TO USE
	main_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	main_server.bind((ip, port))

	while True:
		try:
			message, addr = main_server.recvfrom(1024)
			data = message.decode()			
			total_clients.append(addr)
			print(f'Counter: {counter}\nServers: {len(servers)}')

			if counter % 2 == 0 and len(servers) > 0:
				#give the current server info (string message will be like '111.111.111.111|4435')
				s = len(servers)
				main_server.sendto((str(servers[s - 1].ip) + '|' + str(servers[s - 1].port)).encode(), addr)
				counter += 1
				pass

			elif counter % 2 == 1 or len(servers) < 1:
				#create a new server to provide info for and creates a thread to open the server on
				s = len(servers)
				s1 = Server('192.168.0.247', port + 1)
				servers.append(s1)
				thread = threading.Thread(target=servers[s].recieve)
				thread.daemon = True
				thread.start()
				main_server.sendto((str(servers[s].ip) + '|' + str(servers[s].port)).encode(), addr)
				counter += 1

		except Exception as e:
			print(e)
			total_clients.remove(addr)
			print(f'DISCONNECTED: {addr}')


	
if __name__ == '__main__':
	main()
