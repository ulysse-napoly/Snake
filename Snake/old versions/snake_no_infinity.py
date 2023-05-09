import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow =(255,255,0)
grey = (150,150,150)
purple = (75,0,130)
black = (0, 0, 0)
red = (213, 50, 80)
green1 = (0, 255, 0)
green2  = (40, 215, 40)
green_bonus = (0,150,0)
blue = (50, 153, 213)

display_width = 600
display_height = 400

dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont(None, 30)

shield_ico = pygame.transform.scale(pygame.image.load("shield_ico.png"), (snake_block*3, snake_block*3))
speed_ico = pygame.transform.scale(pygame.image.load("speed_ico.png"), (snake_block*3, snake_block*3))
growth_ico = pygame.transform.scale(pygame.image.load("growth_ico.png"),(snake_block*3, snake_block*3))
magnet_ico = pygame.transform.scale(pygame.image.load("magnet_ico.png"), (snake_block*3, snake_block*3))

powerup_types = [{'name': 'invincible', 'color': grey, 'duration': 10, 'icon': shield_ico},
                 {'name': 'speed boost', 'color': yellow, 'duration': 10, 'icon': speed_ico},
                 {'name': 'growth multiplier', 'color': green_bonus, 'duration': 10, 'icon': growth_ico},
                 {'name': 'magnet', 'color': red, 'duration': 10, 'icon': magnet_ico}]

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])
    
def show_scores(Length_of_snake1,Length_of_snake2,font_score):
    # Update scores
    score1 = Length_of_snake1
    score2 = Length_of_snake2
    
    # Draw scores on top of screen
    text_score1 = font_score.render(f"Player 1 Score: {score1}", True, white)
    text_score2 = font_score.render(f"Player 2 Score: {score2}", True, white)
    dis.blit(text_score1, (10, 10))
    dis.blit(text_score2, (display_width - text_score2.get_width() - 10, 10))
def show_timer(player, color, time_left):
    font_style = pygame.font.SysFont(None, 80)
    timer_text = str(int(time_left)).zfill(2)
    text = font_style.render(timer_text, True, color)
    if player == 2:
        dis.blit(text, (display_width - text.get_width() - 10, 50))
    else:
        dis.blit(text, (10, 50))
     
