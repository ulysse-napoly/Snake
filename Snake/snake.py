import pygame
import time
import random
import sys
from pygame import mixer

print("-"*30)
print("-"*30)
game_mode = sys.argv[1] if len(sys.argv) > 1 else "classic"
print("Game Mode : ",game_mode )
print(" -"*10)
difficulty = eval(sys.argv[2]) if len(sys.argv) > 2 else 2
print("Difficulty : ", difficulty)
print(" -"*10)
game_music_id = sys.argv[3] if len(sys.argv) > 3 else "classic"
game_music_name = "gfunk" if game_music_id == "g" else game_music_id
print("Game Music : ",game_music_name )
print(" -"*10)
music_volume = eval(sys.argv[4])/100 if len(sys.argv) > 4 else 0.4
print("Music Volume : ", int(music_volume*100), "%")
print("-"*30)
print("-"*30)

if "info" in game_mode :
    print("Game Modes : \n --> infinity : Wrap around edges\n --> god : Be invincible and compete for points")
    print("-"*30)
    print("Game Difficulty : \n --> 1 : Normal\n --> 2 : Hard\n --> 3 : Good Luck\n (decimals are accepted)")
    print("-"*30)
    print("Game Themes : \n --> classic\n --> epic\n --> gfunk\n --> retro\n --> metal\n --> chill")
    print("-"*30)
    print("-"*30)

pygame.init()



#############################
######### Graphics  #########
#############################
white = (255, 255, 255)
yellow =(255,255,0)
grey = (100,100,100)
purple = (75,0,130)
black = (0, 0, 0)
red = (213, 50, 80)
green1 = (0, 255, 0)
green2 = (40, 215, 40)
green_bonus = (0,150,0)
blue = (50, 153, 213)
blue_freeze = (0,0,255)

snake_block = 20


display_width = 60*snake_block
display_height = 40*snake_block

dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
max_timer = 10

def load_image(path, scale=1) : 
    return pygame.transform.scale(pygame.image.load(path), (snake_block*scale, snake_block*scale))

shield_ico = load_image("graphics/shield_ico.png", 3)
speed_ico = load_image("graphics/speed_ico.png", 3)
growth_ico = load_image("graphics/growth_ico.png", 3)
magnet_ico = load_image("graphics/magnet_ico.png", 3)
reverse_ico = load_image("graphics/reverse_ico.png", 3)
freeze_ico = load_image("graphics/freeze_ico.png", 3)

pommeV_ico = load_image("graphics/pommeV_ico.png")
pommeR_ico = load_image("graphics/pommeR_ico.png")
pommeOr_ico = load_image("graphics/pommeOr_ico.png")


black_player_ico = load_image("graphics/python_ico.png", 2)
white_player_ico = load_image("graphics/python_ico.png", 2)



#############################
##########  Audio  ##########
#############################
mixer.init()
# Load main theme 
if game_music_name == "retro" :
    game_theme_music_path = "retro_theme.wav" 
else :
    game_theme_music_path = game_music_name+"_theme.mp3"
game_theme_music_path = "sounds/"+game_theme_music_path
pygame.mixer.music.load(game_theme_music_path)


# Modifiers
powerup_list = [{'name': 'Invincible', 'color': grey, 'duration': 10, 'icon': shield_ico},
                 {'name': 'Speed Boost', 'color': yellow, 'duration': 7, 'icon': speed_ico},
                 {'name': 'Growth Multiplier', 'color': green_bonus, 'duration': 8, 'icon': growth_ico},
                 {'name': 'Magnet', 'color': red, 'duration': 10, 'icon': magnet_ico},
                 {'name': 'Reverse', 'color': purple, 'duration': 5, 'icon': reverse_ico},
                 {'name': 'Freeze', 'color': blue_freeze, 'duration': 5, 'icon': freeze_ico}]





