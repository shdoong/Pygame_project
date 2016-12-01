#Name: Susan Doong
#Uniqname: shdoong
#Student ID: 07675004
#References: in class gold_game.py code, thenewboston Pygame tutorials on Youtube: https://www.youtube.com/watch?v=K5F-aGDIYaM,
#http://www.pygame.org/docs/ref/transform.html, http://www.pygame.org/docs/ref/rect.html

from pygame import *
from pygame.sprite import *
from random import *
import random 
import sys

#constants for program
DELAY = 1000; #Seed a timer to move sprite

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
HONEYDEW = (240, 255, 240)

FPS = 60

width = 800
height = 600

bgcolor = HONEYDEW  #Color for background

clock = pygame.time.Clock()

#creating Sprite groups
cookie_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

pygame.init()

class Cookie(Sprite):
    def __init__(self, cookie_max): #cookie_max represents the maximize size increase the cookie can have. Limits size.
        Sprite.__init__(self) 
        self.image = image.load("cookie.png").convert_alpha()
        self.size = self.image.get_size()
        size_inc = random.uniform(0.35, cookie_max)
        #using transform.scale to make each monster a different size
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*size_inc), int(self.size[1]*size_inc)))
        self.rect = self.image.get_rect()
        self.rect.x = randint(50, 750) #randomizes starting location
        self.rect.y = randint(50, 550)
        
    def move(self): #cookie's random movements
        self.move_x = randint(-50, 50)
        self.move_y = randint(-50, 50)
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        #adding boundaries to cookie movement
        if self.rect.x > 750:
            self.rect.x -= 20
        if self.rect.x < 50:
            self.rect.x += 20
        if self.rect.y > 560: 
            self.rect.y -= 20
        if self.rect.y < 50:
            self.rect.y += 20

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("cookiemonster2.png").convert_alpha()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

    def update(self): #handles player movement and boundaries
        key = pygame.key.get_pressed()
        dist = 4 # distance moved in 1 frame
        if key[pygame.K_DOWN]: # down key
            self.rect.y += dist # move down
            if self.rect.y < 0: #adds boundaries if player tries to go off screen
                self.rect.y = 0
            elif self.rect.y > height - 25:
                self.rect.y = height - 25
        elif key[pygame.K_UP]: # up key
            self.rect.y -= dist # move up
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > height - 25:
                self.rect.y = height - 25
        if key[pygame.K_RIGHT]: # right key
            self.rect.x += dist # move right
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > width - 25:
                self.rect.x = width - 25
        elif key[pygame.K_LEFT]: # left key
            self.rect.x -= dist # move left
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > width - 25:
                self.rect.x = width - 25
        elif key[pygame.K_q]:
            exit()

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def inc_size(self): #increases size of player when it eats smaller monsters
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]+2), int(self.size[1]+2))) #increases size visually
        self.rect.inflate_ip(2, 2) #increase size internally

def make_cookies(minc, maxc, cookie_max):
    for x in range(randint(minc, maxc)): #makes between minc and maxc random cookies
        cookie = Cookie(cookie_max)
        cookie_sprites.add(cookie)
        all_sprites.add(cookie)

def message(msg, color, screencolor, screen, width, height):
    myfont = pygame.font.SysFont(None, 30)
    screen.fill(screencolor)
    label = myfont.render(msg, 1, color)
    screen.blit(label, (width, height))
    pygame.display.flip()

screen = display.set_mode((width, height))

#Intro screens and instructions
message("Monster Eats Cookie Game", BLACK, WHITE, screen, 250, 300) #display screen before game starts
pygame.time.delay(2000)
message("Eat as many cookies as you can but don't get squashed by bigger cookies!", BLACK, WHITE, screen, 30, 325)
pygame.time.delay(3000)
message("You can only eat smaller cookies, but you get bigger with each cookie you eat!", BLACK, WHITE, screen, 20, 325)
pygame.time.delay(3000) #delay game start

def main():
    score = 0
    movement = 10

    display.set_caption('Doong Pygame')

    player = Player()

    # creates a group of sprites so all can be updated at once
    sprites2 = RenderPlain(cookie_sprites)

    time.set_timer(USEREVENT + 1, DELAY)

    gameExit = False
    gameOver = False

    minc = 0
    maxc = 0

    intro = True 

    #intro screen
    while intro:
        message("Game Level: Press 1 for Easy, 2 for Medium, 3 for Hard", BLACK, WHITE, screen, 130, 300) #allows player to pick level
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #assigns number of cookies and cookie sizes based on difficulty level
                if event.key == pygame.K_1: 
                    minc = 8
                    maxc = 12
                    cookie_max = 1.1
                    intro = False
                if event.key == pygame.K_2: 
                    minc = 15
                    maxc = 20
                    cookie_max = 1.4
                    intro = False
                if event.key == pygame.K_3: 
                    minc = 23
                    maxc = 28
                    cookie_max = 1.8
                    intro = False

    make_cookies(minc, maxc, cookie_max)
    # loop until user quits ------------- main --------------------- #
    while not gameExit:

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                break
      
            elif event.type == USEREVENT + 1: 
                for y in cookie_sprites:
                    y.move() #each cookie move in random direction

        remove = True

        collide_list = pygame.sprite.spritecollide(player, cookie_sprites, remove) #collision detection

        for hit in collide_list:
            score += 1
            mixer.Sound("bitesound.wav").play() #play sound each time monster eats a cookie

            #testing for losing
            if player.rect.size < hit.rect.size: #checks if player is smaller than monster
                print ("cookie: ", hit.rect.size)
                print ("player: ", player.rect.size)
                mixer.Sound("lost.wav").play()
                message("Game Over. You got squashed by a giant cookie!", RED, BLACK, screen, 170, 300)
                pygame.time.delay(2000)
                gameOver = True

            else:
                player.inc_size()

                #testing for winning
                if len(cookie_sprites) == 0: #if no more cookies, then player wins
                    screen.fill(WHITE)
                    mixer.Sound("tada.wav").play()
                    message("You win! You ate all the cookies!", GREEN, WHITE, screen, 225, 300)
                    pygame.time.delay(2000)
                    gameOver = True

        #Option for user to play again or quit once they lose or win
        while gameOver == True:
            screen.fill(BLACK)
            message("Q to quit or P to play again.", RED, BLACK, screen, 250, 300)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #if key q is pressed, exit game
                        exit()
                    if event.key == pygame.K_p: #if key p is pressed, restart game
                        cookie_sprites.empty() #reset cookie_sprites list
                        main()
            
        # refill background color 
        screen.fill(bgcolor)

        myfont2 = font.Font(None, 25)
        t = myfont2.render("Cookies Eaten = " + str(score), False, BLACK) #shows score counter
        screen.blit(t, (320, 0))  

        player.update()
        player.draw(screen)
        
        # update and redraw sprites
        cookie_sprites.update()
        cookie_sprites.draw(screen)
        
        display.update()

        clock.tick(FPS) #limits to 60 frames per second

main() #calls main function to run the game
