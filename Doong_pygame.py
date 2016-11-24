from pygame import *
from pygame.sprite import *
from random import *
import random 

DELAY = 1000;            #Seed a timer to move sprite
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (34, 139, 34)
blue = (0, 0, 255)

width = 800
height = 600

bgcolor = green   #Color taken from background of sprite

monster_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Monster(Sprite):
    def __init__(self):
        Sprite.__init__(self) #importan
        self.image = image.load("monster.png").convert_alpha()
        self.size = self.image.get_size()
        size_inc = random.uniform(0.25, 2)
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
        self.rect = self.image.get_rect()

    def update(self):
        key = pygame.key.get_pressed()
       
        dist = 1 # distance moved in 1 frame
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

def make_monsters():
    for x in range(randint(20, 30)):
        monster = Monster()
        monster_sprites.add(monster)
        all_sprites.add(monster)

def main():
    movement = 10
    init()

    screen = display.set_mode((width, height))
    display.set_caption('Doong Pygame')

    make_monsters()

    player = Player()
    #player_sprite.add(player)
    #all_sprites.add(player)

    # creates a group of sprites so all can be updated at once
    sprites2 = RenderPlain(monster_sprites)

    time.set_timer(USEREVENT + 1, DELAY)

    gameExit = False

    # loop until user quits ------------- main --------------------- #
    while not gameExit:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                break
      
            elif event.type == USEREVENT + 1: 
                for y in monster_sprites:
                    y.move()

        remove = False

        collide_list = pygame.sprite.spritecollide(player, monster_sprites, remove)

        for hit in collide_list:
            if player.rect.size > hit.rect.size:
                remove = True 
                
        if len(collide_list) > 0:
            print (collide_list)
            print ("hi")
            
        # refill background color so that we can paint sprites in new locations
        screen.fill(bgcolor)

        player.update()
        player.draw(screen)
        
        # update and redraw sprites
        monster_sprites.update()
        monster_sprites.draw(screen)
        
        display.update()

main()