class Snake():
    def __init__(self, x, y, player_name, controls, game, ico, color):
        self.game = game
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.length = 1
        self.player_name = player_name
        self.controls = controls
        self.head_ico = ico
        self.color = color
        self.reset_power_up_variators()

    def reset_power_up_variators(self):
        self.game.powerup_time[self.player_name] = None
        self.growth_multiplier = 1
        self.magnet = 1
        self.control_variation = 1
        self.movement_variation = 1
        if self.game.god_mode :
            self.state = 'invincible'
        else :
            self.state = 'normal'

    def handle_events(self, events):
        # We consider only the last event in player keys that were pressed
        events = [event for event in events if event.type != pygame.QUIT and event.key in list(self.controls.values()) ][-1:]
        for event in events :
            if self.control_variation != 0 :
                if event.key == self.controls['left'] and self.x_change == 0:
                    self.x_change = -snake_block*self.control_variation
                    self.y_change = 0
                elif event.key == self.controls['right'] and self.x_change == 0:
                    self.x_change = snake_block*self.control_variation
                    self.y_change = 0
                elif event.key == self.controls['up'] and self.y_change == 0:
                    self.y_change = -snake_block*self.control_variation
                    self.x_change = 0
                elif event.key == self.controls['down'] and self.y_change == 0:
                    self.y_change = snake_block*self.control_variation
                    self.x_change = 0

    def move(self):
        self.x += self.movement_variation*self.x_change
        self.y += self.movement_variation*self.y_change
    
    def check_len(self):
        while len(self.snake1.snake_list) > self.snake1.length:
                    del self.snake1.snake_list[0]

    def is_out_of(self, x_max, y_max):
        return self.x >= x_max or self.x < 0 or self.y >= y_max or self.y < 0
        
    
    def check_edge_collision(self):
        if self.game.infinity_mode or 'invincible' in self.state:
            # Wrap around the screen for player 
            self.x %= display_width
            self.y %= display_height
        else :
            # Check for out of bounds for player (only in classic mode)
            if self.is_out_of(display_width,display_height) :
                self.game.game_ending = True
                self.game.winner = self.player_name
            
    def eat_powerup(self):
        other_players_list = [snake for snake in self.game.players if snake != self]
        if abs(self.x - self.game.powerup_x) < self.magnet*2*snake_block and abs(self.y - self.game.powerup_y) < self.magnet*2*snake_block and self.game.powerup_active:
            if self.game.powerup_type != None :
                    self.game.powerup_time[self.player_name] = time.time()  # set power-up time for player 1
                    self.game.powerup_sound.play()
                    if self.game.powerup_type['name'] == 'Invincible':
                        self.state += 'invincible'
                    elif self.game.powerup_type['name'] == 'Speed Boost':
                        self.state = 'speed boost'
                        self.movement_variation *=2
                        self.magnet = 2
                    elif self.game.powerup_type['name'] == 'Growth Multiplier':
                        self.growth_multiplier = 3
                    elif self.game.powerup_type['name'] == 'Magnet':
                        self.magnet = 5
                    elif self.game.powerup_type['name'] == 'Reverse':
                        for adverse_snake in other_players_list:
                            adverse_snake.control_variation *= -1
                    elif self.game.powerup_type['name'] == 'Freeze':
                        for adverse_snake in other_players_list:
                            adverse_snake.movement_variation = 0
                            adverse_snake.control_variation = 0
                            adverse_snake.state += 'invincible'
                    self.game.powerup_type = None
    
    def check_powerup_duration(self): 
        if self.game.powerup_time[self.player_name] is not None and time.time() - self.game.powerup_time[self.player_name] >= self.game.powerup_duration:
            for snake in self.game.players :
                snake.reset_power_up_variators()
            self.game.powerup_active = False 

class Food():
    def __init__(self, game, points, ico): 
        self.x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
        self.y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
        self.exist = True
        self.points = points 
        self.ico = ico 
        self.game = game

    def get_eaten(self, snake):
        other_players_list = [enemy_snake for enemy_snake in self.game.players if snake != enemy_snake and "invincible" not in snake.state]
        if self.points > 0 : 
            self.exist = False
            self.game.eating_sound.play()
            snake.length += snake.growth_multiplier*self.points
        elif len(other_players_list)>0 :
            for adverse_snake in other_players_list : 
                self.exist = False
                self.game.eating_sound.play()
                adverse_snake.length += adverse_snake.growth_multiplier*self.points
                     
