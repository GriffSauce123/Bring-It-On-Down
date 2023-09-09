# BRING IT ON DOWN - Griffin Adelmann
# August 15 2023
# Alpha 0.1 - Offline

import random, sys, pygame, time


# -------------------- THINGS THAT NEED TO BE DONE -------------------- #
# win detection / end of turn detection
# Make it look better make logos, banners, sprites, 
# BRING IT ON DOWN
# save states, stats and such
# --------------------------------------------------------------------- #

pygame.init()
pygame.font.init()

#ASPECT RATIO MUST BE 16 x 9 FOR CORRECT SCALING OF OBJECTS
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w

#loading images and captions and things
icon = pygame.image.load('icon-0.2.png')
icon_4k = pygame.image.load('icon-0.3.png')
pop = pygame.mixer.Sound('pop.wav')

#banner = pygame.image.load('banner.png') # The title for the main menu and such

pygame.display.set_icon(icon)
pygame.display.set_caption('Bring It On Down')


screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
font = pygame.font.SysFont('', int(height / 24))
dice_font = pygame.font.SysFont('', int(height / 9.6))
clock = pygame.time.Clock()
turn = 1
segments = 10 # number of segments to be rendered (used for centering things)
dice = [0,0]
running = False
highlight = False
dice = [0,0]

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Button(object):
  def __init__(self, color, pos, size, action, text, font):
    self.color = color
    self.pos = pos
    self.size = size
    self.action = action
    self.text = text
    self.font = font

    #rect for click detection
    self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def function(self):
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      pop.play()
      self.action()

  #drawing screen objects
  def draw(self):
    pygame.draw.rect(screen, (255,255,255), self.rect, 0, border_radius = 1000)
    pygame.draw.rect(screen, self.color, self.rect, 5, border_radius = 1000)
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      pygame.draw.rect(screen, dice_color, self.rect, 5, border_radius = 1000)
    
    screen.blit((self.font.render(str(self.text), False, self.color)), (self.pos[0] + int(height / 36), self.pos[1] + int(height / 45)))

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Segment(object):
  def __init__(self, num, pos, team):
    self.num = num
    self.pos = pos
    self.team = team
    self.rad = int(width / 32)
    self.stat = 0
    self.adjust = -int(width / 32) * self.team
    
    #setting colors based on the team provided
    if self.team == -1:
      self.color = (255, 50, 50)
    elif self.team == 1:
      self.color = (50, 50, 255)

    #pygame Rect object for player interactions
    self.rect = pygame.Rect(self.pos[0] - self.rad, self.pos[1] - self.rad - self.adjust - (width / 32), self.rad * 2, self.rad * 4)

    #pygame surface to render the num on
    self.text_s = font.render(str(self.num), False, self.color)

  def draw(self):
    #highlighting playable spaces
    if highlight:
     if self.num in dice or self.num == dice[0] + dice[1]:
        pygame.draw.rect(screen, 'lime', [self.pos[0] - self.rad - int(width / 160), self.pos[1] - self.rad - self.adjust - int(height / 15), self.rad * 2 + int(width / 80), self.rad * 4 + int(width / 80)], int(width / 256), border_radius = 1000)
        pygame.draw.circle(screen, 'lime', [self.pos[0], self.pos[1] + int(width / 8) * self.team], self.rad + int(width / 160), int(width / 256))
    
    #outline
    pygame.draw.rect(screen, self.color, self.rect, int(width / 160), border_radius = 1000)
    pygame.draw.rect(screen, (0,0,0), [self.pos[0] - self.rad - int(width / 320), self.pos[1] - self.rad - self.adjust - int(width / 29), self.rad * 2 + int(width / 160), self.rad * 4 + int(width / 160)], int(width / 320), border_radius = 1000)

    #player piece                                             80 = movement amount
    pygame.draw.circle(screen, self.color, [self.pos[0], self.pos[1] + int(width / 16) * self.stat * self.team], self.rad, int(height / 40))
    
    #safe space
    pygame.draw.circle(screen, self.color, [self.pos[0], self.pos[1] + int(width / 8) * self.team], self.rad, int(width / 160))
    pygame.draw.circle(screen, (0, 0, 0), [self.pos[0], self.pos[1] + int(width / 8) * self.team], self.rad + int(width / 320), int(width / 256))

    #Render the num assigned with the segment
    screen.blit(self.text_s, (self.pos[0] - int(width / 160), self.pos[1] + int(width / 8) * self.team))

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
    if self.stat == 0:
      
      #only manipulate pieces on correct team
      if turn % 2 != 0 and self.team == -1 or turn % 2 == 0 and self.team == 1:
        self.stat = 1
        dice_check()
        pop.play()

    elif self.stat == 2:
      if turn % 2 != 0 and self.team == -1 or turn % 2 == 0 and self.team == 1:
        self.stat = 1
        dice_check()
        pop.play()

    elif self.stat == 1:
      if turn % 2 == 0 and self.team == -1 or turn % 2 != 0 and self.team == 1:
        self.stat = 0
        dice_check()
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

def roll_dice():
    global dice
    dice = [random.randint(1, 6), random.randint(1, 6)]

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
  
# ------------------------------------------------------------------------------------------------------------------------------------------ #

