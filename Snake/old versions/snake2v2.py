import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green1 = (0, 255, 0)
green2  = (40, 215, 40)
blue = (50, 153, 213)

display_width = 600
display_height = 400

dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 30)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])


def gameLoop():
    #print("Game Loop")
    game_over = False
    game_close = False

    #print(" Player 1 Snake")
    x1 = display_width / 4
    y1 = display_height / 4
    x1_change = 0
    y1_change = 0
    snake_List1 = []
    Length_of_snake1 = 1

    #print(" Player 2 Snake")
    x2 = 3*display_width / 4
    y2 = 3*display_height / 4
    x2_change = 0
    y2_change = 0
    snake_List2 = []
    Length_of_snake2 = 1

    #print(" Food")
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    food2x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    food2y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
    food2_exist = True

    winner = ""
    while not game_over:

        while game_close:
            dis.fill(blue)
            message(winner+" Player Wins! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        #print(" Handle events")
        for i,event in enumerate(pygame.event.get()):
            print(i, event)
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

        #print(" check for out of bounds for player 1")
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
            winner = "Red"

        #print(" check for out of bounds for player 2")
        if x2 >= display_width or x2 < 0 or y2 >= display_height or y2 < 0:
            game_close = True
            winner = "Black"

        #print(" update positions of players")
        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        dis.fill(blue)

        #print(" draw food on the screen")
        pygame.draw.rect(dis, green1, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, green2, [food2x, food2y, snake_block, snake_block])


        #print(" update snake 1 and check for collision with player 2")
        snake_Head1 = [x1, y1]
        snake_List1.append(snake_Head1)

        if len(snake_List1) > Length_of_snake1:
            del snake_List1[0]
            
        for x in snake_List1[:-1]:
            if x == snake_Head1:
                    game_close = True
                    winner = "Red"
        for x in snake_List2[:-1]:
            if x == snake_Head1:
                    game_close = True
                    winner = "Red"

        for x in snake_List1:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

        #print(" update snake 2 and check for collision with player 1")
        snake_Head2 = [x2, y2]
        snake_List2.append(snake_Head2)

        if len(snake_List2) > Length_of_snake2:
            del snake_List2[0]

        for x in snake_List2[:-1]:
            if x == snake_Head2:
                    game_close = True
                    winner = "Black"
        for x in snake_List1[:-1]:
            if x == snake_Head2:
                    game_close = True
                    winner = "Black"
                    

        for x in snake_List2:
            pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])

        #print(" update display")
        pygame.display.update()

        #print(" check for food collision for player 1")
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake1 += 5

        #print(" check for food collision for player 2")
        if x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake2 += 5

        if food2_exist:
            if x1 == food2x and y1 == food2y:
                food2_exist = False
                Length_of_snake1 += 2

            if x2 == food2x and y2 == food2y:
                food2_exist = False
                Length_of_snake2 += 2
                
        if not food2_exist:
            food2x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            food2y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            food2_exist = True
                
        #print(" check for collision between snake heads")
        if x1 == x2 and y1 == y2:
            game_close = True

        clock.tick(snake_speed)

    pygame.quit()
gameLoop()
