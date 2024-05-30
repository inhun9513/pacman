#PacMan from scatch  
from board import boards
import math
import pygame

pygame.init()
WIDTH = 900
HEIGHT = 950 
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60 
#font = pygame.font.Font('freesansbold.tff, 20')
level = boards 
color = 'blue'
PI = math.pi
#player images 
player_images = []
for i in range(1,5): #each time out of the four (because four pac man pics)
    #transform = load image, scale image
    player_images.append(pygame.transform.scale(pygame.image.load   
                                                                              #scale: x width, y height
                                                 (f'assets/player_images/{i}.png'), (45,45)))
#next, let's get pac-man drawn on the screen
#guess and check for the starting position 
player_x = 450 
player_y = 663
direction = 0 
counter = 0
flicker = False
# R, L, U, D
#Each 'False' stands for cannot turn right, left, up, & down
#eg. Can i turn right right now? Can I turn left? Can I turn up? Can I turn down? 
turns_allowed = [False, False, False, False] 
direction_command = 0
player_speed = 2
score = 0 
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
moving = False
startup_counter = 0
lives = 3 #represents 3 spare lives 

#def draw_misc():
    #score_text = font.render(f'Score: {score}', True, 'white')
    #screen.blit(score_text, (10, 920))
    #1h 48: if powerup: 
    #          pygame.draw.circle(screen, 'blue', (140, 930), 15)
    #for i in range(lives): #1 h 50
        #screen.blit(pygame.transform.scale(player_images[0],(30, 30)), (650 + i * 40, 915))


def check_collisions(score, power, power_count, eaten_ghosts): #scoring and eating the dots and powerups
    if 0 < player_x < 870: 
        num1 = (HEIGHT - 50)// 32
        num2 = WIDTH // 30
        #1st: what row we are in #2: 
        if level[center_y // num1][center_x // num2] == 1: 
            level[center_y // num1][center_x // num2] = 0 #now we want the dot to be empty/EATEN by P.M.
            score += 10
        if level[center_y // num1][center_x // num2] == 2: 
            level[center_y // num1][center_x // num2] = 0 #now we want the dot to be empty/EATEN by P.M.
            score += 50
            #1 h 41 
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    
    return score, power, power_counter, eaten_ghost


def draw_board():
    num1 = ((HEIGHT-50)//32)  
    num2 = ((WIDTH // 30))  
    #define a function meant to draw the board in pygame
    for i in range(len(level)):
        for j in range(len(level[i])): 
            #(if statement for 0 isn't required)
            #goal: 2 circles
            if level[i][j] == 1: 
                pygame.draw.circle(
                    screen,'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            elif level[i][j] == 2 and not flicker:                                                            
                pygame.draw.circle(screen,'white', (j * num2 + (0.5 * num2), 
                                                    i * num1 + (0.5 * num1)), 10) #20.25
            elif level[i][j] == 3: #vertical line
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            elif level[i][j] == 4: #horizontal line
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5*num1)), 3)
            elif level[i][j] == 5: #curve line:  #29 min
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.5)), (i * num1 + (0.5 * num1)), 
                                                num2, num1], 0, PI/2, 3)
            elif level[i][j] == 6: #curve line: 
                pygame.draw.arc(screen, color, 
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), 
                                                num2, num1], PI/2, PI, 3)
            elif level[i][j] == 7: #curve line: 
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.5 * num1)), 
                                                num2, num1], PI, 3 * PI/2, 3)
            elif level[i][j] == 8: #curve line: 
                pygame.draw.arc(screen, color, 
                                [(j * num2 - (num2 * 0.5)), (i * num1 - (0.5 * num1)), 
                                                num2, num1], 3 * PI/2, 2 * PI, 3)
            elif level[i][j] == 9: #horizontal line
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5*num1)), 3)


def draw_player(): 
    #0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    #pacman can face 4 different directions, so we need a variable to check which directions he's facing 
                       #if this is the direction, the image we want to 'blip' onto the screen is-
                       #from player_images, the variable we defined standing for our 4 images
    if direction == 0: 
        #counter variable meant to track how fast pac-man should move
        #player_x, player_y are variables representing position which the pacman should be at/start at
        screen.blit(player_images[counter // 5], (player_x,player_y))

    #upper if statement act as a sample to the ones below-
    #because the only thing changing are the direction
    #elif statements are present because only one direction at a time should be happening
    elif direction == 1: 
                    #'transform.flip' : this turns the originally RIGHT pac-man and FLIPS it to LEFT
                    #True- flip it to the X direction (WE WANT), False- flip it to the Y direction (NO)
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x,player_y))
    
    elif direction == 2: 
                                                                        #90 symbolizes rotate 90 degrees
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x,player_y))
    
    elif direction == 3:                 
                                                                         #270 degrees rotate
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x,player_y))