def gameLoop():
    #print("Game Loop")
    game_over = False
    game_close = False

    #print(" Player 1 Snake")
    x1 = display_width / 4
    y1 = display_height / 4
    x1_change = 0
    y1_change = 0
    snake_state1 = 'normal'
    snake_List1 = []
    Length_of_snake1 = 1
    growth_multiplier1 = 1
    magnet1 = 1


    #print(" Player 2 Snake")
    x2 = 3*display_width / 4
    y2 = 3*display_height / 4
    x2_change = 0
    y2_change = 0
    snake_state2 = 'normal'
    snake_List2 = []
    Length_of_snake2 = 1
    growth_multiplier2 = 1
    magnet2 = 1

    #print(" Food")
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    food2x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    food2y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
    food2_exist = True
    
    #print(" Power ups")
    powerup_chance = 0.05
    powerup_timer = 0
    POWERUP_DURATION = 0 
    powerup_active = False
    powerup_type = None
    powerup_x = None
    powerup_y = None
    powerup_time1 = None
    powerup_time2 = None

    # Set up font objects
    font_score = pygame.font.SysFont(None, 25)
    font_winner = pygame.font.SysFont(None, 30)
    
    winner = ""
    while not game_over:
        while game_close:
            dis.fill(blue)
            message(winner+" Player Wins! Press Q-Quit or C-Play Again", red)
            show_scores(Length_of_snake1,Length_of_snake2,font_score)
            pygame.display.update()

            events =  pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        
        #print(" Handle events")
        events = [event for event in pygame.event.get() if event.type == pygame.QUIT or event.type == pygame.KEYDOWN]
        quit_event = [event for event in events if event.type == pygame.QUIT]
        keysP1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        keysP2 = [pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d]
        eventP1 = [event for event in events if event.key in keysP1][:1]
        eventP2 = [event for event in events if event.key in keysP2][:1]
        handled_events = quit_event + eventP1 + eventP2
        for event in handled_events:
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and x2_change == 0:
                    x2_change = -snake_block
                    y2_change = 0
                elif event.key == pygame.K_d and x2_change == 0:
                    x2_change = snake_block
                    y2_change = 0
                elif event.key == pygame.K_z and y2_change == 0:
                    y2_change = -snake_block
                    x2_change = 0
                elif event.key == pygame.K_s and y2_change == 0:
                    y2_change = snake_block
                    x2_change = 0
                elif event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    
        #print("Power ups")
        if not powerup_active and random.random() < powerup_chance:
            powerup_type = random.choice(powerup_types)
            powerup_x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            powerup_y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            powerup_active = True
            power_up_color = powerup_type['color']
            powerup_icon = powerup_type['icon']
            powerup_timer = powerup_type['duration'] * snake_speed
            POWERUP_DURATION = powerup_type['duration'] 

        #print(" check for out of bounds for player 1")
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0 and snake_state1 != 'invincible':
            game_close = True
            winner = "White"

        #print(" check for out of bounds for player 2")
        if x2 >= display_width or x2 < 0 or y2 >= display_height or y2 < 0 and snake_state1 != 'invincible':
            game_close = True
            winner = "Black"

        #print(" update positions of players")
        if snake_state1 == 'speed boost':
            x1 += 2*x1_change
            y1 += 2*y1_change
        else :
            x1 += 1*x1_change
            y1 += 1*y1_change
            
        if snake_state2 == 'speed boost':
            x2 += 2*x2_change
            y2 += 2*y2_change
        else :
            x2 += 1*x2_change
            y2 += 1*y2_change

        dis.fill(blue)

        #print(" draw food on the screen")
        pygame.draw.rect(dis, green1, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, green2, [food2x, food2y, snake_block, snake_block])

        #print(" handle power ups")
        #if powerup_active and powerup_type != None:
        #    pygame.draw.rect(dis, powerup_type['color'], [powerup_x, powerup_y, snake_block, snake_block])
        if powerup_active and powerup_type != None:
            dis.blit(powerup_icon, (powerup_x-10, powerup_y-10))

            powerup_timer -= 1
            if powerup_timer <= 0:
                powerup_active = False
                powerup_type = None

            if abs(x1 - powerup_x) < magnet1*3*snake_block and abs(y1 - powerup_y) < magnet1*3*snake_block and powerup_active:
                powerup_time1 = time.time()  # set power-up time for player 1
                if powerup_type['name'] == 'invincible':
                    snake_state1 = 'invincible'
                elif powerup_type['name'] == 'speed boost':
                    snake_state1 = 'speed boost'
                    magnet1 = 1.5
                elif powerup_type['name'] == 'growth multiplier':
                    growth_multiplier1 = 3
                elif powerup_type['name'] == 'magnet':
                    magnet1 = 5
                powerup_type = None
            elif abs(x2 - powerup_x) < magnet2*2*snake_block and abs(y2 - powerup_y) < magnet2*2*snake_block and powerup_active:
                powerup_time2 = time.time()  # set power-up time for player 2
                if powerup_type['name'] == 'invincible':
                    snake_state2 = 'invincible'
                elif powerup_type['name'] == 'speed boost':
                    snake_state2 = 'speed boost'
                    magnet2 = 1.5
                elif powerup_type['name'] == 'growth multiplier':
                    growth_multiplier2 = 3
                elif powerup_type['name'] == 'magnet':
                    magnet2 = 5
                powerup_type = None


        # check power-up effect duration for player 1
        if powerup_time1 is not None and time.time() - powerup_time1 >= POWERUP_DURATION:
            snake_state1 = 'normal'
            powerup_time1 = None
            powerup_active = False
            growth_multiplier1 = 1
            magnet1 = 1


        # check power-up effect duration for player 2
        if powerup_time2 is not None and time.time() - powerup_time2 >= POWERUP_DURATION:
            snake_state2 = 'normal'
            powerup_time2 = None
            powerup_active = False
            growth_multiplier2 = 1
            magnet2 = 1

        # show power-up timer if active
        if powerup_active and powerup_time1 is not None:
            show_timer(1,power_up_color,POWERUP_DURATION - (time.time() - powerup_time1))
        elif powerup_active and powerup_time2 is not None:
            show_timer(2,power_up_color,POWERUP_DURATION - (time.time() - powerup_time2))
            
        #print(" update snake 1 and check for collision with player 2")
        snake_Head1 = [x1, y1]
        snake_List1.append(snake_Head1)

        if len(snake_List1) > Length_of_snake1:
            del snake_List1[0]
            
        for x in snake_List1[:-1]:
            if x == snake_Head1 and snake_state1 != 'invincible':
                    game_close = True
                    winner = "White"
        for x in snake_List2[:-1]:
            if x == snake_Head1 and snake_state1 != 'invincible':
                    game_close = True
                    winner = "White"

        for x in snake_List1:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

        #print(" update snake 2 and check for collision with player 1")
        snake_Head2 = [x2, y2]
        snake_List2.append(snake_Head2)

        if len(snake_List2) > Length_of_snake2:
            del snake_List2[0]

        for x in snake_List2[:-1]:
            if x == snake_Head2 and snake_state2 != 'invincible':
                    game_close = True
                    winner = "Black"
        for x in snake_List1[:-1]:
            if x == snake_Head2 and snake_state2 != 'invincible':
                    game_close = True
                    winner = "Black"
                    

        for x in snake_List2:
            pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

        # Update scores
        show_scores(Length_of_snake1,Length_of_snake2,font_score)

        #print(" update display")
        pygame.display.update()

        #print(" check for food collision for player 1")
        if abs(x1 - foodx) < magnet1*snake_block and abs(y1 - foody) < magnet1*snake_block:
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            Length_of_snake1 += growth_multiplier1*3

        #print(" check for food collision for player 2")
        if abs(x2 - foodx) < magnet2*snake_block and abs(y2 - foody) < magnet2*snake_block:
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            Length_of_snake2 += growth_multiplier2*3

        if food2_exist:
            if abs(x1 - food2x) < magnet1*snake_block and abs(y1 - food2y) < magnet1*snake_block:
                food2_exist = False
                Length_of_snake1 += growth_multiplier1*2

            if abs(x2 - food2x) < magnet2*snake_block and abs(y2 - food2y) < magnet2*snake_block:
                food2_exist = False
                Length_of_snake2 += growth_multiplier2*2
                
        if not food2_exist:
            food2x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            food2y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            food2_exist = True
                
        #print(" check for collision between snake heads")
        if x1 == x2 and y1 == y2 and snake_state1 != 'invincible' and snake_state2 != 'invincible':
            winner = "No"
            game_close = True
            

        clock.tick(snake_speed)

    pygame.quit()
gameLoop()