def gameloop():
  global dice, turn, running, board1, board2, dice_color
  
  #creating the player boards
  board1 = [Segment(x + 1, (x * int(width / 12.8) + int(height / 8) + ((12 - segments) * int(width / 25.3)), int(height * (8 / 9))), -1) for x in range(segments)]
  board2 = [Segment(x + 1, (x * int(width / 12.8) + int(height / 8) + ((12 - segments) * int(width / 25.3)), int(height / 9)), 1) for x in range(segments)]

  #creating the button class instances
  dice_button = Button((0, 0, 0), (width * 0.75 - int(width / 19.7), height / 2 - int(height / 28.8)), (int(width / 10), int(height / 14.4)), roll_dice, 'Roll Dice', font)
  turn_button = Button((0, 0, 0), (width / 4 - int(width / 19.7), height / 2 - int(height / 28.8)), (int(width / 10), int(height / 14.4)), change_turn, 'End Turn', font)

  running = True
  
# ------------------------------------------------------------------------------------------------------------------------------------------ #

  while running:
    
    #checking for wins
    winning = 0
    for s in board1:
      if s.stat != 0:
        winning += 1
    if winning == segments:
      win('red team'.upper())

    winning = 0
    for s in board2:
      if s.stat != 0:
        winning += 1
      if winning == segments:
        win('blue team'.upper())


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()

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

        #Checking for a win condition every click
        # : (
        # win_menu(team)
                
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
        
    #Draws lines to center things
    #pygame.draw.line(screen, (0, 0, 0), [width/2,0], [width/2,height], 1)
    #pygame.draw.line(screen, (0, 0, 0), [0,height/2], [width,height/2], 1)
    
    # refreshes the display
    pygame.display.flip()
    
    clock.tick(10000)  # limits FPS to 10000
  
def light():
  global highlight
  if highlight:
    highlight = False
  else:
    highlight = True

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def run_menu():
  global running, highlight, quit_button, dice_color
  running = False
  menu = True
  
  #initial states of variables
  dice_color = (255, 100, 100)


  quit_button = Button((0, 0, 0), (width - int(5 * width / 60), int(width / 60)), (int(width / 15), int(height / 14.4)), quit, 'Quit', font)
  game = Button((0,0,0), (width / 2 - int(width / 17.066), height * 0.65 ), (int(width / 8.53), int(height / 9)), gameloop, 'Play', dice_font)
  highlights = Button((0, 0, 0), (width / 2 - int(width / 6.4), height / 2), (int(width / 3.2), int(height / 9)), light, 'Highlights', dice_font)
  
  while menu and not running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
        
      elif event.type == pygame.MOUSEBUTTONUP:
        game.function()
        highlights.function()
        quit_button.function()

    # background
    screen.fill('white')
    screen.blit(icon, (width / 2 - icon.get_width() / 2, height * 0.25 - icon.get_height() / 2))
    #screen.blit(icon_4k, (width / 2 - icon_4k.get_width() / 2, height * 0.25 - icon_4k.get_height() / 2))
    #screen.blit(banner, (width / 2 - banner.get_width() / 2, height * 0.2 - banner.get_height() / 2))

    #Draws lines to center things
    #pygame.draw.line(screen, (0, 0, 0), [width / 2, 0], [width / 2,height], 1)
    #pygame.draw.line(screen, (0, 0, 0), [0, height / 2], [width,height / 2], 1)

    #some buttons here
    game.draw()
    quit_button.draw()
    highlights.draw()
    if highlight:
      pygame.draw.circle(screen, 'lime', (width / 2 + int(height / 4.8), height * 0.5 + int(width / 32)), int(height / 24), 0)
    pygame.draw.circle(screen, 'black', (width / 2 + int(height / 4.8), height * 0.5 + int(width / 32)), int(height / 24), int(width / 320))


    pygame.display.flip()
    clock.tick(10000)

  pygame.quit()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def pause():
  global running
  running = False
  paused = True
  while paused:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          paused = False
          running = True

      if event.type == pygame.MOUSEBUTTONUP:
        quit_button.function()

    #background
    #screen.fill('white')
    pygame.draw.rect(screen, dice_color, (0,0, width, height), 0)

    screen.blit((dice_font.render(f'Press ESCAPE To Return To Game', False, (0, 0, 0))), [int(width / 6.4), height / 2 - int(height / 10.3)])
    screen.blit((dice_font.render(f'Turn: {str(turn)}', False, (0, 0, 0))),[width / 2 - int(width / 15.238), height / 2 + int(height / 30)])

    quit_button.draw()

    pygame.display.flip()
    clock.tick(10000)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def win(team):
  global running, turn
  running = False
  
  particles = []

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      if event.type == pygame.KEYDOWN:
        quit()
    screen.fill('white')

    # confetti would happen here btw

    particles.append(Particle(random.randint(2, 10), dice_color, random.randint(0, width), -10, random.randint(-2, 2), random.randint(1,2), particles))
    for particle in particles:
      particle.update()

    screen.blit((dice_font.render(f'{team.upper()} WINS!', False, (0, 0, 0))),[width / 3, height / 2])

    clock.tick(10000)
    pygame.display.flip()

# ------------------------------------------------------------------------------------------------------------------------------------------ #

if __name__ == '__main__':
  run_menu()