def check_position(center_x, center_y): 
    turns = [False, False, False, False]
    #confirm whether player's "center position" pathways are clear above, below and to the sides
    #remember! in board, cubes #0,1,2 is what the player CAN pass through
    #hence, this center checker of num1 and num2 checks that center entity just like the circles
    num1 = (HEIGHT-50)//32  
    num2 = (WIDTH//30)
    num3 = 15 #essentially for collisions not to look messy, so pac-man stops at a ceirtan step not ON cols
    


    #2) #remember our array, turns[0] = RIGHT, turns[1] = LEFT, turns[2] = UP, turns[3] = DOWN
        #G.S.: if itsn't on the edge, if direction is something, if it's column and row maths-
        #are less than 3, an empty space, turns[whatever] = True, it can move in that direction
    
    if center_x // 30 < 29: 
        if direction == 0: 
            if level[center_y // num1][(center_x - num3) // num2] < 3: 
                turns[1] = True
        if direction == 1: 
            if level[center_y // num1][(center_x + num3) // num2] < 3: 
                turns[0] = True
        if direction == 2: 
            if level[(center_y + num3)// num1][center_x // num2] < 3: 
                turns[3] = True
        if direction == 3: 
            if level[(center_y - num3)// num1][center_x // num2] < 3: 
                turns[2] = True

        if direction == 2 or direction == 3: 
            if 12 <= center_x % num2 <= 18: 
                if level[(center_y + num3) // num1][center_x // num2] < 3: 
                    turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3: 
                    turns[2] = True
            if 12 <= center_y % num1 <= 18: 
                if level[center_y // num1][(center_x - num2) // num2] < 3: 
                    turns[1] = True
                if level[center_y // num1][(center_x + num2) // num2] < 3: 
                    turns[0] = True      
        if direction == 0 or direction == 1: 
            if 12 <= center_x % num2 <= 18: 
                if level[(center_y + num1) // num1][center_x // num2] < 3: 
                    turns[3] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3: 
                    turns[2] = True
            if 12 <= center_y % num1 <= 18: 
                if level[center_y // num1][(center_x - num3) // num2] < 3: 
                    turns[1] = True
                if level[center_y // num1][(center_x + num3) // num2] < 3: 
                    turns[0] = True
    else: 
        turns[0] = True 
        turns[1] = True
    
    return turns


def move_player(player_x, player_y): #move the player, setting up joystick  
    #r, l, u, d
    if direction == 0 and turns_allowed[0]: 
        player_x += player_speed
    elif direction == 1 and turns_allowed[1]: 
        player_x -= player_speed
    elif direction == 2 and turns_allowed[2]: 
        player_y -= player_speed
    elif direction == 3 and turns_allowed[3]: 
        player_y += player_speed
    return player_x, player_y

run = True 
while run: 
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3: #3 symbolizes something that's plenty of time for the flicker
            flicker = False
    else: 
        counter = 0 #1 h 46- setting up powerup active timer
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600: 
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180: 
        moving = False
        startup_counter += 1
    else: 
        moving = True 

    screen.fill('black')
    draw_board()
    draw_player()
    #draw_misc()
    center_x = player_x + 23
    center_y = player_y + 24
    pygame.draw.circle(screen,'white', (center_x, center_y), 2)
    turns_allowed = check_position(center_x, center_y) 
    if moving: #1 h  47 
        player_x, player_y = move_player(player_x, player_y)
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            run = False                       
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
                                #if you kept on pressing right but accidentally pressed left and let go
                                #what would happen nexT/
            if event.key == pygame.K_RIGHT and direction_command == 0 : 
                direction_command = direction             
            if event.key == pygame.K_LEFT and direction_command == 1:  
                direction_command = direction              
            if event.key == pygame.K_UP and direction_command == 2:    
                direction_command = direction               
            if event.key == pygame.K_DOWN and direction_command == 3:  
                direction_command = direction  

    #for i in range(4)
    if direction_command == 0 and turns_allowed[0]: 
        direction = 0
    if direction_command == 1 and turns_allowed[1]: 
        direction = 1
    if direction_command == 2 and turns_allowed[2]: 
        direction = 2
    if direction_command == 3 and turns_allowed[3]: 
        direction = 3

    if player_x > 900:  #then direction goes to the left
            player_x = -47
    elif player_x < -50: #then direction goes to the right
            player_x = 897
            


    pygame.display.flip()

pygame.quit()