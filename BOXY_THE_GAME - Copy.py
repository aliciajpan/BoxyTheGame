import pygame
import random
import time

pygame.init()

####### MUSIC #######

pygame.mixer.init() # initialize mixer for music
pygame.mixer.music.load("bkgd_music.mp3") # set up here allows music to play during start screen as well as main game
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) # (-1)means loops indefinitely

def main():

    ####### SET-UP #######

    black = (0, 0, 0)
    red = (255, 51, 51)
    blue = (0, 76, 153)

    clock = pygame.time.Clock()

    ####### KEY CO-ORDINATES #######

    x = 375 # used for inital player position 
    y = 250

    # black box = player
    black_top = x 
    black_left = y # separate variables to get rid of lag

    # red box = enemy
    red_top = 100
    red_left = 100

    #blue box = enemy2
    blue_top = 100
    blue_left = 300

    screen_top = 0 # edges of screen
    screen_bottom = 650 # dimensions account for size of squares (50x50)
    screen_left = 0
    screen_right = 450

    ####### IMPORT IMAGES #######

    star_image = pygame.image.load("star.png") # stars appear in random locations
    star = star_image.get_rect()                
    star.left = random.randrange(150, 600, 50)  # ensures no blit under SCORE text or in respawn box
    star.top = random.randrange(50, 400, 50)    # get outside of game loop for the 1st location

    respawn_image = pygame.image.load("respawn_box.png")
    respawn_box = respawn_image.get_rect()
    respawn_box.left = 595
    respawn_box.top = 395

    bkgd_image = pygame.image.load("bkgd.jpeg")
    game_over_screen = pygame.image.load("game_over.png")
    respawn_screen = pygame.image.load("respawn_screen.png")

    ####### GAME VARIABLES #######

    player_score = 0 # init outside of game loop to not reset everytime screen refreshes

    speed = 7
    enemy_speed = 1
    enemy2_speed = 3

    done = False

    while not done:

        screen.blit(bkgd_image, (0, 0))

        ####### EXIT #######

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                done = True # return to main menu (start screen)

        ####### TEXT #######

        myfont = pygame.font.SysFont('callisto', 40)
        score = myfont.render(("SCORE:"), 1, black)
        score_value = myfont.render(str(player_score), 1, black)

        ####### DRAW #######

        screen.blit(respawn_image, (respawn_box.left, respawn_box.top))

        screen.blit(star_image, (star.left, star.top))

        player = pygame.draw.rect(screen, black, (black_top, black_left, 50, 50), 0) # name for collision detection
        
        enemy = pygame.draw.rect(screen, red, (red_top, red_left, 50, 50), 0)

        enemy2 = pygame.draw.rect(screen, blue, (blue_top, blue_left, 50, 50), 0)

        ####### PLAYER MOVEMENT #######

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            black_left -= speed

        if keys[pygame.K_DOWN]:
            black_left += speed

        if keys[pygame.K_LEFT]:
            black_top -= speed

        if keys[pygame.K_RIGHT]:
            black_top += speed

        ####### ENEMY MOVEMENT #######

        #enemy

        if red_left > black_left: # enemy tracks player and follows
            red_left -= enemy_speed
        elif red_left == black_left:
            red_left = red_left
        else:
            red_left += enemy_speed

        if red_top > black_top:
            red_top -= enemy_speed
        elif red_top == black_top:
            red_top = red_top
        else:
            red_top += enemy_speed

        #enemy2 (faster, appears when player gets 50 points)

        if blue_left > black_left: 
            blue_left -= enemy2_speed
        elif blue_left == black_left:
            blue_left = blue_left
        else:
            blue_left += enemy2_speed

        if blue_top > black_top:
            blue_top -= enemy2_speed
        elif blue_top == black_top:
            blue_top = blue_top
        else:
            blue_top += enemy2_speed
    

        ####### SCREEN LIMITS #######
            
        if black_top >= screen_bottom: # ensures boxes do not leave limits of screen
            black_top = screen_bottom

        if black_top <= screen_top:
            black_top = screen_top

        if black_left <= screen_left: 
            black_left = screen_left

        if black_left >= screen_right:
            black_left = screen_right

        if red_top >= screen_bottom:
            red_top = screen_bottom

        if red_top <= screen_top:
            red_top = screen_top

        if red_left <= screen_left:
            red_left = screen_left

        if red_left >= screen_right:
            red_left = screen_right

        ####### STAR COLLECTION ####### 

        if player.colliderect(star):

            player_score += 10  # 1 star --> +10 points
            
            score_value = myfont.render(str(player_score), 1, black) # update score

            star.left = random.randrange(150, 600, 50)  # generate new star position
            star.top= random.randrange(50, 400, 50)

        screen.blit(score, (10, 10))
        screen.blit(score_value, (125, 10))

        ####### HIT BY ENEMY #######

        if enemy.colliderect(player): 

            pygame.draw.rect(screen, black, (black_top, black_left, 50, 50), 0)

            player_score -= 10  # hit enemy --> -10 points
     
            black_top = 620
            black_left = 425

            red_top = 100 # reset enemy location to make sure player is not cornered in respawn box 
            red_left = 100

        if enemy2.colliderect(player):

            pygame.draw.rect(screen, black, (black_top, black_left, 50, 50), 0)

            player_score -= 10 
     
            black_top = 620
            black_left = 425

            blue_top = 100
            blue_left = 300

            if player_score >= 0: # shows respawn screen (unless player has lost the game)

                screen.blit (respawn_screen, (0, 0))
                pygame.display.update()

                time.sleep(1)

        ####### RESPAWN BOX #######

        wall_box = pygame.Rect((595, 395, 100, 100))

        if player.colliderect(wall_box):
            if enemy.colliderect(wall_box):
                enemy_speed = 0 # enemies not allowed in respawn box while player is in respawn box
            if enemy2.colliderect(wall_box):
                enemy2_speed = 0
        else:
            enemy_speed = 1
            enemy2_speed = 3

        ####### END GAME WHEN PLAYER LOSES ALL POINTS #######

        if player_score < 0:
            screen.blit(bkgd_image, (0, 0))
            screen.blit(game_over_screen, (0, 0))

        ####### SCREEN DISPLAY + FPS #######

        pygame.display.update()
        
        clock.tick(60)

####### INTRO SCREEN + START GAME #######

start_screen_image = pygame.image.load("start_screen.jpeg")

size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("BOXY: The Game")

done = False

while not done: # separate loop for start screen

    screen.blit(start_screen_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main() # begin playing
         
    pygame.display.update() 
    
pygame.mixer.music.stop()    
pygame.quit()
