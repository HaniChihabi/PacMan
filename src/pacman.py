from board import boards
import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
PI = math.pi
 
def draw_board():
   num1 = ((HEIGHT - 50) // 32)
   num2 = (WIDTH // 30)
   for i in range(len(level)):
       for j in range(len(level[i])):      #Für jede Zahl bei diesem board mäßiig
           if level[i][j] == 1:
               pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 4)
           if level[i][j] == 2:
               pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 10)
           if level[i][j] == 3:
               pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                (j * num2 + (0.5 * num2), i * num1 + num1), 3)
           if level[i][j] == 4:
               pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                (j * num2 + num2, i * num1 + + (0.5 * num1)), 3)
               
           if level[i][j] == 5:
               pygame.draw.arc(screen, color, [(j*num2 - (num2 * 0.4) - 2), (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3) 
            
           if level[i][j] == 6:
               pygame.draw.arc(screen, color,
                                [(j*num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI/2, PI, 3) 
           
           if level[i][j] == 7:
               pygame.draw.arc(screen, color, [(j*num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI/2, 3) 
            
           if level[i][j] == 8:
               pygame.draw.arc(screen, color,
                                [(j*num2 - (num2 * 0.4)) -2, (i * num1 - (0.4 * num1)), num2, num1], 3*PI / 2, 2*PI, 3) 
           
           if level[i][j] == 9:
               pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                (j * num2 + num2, i * num1 + + (0.5 * num1)), 3)
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board()

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()
pygame.quit()