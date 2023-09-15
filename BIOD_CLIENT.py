	# BRING IT ON DOWN - Griffin Adelmann
# August 15 2023
# Alpha 0.5 - Online - Functioning, multi client filtering, disconnection detection

import random, sys, pygame, time, socket, threading, os

# -------------------- THINGS TO BE DEALT WITH -------------------- #
#
# option to play multiplayer or singleplayer
# make server not use a seperate thread for every 2 users :(
# waiting screen for connection looks like dick
# dissconection through crash / forcefull end detection
# Make it look better make logos, banners, sprites, 
# save states, stats and such
#
# --------------------------------------------------------------------- #

class Button(object):
	def __init__(self, color, pos, action, text, font):
		self.color = color
		self.pos = pos
		self.action = action
		self.text = text.upper()
		self.font = font
		
		#so the text renders properly
		self.text_width, self.text_height = self.font.size(self.text)
		self.size = (self.text_width + width / 19.2, self.text_height + width / 48)

		#to center things properly
		self.render_pos = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)

		#rect for click detection
		self.rect = pygame.Rect(self.render_pos[0], self.render_pos[1], self.size[0], self.size[1])

	def function(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			#pop.play()
			self.action()

	#drawing screen objects
	def draw(self):
		pygame.draw.rect(screen, (255,255,255), self.rect, 0, border_radius = 1000)
		pygame.draw.rect(screen, self.color, self.rect, 5, border_radius = 1000)
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			pygame.draw.rect(screen, dice_color, self.rect, 5, border_radius = 1000)
		
		screen.blit((self.font.render(str(self.text), False, self.color)), (self.render_pos[0] + width / 38.4, self.render_pos[1] + width / 80))

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Segment(object):
	def __init__(self, num, pos, team, board):
		self.num = num
		self.pos = pos
		self.team = team
		self.rad = int(width / 32)
		self.stat = 0
		self.board = board
		self.color = (0, 0, 0)
		#setting colors based on the team provided
		if self.team == -1:
			self.color = (255, 50, 50)
		elif self.team == 1:
			self.color = (50, 50, 255)

		#pygame Rect object for player interactions
		self.rect = pygame.Rect(self.pos[0] - self.rad, self.pos[1] - self.rad - (width / 32) - self.rad * self.board, self.rad * 2, self.rad * 4)

		#pygame surface to render the num on
		self.text_s = font.render(str(self.num), False, self.color)
		self.text_width, self.text_height = font.size(str(self.num))

	def change_value(self, value):
		self.stat = value

	def draw(self):

		#highlighting playable spaces
		if highlight:
		 if self.num in dice or self.num == dice[0] + dice[1]:
				pygame.draw.rect(screen, 'lime', [self.pos[0] - self.rad - int(width / 160), self.pos[1] - self.rad - int(height / 15) - self.rad * self.board, self.rad * 2 + int(width / 80), self.rad * 4 + int(width / 80)], int(width / 256), border_radius = 1000)
				pygame.draw.circle(screen, 'lime', [self.pos[0], self.pos[1] - int(width / 8) * self.board], self.rad + int(width / 160), int(width / 256))
		
		#outline
		pygame.draw.rect(screen, self.color, self.rect, int(width / 160), border_radius = 1000)
		pygame.draw.rect(screen, (0,0,0), [self.pos[0] - self.rad - int(width / 320), self.pos[1] - self.rad - int(width / 29) - self.rad * self.board, self.rad * 2 + int(width / 160), self.rad * 4 + int(width / 160)], int(width / 320), border_radius = 1000)

		#player piece                                 x                                    y
		pygame.draw.circle(screen, self.color, [self.pos[0], self.pos[1] + (int(width / 16) * self.stat * self.board * -1)], self.rad, int(height / 40))
		
		#safe space
		pygame.draw.circle(screen, self.color, [self.pos[0], self.pos[1] - int(width / 8) * self.board], self.rad, int(width / 160))
		pygame.draw.circle(screen, (0, 0, 0), [self.pos[0], self.pos[1] - int(width / 8) * self.board], self.rad + int(width / 320), int(width / 256))

		#Render the num assigned with the segment
		screen.blit(self.text_s, (self.pos[0] - self.text_width / 2, self.pos[1] - int(width / 8) * self.board - self.text_height / 3))

	def update(self):
		def dice_check():
			global dice
			#checking to see if move is legal and reseting dice when necessary
			for i in range(2):
				if int(dice[i]) == int(self.num):
					dice[i] = 0
					break
				if int(dice[0]+dice[1]) == int(self.num):
					dice = [0,0]

		#updating stat of pieces
		if self.num in dice or self.num == (dice[0] + dice[1]):
			if self.stat == 0:
				
				#only manipulate pieces on correct team
				if turn % 2 != 0 and self.team == -1 or turn % 2 == 0 and self.team == 1:
					self.stat = 1
					dice_check()
					send_server(str(self.board) + '.' + str(self.num) + '.' + str(self.stat))
					pop.play()

			elif self.stat == 2:
				if turn % 2 != 0 and self.team == -1 or turn % 2 == 0 and self.team == 1:
					self.stat = 1
					dice_check()
					send_server(str(self.board) + '.' + str(self.num) + '.' + str(self.stat))
					pop.play()

			elif self.stat == 1:
				if turn % 2 == 0 and self.team == -1 or turn % 2 != 0 and self.team == 1:
					self.stat = 0
					dice_check()
					send_server(str(self.board) + '.' + str(self.num) + '.' + str(self.stat))
					pop.play()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Particle(object):
	def __init__(self, rad, color, x, y, x_vel, y_vel, particles):
		self.rad = rad
		self.color = color
		self.x = x
		self.y = y
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.particles = particles

	def update(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad, 0)
		self.y += self.y_vel
		self.x += self.x_vel

		if self.y > height + self.rad * 2:
			self.particles.remove(self)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def recieve():
	global m, team, turn, not_team, dice_color, board2_o, board1_o, dice, host, port, go, running_online
	get_team = True
	print('[ RECIEVING ]')
	while recieving:
		try:
			message = client.recvfrom(1024)
			m = message[0].decode()
			print(f'\nMESSAGE: {m}\n')

			if '|' in m:
				host = m.split('|')[0]
				port = int(m.split('|')[1])

				#requesting the team variable:
				send_server('team')

			if m == '-1' or m == '1':
				if get_team:
					team = int(m)
					if m == '1':
						not_team = -1
					elif m == '-1':
						not_team = 1
					print(f'GOT TEAM: {team}')
					get_team = False
		 
			if m == 'go':
				print('GO RECIEVED')
				go = True

			if m == 'turn':
				print(f'RECIEVED TURN')  
				
				pop.play()

				turn += 1
				dice = [0,0]

				if turn % 2 == 1:
					dice_color = (255, 100, 100)
				elif turn % 2 != 1:
					dice_color = (100, 100, 255)

			#if there is a board status update
			if '.' in m and '|' not in m:
				print(f'BOARD UPDATE: {m}')
				temp = m.split('.')
				if temp[0] == '-1':
					board1_o[int(temp[1]) - 1].change_value(int(temp[2]))
				elif temp[0] == '1':
					board2_o[int(temp[1]) - 1].change_value(int(temp[2]))
				pop.play()

			if 'dice' in m:
				print(f'DICE: {m}')
				dice = m[-3:].split(' ')
				print(f'DICE1: {dice}')
				dice[0], dice[1] = int(dice[0]), int(dice[1])
				pop.play()

			if 'disconnect' in m:
				print('CLIENT 2 DISCONNECTED, SERVER SHUTTING DOWN')
				running_online = False
				go = True
				run_menu()


			m = ''
		except Exception as e:
			print(e)
	print('[ NO LONGER RECIEVING ]')

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def send_server(data):
	try:
		client.sendto(str(data).encode(), (server_host, port))
	except Exception as e:
		print(e)
# ------------------------------------------------------------------------------------------------------------------------------------------ #

def roll_dice():
	global dice
	if team == -1 and turn % 2 == 1 or team == 1 and turn % 2 == 0:
		dice = [random.randint(1, 6), random.randint(1, 6)]
		pop.play()
		send_server('dice' + str(dice[0]) + ' ' + str(dice[1]))

def roll_dice_offline():
	global dice
	dice = [random.randint(1, 6), random.randint(1, 6)]
	pop.play()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def change_turn_online():
	global turn, dice, board1_o, board2_o, dice_color
	
	if turn % 2 == 0 and team == 1:
		for s in board2_o:
			if s.stat == 1:
				s.stat = 2
				send_server(str(s.board) + '.' + str(s.num) + '.' + str(s.stat))
		send_server('turn')
		pop.play()

		turn += 1
		dice = [0,0]

		if turn % 2 == 1:
			dice_color = (255, 100, 100)
		elif turn % 2 != 1:
			dice_color = (100, 100, 255)

	elif turn % 2 == 1 and team == -1:
		for s in board2_o:
			if s.stat == 1:
				s.stat = 2
				send_server(str(s.board) + '.' + str(s.num) + '.' + str(s.stat))
		send_server('turn')
		pop.play()

		turn += 1
		dice = [0,0]

		if turn % 2 == 1:
			dice_color = (255, 100, 100)
		elif turn % 2 != 1:
			dice_color = (100, 100, 255)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def change_turn():
		global turn, dice
		if turn % 2 == 0:
			for s in board1:
				if s.stat == 1:
					s.stat = 2
		elif turn % 2 == 1:
			for s in board2:
				if s.stat == 1:
					s.stat = 2
		#resets the dice after each turn
		dice = [0,0]
		turn += 1
		pop.play()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def offline():
	global dice, turn, running, board1, board2, dice_color
	pop.play()

	#creating the player boards
	board1 = [Segment(x + 1, (x * int(width / 12.8) + int(height / 8) + ((12 - segments) * int(width / 25.3)), int(height * (8 / 9))), -1, 1) for x in range(segments)]
	board2 = [Segment(x + 1, (x * int(width / 12.8) + int(height / 8) + ((12 - segments) * int(width / 25.3)), int(height / 9)), 1, -1) for x in range(segments)]

	#creating the button class instances
	dice_button = Button((0, 0, 0), (width * 0.8, height / 2), roll_dice_offline, 'Roll Dice', font) # turn into width
	turn_button = Button((0, 0, 0), (width / 5, height / 2), change_turn, 'End Turn', font)

	running = True
	while running:
		
		#checking for wins
		winning = 0
		for s in board1:
			if s.stat != 0:
				winning += 1
		if winning == segments:
			win()

		winning = 0
		for s in board2:
			if s.stat != 0:
				winning += 1
			if winning == segments:
				win()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				button_quit()

			#exit to the menu
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause()
					
			# checking for clicks on buttons
			if event.type == pygame.MOUSEBUTTONUP:
				#so you can only roll dice when they have been used up
				if dice == [0,0]:
					dice_button.function()
				turn_button.function()

			#Player 1 turn (red)
			if turn % 2 != 0:
				dice_color = (255, 100, 100)
				
				#checks for clicks and processes actions appropriately
				if event.type == pygame.MOUSEBUTTONUP:
					for s in board1:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							if s.stat == 0 and s.num in dice or s.num == dice[0]+dice[1] or s.stat == 2 and s.num in dice or s.num == dice[0]+dice[1]:
								s.update()
					for s in board2:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							if s.stat == 1 and s.num in dice or s.num == dice[0]+dice[1]:
								s.update()

			#Player 2 turn (blue)
			elif turn % 2 == 0:
				dice_color = (100, 100, 255)
				
				#checks for clicks and processes actions appropriately
				if event.type == pygame.MOUSEBUTTONUP:
					for s in board2:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							if s.stat == 0 and s.num in dice or s.num == dice[0]+dice[1] or s.stat == 2 and s.num in dice or s.num == dice[0]+dice[1]:
								s.update()
					for s in board1:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							if s.stat == 1 and s.num in dice or s.num == dice[0]+dice[1]:
								s.update()

		# background
		screen.fill('white')
		#player boards
		for seg in board1:
			seg.draw()
		for s in board2:
			s.draw()

		#drawing the dice area
		pygame.draw.rect(screen, dice_color, [width / 2 - int(height / 3.2), height / 2 - int(height / 12.8), int(height / 1.6), int(height / 6.4)], 0, border_radius = 1000)
		pygame.draw.rect(screen, (0, 0, 0), [width / 2 - int(height / 3.2), height / 2 - int(height / 12.8), int(height / 1.6), int(height / 6.4)], int(width / 256), border_radius = 1000)
		
		#drawing the nums on the dice
		screen.blit((dice_font.render(str(dice[0]) + '     ' + str(dice[1]), False, (0,0,0))), [width / 2 - int(height / 11.4), height / 2 - int(height / 32)])
		
		#buttons
		dice_button.draw()
		turn_button.draw()
				
		# refreshes the display
		pygame.display.flip()
		
		clock.tick(240)  # limits FPS to 240

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def online():
	global dice, turn, running_online, board1_o, board2_o, dice_color, recieving, client, server_host, port, host, team, m, go
	
	#initializing the network to send and recieve data
	host = str((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
	#host = '192.168.0.107' # THIS IS THE CLIENT'S IP ADDRESS
	server_host = '73.159.244.185' # THIS IS THE SERVER IP ADDRESS
	port = 10003

	recieving = True

	team = 0
	go = False

	m = ''

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client.bind((host, port))

	#initializing and starting the networking thread
	t1 = threading.Thread(target=recieve)
	t1.daemon = True
	t1.start()

	send_server('Request To Connect')

	pop.play()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

	#making sure the game only starts once team is given from the server
	angle = 0
	while team == 0:
		continue

	#WAITING SCREEN WHILE SERVER LOOKS FOR PLAYER 2
	print(f'GO STATUS: {go}')
	while not go:
		
		if go == True:
			break
		#to update the server
		send_server('')

		for event in pygame.event.get():
			#check for an exit request
			if event.type == pygame.QUIT:
				button_quit()

			#exit to the menu
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause()
			

		screen.fill((255, 255, 255))
		t_width, t_height = dice_font.size('WAITING FOR PLAYER 2')
		screen.blit((dice_font.render(f'WAITING FOR PLAYER 2', False, (0, 0, 0))), [width / 2 - t_width / 2, height / 3 - t_height / 2]) # turn into width
		img_copy = pygame.transform.rotate(loading_icon, angle)
		screen.blit(img_copy, (width / 2 - img_copy.get_width() / 2, height / 2 - img_copy.get_height() / 2))
		angle += 3

		pygame.display.flip()
		clock.tick(240)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

	#creating the player boards
	board1_o = [Segment(x + 1, (x * int(width / 12.8) + int(height / 8) + ((12 - segments) * int(width / 25.3)), int(height * (8 / 9))), team, 1) for x in range(segments)] # turn into width
	board2_o = [Segment(x + 1, (x * int(width / 12.8) + int(height / 8) + ((12 - segments) * int(width / 25.3)), int(height / 9)), not_team, -1) for x in range(segments)]

	#creating the button class instances
	dice_button = Button((0, 0, 0), (width * 0.8, height / 2), roll_dice, 'Roll Dice', font) # turn into width
	turn_over = Button((0, 0, 0), (width / 5, height / 2), change_turn_online, 'End Turn', font)

	running_online = True
	
# ------------------------------------------------------------------------------------------------------------------------------------------ #

	while running_online:
		
		#checking for wins
		winning = 0
		for s in board1_o:
			if s.stat != 0:
				winning += 1
		if winning == segments:
			win()

		winning = 0
		for s in board2_o:
			if s.stat != 0:
				winning += 1
			if winning == segments:
				win()

		#Checking for any pygame event
		for event in pygame.event.get():
			
			#check for an exit request
			if event.type == pygame.QUIT:
				button_quit()

			#exit to the menu
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause()
			
			#Player 1 turn (red)
			if turn % 2 != 0 and team == -1:
				
				#checks for clicks and processes actions appropriately
				if event.type == pygame.MOUSEBUTTONUP:
					for s in board1_o:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							s.update()
					for s in board2_o:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							s.update()

			#Player 2 turn (blue)
			elif turn % 2 == 0 and team == 1:
								
				#checks for clicks and processes actions appropriately
				if event.type == pygame.MOUSEBUTTONUP:
					for s in board2_o:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							s.update()
					for s in board1_o:
						if s.rect.collidepoint(pygame.mouse.get_pos()):
							s.update()
				

			# checking for clicks on buttons
			if event.type == pygame.MOUSEBUTTONUP:
				turn_over.function()

				#so you can only roll dice when they have been used up
				if dice == [0,0]:
					dice_button.function()

			
		# background
		screen.fill('white')
		#player boards
		for seg in board1_o:
			seg.draw()
		for s in board2_o:
			s.draw()

		#drawing the dice area
		pygame.draw.rect(screen, dice_color, [width / 2 - int(height / 3.2), height / 2 - int(height / 12.8), int(height / 1.6), int(height / 6.4)], 0, border_radius = 1000) # turn into width
		pygame.draw.rect(screen, (0, 0, 0), [width / 2 - int(height / 3.2), height / 2 - int(height / 12.8), int(height / 1.6), int(height / 6.4)], int(width / 256), border_radius = 1000)
		
		#drawing the nums on the dice
		screen.blit((dice_font.render(str(dice[0]) + '     ' + str(dice[1]), False, (0,0,0))), [width / 2 - int(height / 11.4), height / 2 - int(height / 32)])
		
		#buttons
		dice_button.draw()
		turn_over.draw()
				
		#Draws lines to center things
		#pygame.draw.line(screen, (0, 0, 0), [width/2,0], [width/2,height], 1)
		#pygame.draw.line(screen, (0, 0, 0), [0,height/2], [width,height/2], 1)
		
		# refreshes the display
		pygame.display.flip()
		
		clock.tick(240) # limits FPS to 240
	
# ------------------------------------------------------------------------------------------------------------------------------------------ #

def light():
	global highlight
	pop.play()
	if highlight:
		highlight = False
	else:
		highlight = True

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def button_quit():
	pop.play()
	try:
		send_server('disconnect')
		print('DISCONNECTED')
	except Exception as e:
		pass
	time.sleep(0.1)
	quit()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def run_menu():
	global running_online, highlight, quit_button, dice_color, recieving, client, menu_button
	pop.play()
	running_online = False
	running = False
	menu = True
	recieving = False
	
	send_server('disconnect')
	try:
		client.close()
	except Exception as e:
		print(e)

	#initial states of variables
	dice_color = (255, 100, 100)

	quit_button = Button((0, 0, 0), (width - int(width / 16), int(width / 30)), button_quit, 'Quit', font)
	menu_button = Button((0, 0, 0), (width - int(width / 6), int(width / 30)), run_menu, 'Menu', font) 
	game = Button((0,0,0), (width / 2, height * 0.7),  online, 'Online Game', dice_font)
	game_offline = Button((0,0,0), (width / 2, height * 0.85 ), offline, 'Local Game', dice_font)
	highlights = Button((0, 0, 0), (width / 2, height * 0.55), light, 'Highlights     ', dice_font) # turn into height
	
	while menu and not running_online:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				button_quit()
				
			elif event.type == pygame.MOUSEBUTTONUP:
				game.function()
				game_offline.function()
				highlights.function()
				quit_button.function()

		# background
		screen.fill('white')
		screen.blit(icon, (width / 2 - icon.get_width() / 2, height * 0.25 - icon.get_height() / 2))

		#some buttons here
		game.draw()
		game_offline.draw()
		quit_button.draw()
		highlights.draw()
		if highlight:
			pygame.draw.circle(screen, 'lime', (width / 2 + int(height / 4), height / 2 + int(height / 20)), int(height / 24), 0) # turn into width
		pygame.draw.circle(screen, 'black', (width / 2 + int(height / 4), height / 2 + int(height / 20)), int(height / 24), int(width / 320))


		pygame.display.flip()
		clock.tick(240)

	button_quit()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def pause():
	global running_online, recieving, running
	if running_online:
		running_online = False
	if running:
		running = False
	paused = True
	pop.play()
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				button_quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					paused = False
					running_online = True
					running = True

			if event.type == pygame.MOUSEBUTTONUP:
				quit_button.function()
				menu_button.function()

		pygame.draw.rect(screen, dice_color, (0,0, width, height), 0)

		screen.blit((dice_font.render(f'Press ESCAPE To Return To Game', False, (0, 0, 0))), [int(width / 6.4), height / 2 - int(height / 10.3)])
		screen.blit((dice_font.render(f'Turn: {str(turn)}', False, (0, 0, 0))),[width / 2 - int(width / 15.238), height / 2 + int(height / 30)])

		quit_button.draw()
		menu_button.draw()

		pygame.display.flip()
		clock.tick(240)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def win():
	global running_online, turn
	running_online = False
	
	particles = []

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				button_quit()
			
			if event.type == pygame.KEYDOWN:
				button_quit()
		
		screen.fill('white')

		# confetti would happen here btw

		particles.append(Particle(random.randint(2, 10), dice_color, random.randint(0, width), -10, random.randint(-2, 2), random.randint(1,2), particles))
		for particle in particles:
			particle.update()

		if dice_color == (255, 100, 100):
			screen.blit((dice_font.render('RED TEAM WINS!', False, (0, 0, 0))),[width / 3, height / 2])
		elif dice_color == (100, 100, 255):
			screen.blit((dice_font.render('BLUE TEAM WINS!', False, (0, 0, 0))),[width / 3, height / 2])

		clock.tick(240)
		pygame.display.flip()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

if __name__ == '__main__':
	
	pygame.init()
	pygame.font.init()

	#ASPECT RATIO MUST BE 16 x 9 FOR CORRECT SCALING OF OBJECTS
	height = 1080 #pygame.display.Info().current_h
	width = 1920 #pygame.display.Info().current_w

	#loading images and captions and things
	loading_icon = pygame.image.load('loading.png')
	icon = pygame.image.load('icon-0.2.png')
	pop = pygame.mixer.Sound('pop.wav')

	pygame.display.set_icon(icon)
	pygame.display.set_caption('Bring It On Down')

	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
	font = pygame.font.SysFont('', int(height / 24))
	dice_font = pygame.font.SysFont('', int(height / 9.6))
	clock = pygame.time.Clock()
	turn = 1
	team = 0
	not_team = 0
	segments = 10 # number of segments to be rendered (used for centering things)
	dice = [0,0]
	running_online = False
	running = False
	highlight = False
	dice = [0,0]
 
# ------------------------------------------------------------------------------------------------------------------------------------------ #

	run_menu()
