#Name: Susan Doong
#Uniqname: shdoong
#Student ID: 07675004
#References: in class gold_game.py code, thenewboston Pygame tutorials on Youtube: https://www.youtube.com/watch?v=K5F-aGDIYaM

from pygame import *
from pygame.sprite import *
from random import *
import random 
import sys

#constants for program
DELAY = 1000;            #Seed a timer to move sprite

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)

FPS = 60

width = 800
height = 600

bgcolor = GREEN   #Color for background

clock = pygame.time.Clock()

#creating Sprite groups
monster_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Monster(Sprite):
    def __init__(self):
        Sprite.__init__(self) 
        self.image = image.load("monster.png").convert_alpha()
        self.size = self.image.get_size()
        size_inc = random.uniform(0.25, 2.5)
        #using transform.scale to make each monster a different size
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*size_inc), int(self.size[1]*size_inc)))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, 750)
        self.rect.y = randint(0, 550)
        
    def move(self):
        self.move_x = randint(-50, 50)
        self.move_y = randint(-50, 50)
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.rect.x > 760:
            self.rect.x -= 20
        if self.rect.y > 560:
            self.rect.y -= 20

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("player.png").convert_alpha()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

    def update(self):
        key = pygame.key.get_pressed()
        dist = 4 # distance moved in 1 frame
        if key[pygame.K_DOWN]: # down key
            self.rect.y += dist # move down
        elif key[pygame.K_UP]: # up key
            self.rect.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.rect.x += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.rect.x -= dist # move left

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def inc_size(self): #increases size of player when it eats smaller monsters
        self.size = self.image.get_size()
        if self.size[0] < 50 and self.size[1] < 63:
            self.image = pygame.transform.scale(self.image, (int(self.size[0]*1.3), int(self.size[1]*1.3)))
        self.size = self.image.get_size()

def make_monsters():
    for x in range(randint(20, 30)):
        monster = Monster()
        monster_sprites.add(monster)
        all_sprites.add(monster)

def message(msg, color, screencolor, screen, width, height):
    myfont = pygame.font.SysFont(None, 30)
    screen.fill(screencolor)
    label = myfont.render(msg, 1, color)
    screen.blit(label, (width, height))
    pygame.display.flip()

def main():
    movement = 10
    init()

    screen = display.set_mode((width, height))
    display.set_caption('Doong Pygame')

    make_monsters()

    player = Player()

    # creates a group of sprites so all can be updated at once
    sprites2 = RenderPlain(monster_sprites)

    time.set_timer(USEREVENT + 1, DELAY)

    gameExit = False
    gameOver = False

    message("Monster Eats Monster Game", BLACK, WHITE, screen, 250, 300) #display screen before game starts
    pygame.time.delay(2000) #delay game start

    # loop until user quits ------------- main --------------------- #
    while not gameExit:

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                break
      
            elif event.type == USEREVENT + 1: 
                for y in monster_sprites:
                    y.move() #each monster move in random direction

        remove = True

        collide_list = pygame.sprite.spritecollide(player, monster_sprites, remove) #collision detection

        for hit in collide_list:
            print ("monster size ", hit.rect.size)
            if player.rect.size < hit.rect.size: #checks if player is smaller than monster
                message("You got eaten!", RED, BLACK, screen, 300, 300)
                pygame.time.delay(2000)
                gameOver = True
            else:
                player.inc_size()
                print (player.rect.size)

        while gameOver == True:
            screen.fill(BLACK)
            message("Game over. Q to quit or P to play again.", RED, BLACK, screen, 200, 300)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #if key q is pressed
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_p: #if key p is pressed
                        monster_sprites.empty() #reset monster_sprites list
                        main()
            
        # refill background color so that we can paint sprites in new locations
        screen.fill(bgcolor)

        player.update()
        player.draw(screen)
        
        # update and redraw sprites
        monster_sprites.update()
        monster_sprites.draw(screen)
        
        display.update()

        clock.tick(FPS) #limits to 60 frames per second

main()