class SnakeGame():
    
    def __init__(self, game_mode = "classic", difficulty=1):

        self.infinity_mode = 'infinity' in game_mode
        self.time_mode = 'time' in game_mode
        self.god_mode = 'god' in game_mode
        self.difficulty = difficulty
        

        self.global_scores = {}
        self.global_scores["Black"] = 0
        self.global_scores["White"] = 0
                
        self.eating_sound = mixer.Sound('sounds/crunch.wav')
        self.powerup_sound = mixer.Sound('sounds/powerup.wav')

        self.font_end = pygame.font.SysFont(None, 40)
        self.font_win = pygame.font.SysFont(None, 40)
        self.font_scores = pygame.font.SysFont(None, 25)

        self.controls = {}
        self.controls['Black'] = {'left' : pygame.K_LEFT, 'right' : pygame.K_RIGHT, 'up' : pygame.K_UP, 'down' : pygame.K_DOWN}
        self.controls['White'] = {'left' : pygame.K_q, 'right' : pygame.K_d, 'up' : pygame.K_z, 'down' : pygame.K_s}

        self.init_game()

    def init_game(self):
        self.option_menu_open = False

        self.game_over = False
        self.game_ending = False
        self.winner = None

        self.foods = []

        self.snake_speed = 10*self.difficulty

        self.init_powerups()
        self.init_players()
    
    def init_players(self):
        for name in ['Black', 'White']:
            self.powerup_time[name] = None
        self.snake1_ico = black_player_ico
        self.snake2_ico = white_player_ico
        self.snake1 = Snake(3*display_width//4, 3*display_height//4, 'Black', self.controls['Black'], self, black_player_ico, black)
        self.snake2 = Snake(display_width//4, display_height//4, 'White', self.controls['White'], self, white_player_ico, white)
        self.players = [self.snake1, self.snake2]

    def init_powerups(self):
        self.powerup_types = powerup_list
        self.powerup_chance = 0.05
        self.powerup_timer = 0
        self.powerup_name = ''
        self.powerup_duration = 0 
        self.powerup_active = False
        self.powerup_type = None
        self.powerup_color = None
        self.powerup_icon = None
        self.powerup_x = None
        self.powerup_y = None
        self.powerup_time = {}
    
    def show_scores(self, final=False):
        # Update scores
        score1 = self.snake1.length
        score2 = self.snake2.length
        
        # Draw scores on top of screen
        text_score1 = self.font_scores.render(f"Black Score: {score1}", True, white)
        text_score2 = self.font_scores.render(f"White Score: {score2}", True, white)
        dis.blit(text_score2, (10, 10))
        dis.blit(text_score1, (display_width - text_score2.get_width() - 10, 10))

        if final :
            # Update scores
            score1 = self.global_scores['Black']
            score2 = self.global_scores['White']
            
            # Draw scores on top of screen
            text_win1 = self.font_win.render(f"Black Wins: {score1}", True, white)
            text_win2 = self.font_win.render(f"White Wins: {score2}", True, white)
            dis.blit(text_win2, (30, 30))
            dis.blit(text_win1, (display_width - text_score2.get_width() - 90, 30))           

    def show_timer(self,snake, color, time_left, name="-"):
        # Show Power up name :
        type = self.font_win.render(f"{name}", True, color)

        font_style = pygame.font.SysFont(None, 80)
        time_to_print = max(0,int(time_left))
        timer_text = str(time_to_print).zfill(2)
        time = font_style.render(timer_text, True, color)
        if snake.player_name == 'Black':
            dis.blit(time, (display_width - time.get_width() - 10, 50))
            dis.blit(type, (display_width - type.get_width() - 10, 100))
        else:
            dis.blit(time, (10, 50))
            dis.blit(type, (10, 100))

    def show_game_timer(self,time_left):
        # Show time left if time mode activated 
        if self.time_mode:
            font_style = pygame.font.SysFont(None, 80)
            time_to_print = max(0,int(time_left))
            timer_text = str(time_to_print).zfill(2)
            time = font_style.render(timer_text, True, red)
            dis.blit(time, (display_width//2, 30))

    def message(self, msg, color, y_offset = 0):
        mesg = self.font_end.render(msg, True, color)
        dis.blit(mesg, [display_width / 4, display_height / 3 + y_offset])

    def draw_board(self):
        dis.fill(blue)
        #print(self.game_ending)
        #print(" draw food on the screen")
        for food in self.foods :
            dis.blit(food.ico, (food.x, food.y))

    def draw_players(self):
        for snake in self.players :
            for x in snake.snake_list:
                    pygame.draw.rect(dis, snake.color, [x[0], x[1], snake_block-1, snake_block-1])
            dis.blit(snake.head_ico, (snake.x-snake_block//2, snake.y-snake_block//2))
        
    def option_menu_display(self, y = snake_block):
        diff = str(int(self.difficulty*10)/10)
        self.message("        Press I to toggle Infinity Edges : " + ("On" if self.infinity_mode else "Off"), red, y_offset=4*snake_block + y)
        self.message("            Press T to toggle Time Mode : " + ("On" if self.time_mode else "Off"), red, y_offset=6*snake_block + y)
        self.message("             Press G to toggle God Mode : " + ("On" if self.god_mode else "Off"), red, y_offset=8*snake_block + y)
        self.message("    Press <- or -> to change difficulty : " + "  < "+(diff)+" >", red, y_offset=10*snake_block + y)
        pygame.display.update()

    def handle_option_inputs(self, event):
        if self.option_menu_open and event.key == pygame.K_i:
            self.infinity_mode = not self.infinity_mode
        if self.option_menu_open and event.key == pygame.K_t:
            self.time_mode = not self.time_mode
        if self.option_menu_open and event.key == pygame.K_g:
            self.god_mode = not self.god_mode
        if self.option_menu_open and event.key == pygame.K_LEFT:
            self.difficulty -= 0.5 if self.difficulty > 0.5 else 0
        if self.option_menu_open and event.key == pygame.K_RIGHT:
            self.difficulty += 0.5

    def game_over_menu(self):
        while self.game_ending:
            dis.fill(blue)

            self.message(self.winner+" Player Wins! Press E-Exit or C-Play Again", red)
            self.message("   Press SPACEBAR to display game options", red, y_offset=2*snake_block)

            self.show_scores(final=True)

            if self.option_menu_open :
                self.option_menu_display()

            pygame.mixer.music.stop()
            pygame.display.update()

            events =  pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.game_over = True
                    self.game_ending = False
                    return 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                        self.game_over = True
                        self.game_ending = False
                        return
                    if event.key == pygame.K_c or event.key == pygame.K_RETURN:
                        self.init_game()
                        self.gameLoop()
                    if event.key == pygame.K_SPACE:
                        self.option_menu_open = not self.option_menu_open
                    # Handle Options changes
                    self.handle_option_inputs(event)
                    
                
            clock.tick(30)

    def gameLoop(self):

        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(music_volume)
        
    
        #print(self.game_ending)
        #print(" Food")
    
        self.foods.append(Food(self, 3, pommeV_ico))
        self.foods.append(Food(self, 3, pommeV_ico))
        self.foods.append(Food(self, 3, pommeV_ico))
        #self.foods.append(Food(self, 6, pommeOr_ico))
        self.foods.append(Food(self, -2, pommeR_ico))

    
        
        # Set up timer 
        start_time = time.time()
        # 60 seconds limit for time mode
        max_time = 60*snake_block

        self.winner = ""
        while not self.game_over:
            # If game has ended, add self.winner score
            if self.game_ending :
                if self.winner in self.global_scores.keys():
                    self.global_scores[self.winner] +=1

                self.game_over_menu()
                            
            #print(self.game_ending)
            #print(" Handle events")
            events = [event for event in pygame.event.get() if event.type == pygame.QUIT or event.type == pygame.KEYDOWN]
            self.snake1.handle_events(events)
            self.snake2.handle_events(events)
            quit_event = [event for event in events if event.type == pygame.QUIT]
            for event in quit_event:
                if event.type == pygame.QUIT:
                    self.game_over = True
            
                        
            
            #print("Power ups")
            #print(self.game_ending)
            #print(self.powerup_active)
            if not self.powerup_active and random.random() < self.powerup_chance:
                self.powerup_type = random.choice(self.powerup_types)
                self.powerup_x = round(random.randrange(2*snake_block, display_width - 2*snake_block) / snake_block) * snake_block
                self.powerup_y = round(random.randrange(2*snake_block, display_height - 2*snake_block) / snake_block) * snake_block
                self.powerup_active = True
                self.powerup_name = self.powerup_type['name']
                self.powerup_color = self.powerup_type['color']
                self.powerup_icon = self.powerup_type['icon']
                self.powerup_timer = self.powerup_type['duration'] * self.snake_speed
                self.powerup_duration = self.powerup_type['duration'] 

            #print("Draw Board and Power Ups and apples")
            self.draw_board()

            #print("Snakes Moving")
            for snake in self.players :
                snake.move()

            for snake in self.players :
                snake.check_edge_collision()
            
            
            #print(self.game_ending)
            #print(" update snake 1 and check for collision with player 2")
            if self.snake1.movement_variation != 0 :
                snake_Head1 = [self.snake1.x, self.snake1.y]
                self.snake1.snake_list.append(snake_Head1)

            while len(self.snake1.snake_list) > self.snake1.length:
                del self.snake1.snake_list[0]

                
            for x in self.snake1.snake_list[:-1]:
                if x == snake_Head1 and 'invincible' not in self.snake1.state :
                        self.game_ending = True
                        self.winner = "White"
                        #print("Hit himself")
                        
            for x in self.snake2.snake_list[:-1]:
                if x == snake_Head1 and 'invincible' not in self.snake1.state :
                        self.game_ending = True
                        self.winner = "White"
                        #print("Hit Other")
                        
            #print(self.game_ending)
            #print(" update snake 2 and check for collision with player 1")
            if self.snake2.movement_variation != 0 :
                snake_Head2 = [self.snake2.x, self.snake2.y]
                self.snake2.snake_list.append(snake_Head2)

            while len(self.snake2.snake_list) > self.snake2.length:
                del self.snake2.snake_list[0]

            for x in self.snake2.snake_list[:-1]:
                if x == snake_Head2 and 'invincible' not in self.snake2.state :
                        self.game_ending = True
                        self.winner = "Black"
                        #print("Hit himself")
                        
            for x in self.snake1.snake_list[:-1]:
                if x == snake_Head2 and 'invincible' not in self.snake2.state :
                        self.game_ending = True
                        self.winner = "Black"
                        #print("Hit Other")
                        
                        

            self.draw_players()
            
            max_time -= 1
            self.show_game_timer((max_time - (time.time()-start_time))//snake_block)

            if (max_time - (time.time()-start_time)) <= 0 and self.time_mode:
                if self.snake1.length > self.snake2.length :
                    self.winner = 'Black'
                elif self.snake1.length < self.snake2.length :
                    self.winner = 'White'
                else :
                    self.winner = "No"
                self.game_ending = True


            #print(self.game_ending)
            #print(" handle power ups")
            #if self.powerup_active and self.powerup_type != None:
            #    pygame.draw.rect(dis, self.powerup_type['color'], [self.powerup_x, self.powerup_y, snake_block, snake_block])
            if self.powerup_active and self.powerup_type != None:
                dis.blit(self.powerup_icon, (self.powerup_x-snake_block, self.powerup_y-snake_block))
                self.powerup_timer -= 1
                if self.powerup_timer <= 0:
                    self.powerup_active = False
                    self.powerup_type = None

                for snake in self.players :
                    snake.eat_powerup()

            # check power-up effect duration for player 1
            for snake in self.players :
                snake.check_powerup_duration()
                

            # show power-up timer if active
            if self.powerup_active and self.powerup_time['Black'] is not None:
                self.show_timer(self.snake1,self.powerup_color,self.powerup_duration - (time.time() - self.powerup_time['Black']), name=self.powerup_name)
            elif self.powerup_active and self.powerup_time['White'] is not None:
                self.show_timer(self.snake2,self.powerup_color,self.powerup_duration - (time.time() - self.powerup_time['White']), name=self.powerup_name)
                
            # Update scores
            self.show_scores()

            #print(self.game_ending)
            #print(" update display")
            pygame.display.update()
            
            #print(self.game_ending)
            
            for food in self.foods:
                for snake in game.players :
                    if abs(snake.x - food.x) < snake.magnet*snake_block and abs(snake.y - food.y) < snake.magnet*snake_block:
                        food.get_eaten(snake)

                if not food.exist:
                    points = food.points
                    ico = food.ico
                    self.foods.remove(food)
                    self.foods.append(Food(self, points, ico))


            #print("Prevent Apple to make snake length < 0")
            self.snake1.length = max(1, self.snake1.length)
            self.snake2.length = max(1, self.snake2.length)

            #print(self.game_ending)
            #print(self.snake1.state, self.snake2.state)
            #print(" check for collision between snake heads")
            if self.snake1.x == self.snake2.x and self.snake1.y == self.snake2.y and 'invincible' not in self.snake1.state  and 'invincible' not in self.snake2.state :
                if self.snake1.length > self.snake2.length :
                    self.winner = 'Black'
                    
                elif self.snake1.length < self.snake2.length :
                    self.winner = 'White'
                    
                else :
                    self.winner = "No"
                self.game_ending = True
                
            clock.tick(self.snake_speed)

            

        
game = SnakeGame(game_mode, difficulty)
game.gameLoop()
pygame.quit()
