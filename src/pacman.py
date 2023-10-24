from board import boards
import pygame
import math

pygame.init()

# Screen
WIDTH = 900 
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
level = boards
color = 'blue'

# Timer
timer = pygame.time.Clock()
fps = 60

# Font
font = pygame.font.Font('freesansbold.ttf', 20)
special_font = pygame.font.Font(None, 100)
PI = math.pi

# Images

player_images = [] # Player Images
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
numbers = [] and True
counter = 0

blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2


for i in range(1, 4): # Countdown Images
    numbers.append(pygame.transform.scale(pygame.image.load(f'assets/count_down/{i}.png'), (30, 30)))
numbers_counter = 0
numbers_displayed = 0

# Player Information
player_x = 450
player_y = 663
direction = 0
turns_allowed = [False, False, False, False] # R, L, U, D
direction_command = 0
player_speed = 3
lives = 3
moving = True


flicker = False
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y)]
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
ghost_speed = 2

startup_counter = 0

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead 
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        num1 = (HEIGHT - 50) // 32    
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num2][self.center_x // num2] < 3 \
                or (level[(self.center_y + num3) // num2][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num2][self.center_x // num2] < 3 \
                or (level[(self.center_y - num3) // num2][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x// num2] < 3 \
                        or (level[(self.center_y + num3) // num1][self.center_x// num2] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x// num2] < 3 \
                        or (level[(self.center_y - num3) // num1][self.center_x// num2] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num1) // num1][self.center_x// num2] < 3 \
                        or (level[(self.center_y + num1) // num1][self.center_x// num2] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num1) // num1][self.center_x// num2] < 3 \
                        or (level[(self.center_y - num1) // num1][self.center_x// num2] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                        or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True

        else: 
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 490:
            self.in_box = True
        else:
            self.in_box = False

            self.turns = [False, False, False, False]
            self.in_box = True

        return self.turns, self.in_box

    def move_clyde(self):
        # R, L U D
        # Clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos += 1
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 0
                    self.x_pos -= self.speed 
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos += self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed


def draw_countdown():
    if numbers:
        screen.blit(numbers[numbers_counter // 60], (440, 915))

def draw_misc():
    # Blitting Information at the bottom of the screen
    score_text = font.render(f"Score: {score}", True, 'white')

    # Blitting score_text on bottom
    screen.blit(score_text, (10, 920))

    # Blitting score_text at the end on the middle
    if score >= 2620:
        bigger_score_text = pygame.font.SysFont(None, 60) 
        bigger_score_text = bigger_score_text.render(f"Score: {score}", True, 'white')
        screen.blit(bigger_score_text, (360, 500))

    # Blitting Powerup
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    # Blitting Pac-Man lives
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

def check_collisions(scor, power, power_count, eaten_ghosts):


   
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH//30
    if 0 < player_x < 870:

        # Adding 10 Points for each normal sized dot eaten
        if level[center_y//num1][center_x // num2] == 1:
            level[center_y//num1][center_x // num2] = 0
            scor += 10
        
        # Adding 50 Points for each big sized dot eaten
        if level[center_y//num1][center_x // num2] == 2:
            level[center_y//num1][center_x // num2] = 0
            scor += 50        

            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]

    return scor, power, power_count, eaten_ghosts

def draw_board():
   num1 = ((HEIGHT - 50) // 32)
   num2 = (WIDTH // 30)
   for i in range(len(level)):
       for j in range(len(level[i])):  

           # Normal sized dot  
           if level[i][j] == 1:
               pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 4)
            
            # Big sized dot
           if level[i][j] == 2 and not flicker:
               pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 10)

            # Vertical Border line
           if level[i][j] == 3:
               pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                (j * num2 + (0.5 * num2), i * num1 + num1), 3)
               
            # Horizontal Border line
           if level[i][j] == 4:
               pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
               
            # Arc: 0, PI/2 
           if level[i][j] == 5:
               pygame.draw.arc(screen, color, [(j*num2 - (num2 * 0.4) - 2), (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3) 
            
            # Arc: PI/2, PI 
           if level[i][j] == 6:
               pygame.draw.arc(screen, color,
                                [(j*num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI/2, PI, 3) 
            
            # Arc: PI, 3*PI/2
           if level[i][j] == 7:
               pygame.draw.arc(screen, color, [(j*num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI/2, 3) 
            
            # Arc: 2, 2*PI/2
           if level[i][j] == 8:
               pygame.draw.arc(screen, color,
                                [(j*num2 - (num2 * 0.4)) -2, (i * num1 - (0.4 * num1)), num2, num1], 3*PI / 2, 2*PI, 3) 
            
            # White Horizontal line
           if level[i][j] == 9:
               pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
               
def draw_player():
    # Directions player can look at 
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32    # Height of each tile
    num2 = (WIDTH // 30)    # Width of each tile
    num3 = 15    # Fudge number

    # check collisions based on center x and center y of player +/- fudge number 
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True
                
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True                
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
        
    else:
        turns[0] = True
        turns[1] = True

    return turns
    
# Player speed and direction
def move_player(play_x, play_y):
    #r, l, u, d
        if direction == 0 and turns_allowed[0]:
            play_x += player_speed
        elif direction == 1 and turns_allowed[1]:
            play_x -= player_speed
        if direction == 2 and turns_allowed[2]:
            play_y -= player_speed
        elif direction == 3 and turns_allowed[3]:
            play_y += player_speed
        return play_x, play_y

# Time + flicking of big dot
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 10:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]

    # Start-up Counter
    if startup_counter < 180:
        startup_counter += 1
        moving = False
    else:
        moving = True
        
    # Countdown
    if numbers_counter < 179:
        numbers_counter += 1
    else:
        numbers = False
         
    # Functions
    screen.fill('black')
    draw_board()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[0], ghost_speed, inky_img, inky_direction, inky_dead, inky_box, 0)
    pinky = Ghost(pinky_x, pinky_y, targets[0], ghost_speed, pinky_img, pinky_direction, pinky_dead, pinky_box, 0)
    clyde = Ghost(clyde_x, clyde_y, targets[0], ghost_speed, clyde_img, clyde_direction, clyde_dead, clyde_box, 0)
    draw_player()
    draw_misc()
    draw_countdown()
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost )


    # Quitting the screen
    for event in pygame.event.get():  
       if event.type == pygame.QUIT:    
            run = False
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:
               run = False 

    # Defining Controls
       if event.type == pygame.KEYDOWN: 
           if event.key == pygame.K_RIGHT:
               direction_command = 0
           if event.key == pygame.K_LEFT:
               direction_command = 1
           if event.key == pygame.K_UP:
               direction_command = 2
           if event.key == pygame.K_DOWN:
               direction_command = 3


       if event.type == pygame.KEYUP:
           if event.key == pygame.K_RIGHT and direction_command == 0:
               direction_command = direction
           if event.key == pygame.K_LEFT and direction_command == 1:
               direction_command = direction
           if event.key == pygame.K_UP and direction_command == 2:
               direction_command = direction
           if event.key == pygame.K_DOWN and direction_command == 3:
               direction_command = direction

   
    # Setting the direction
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
    
    # Skipping throgh the map
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897


    pygame.display.flip()
pygame.quit()
