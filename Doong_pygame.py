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

width = 700
height = 500

bgcolor = green   #Color taken from background of sprite

class Monster(Sprite):
    def __init__(self):
        Sprite.__init__(self) #importan
        self.image = image.load("monster.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        size_inc = random.uniform(0, 2)
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*size_inc), int(self.size[1]*size_inc)))
        self.current_randX = randint(0, 650)
        self.current_randY = randint(0, 450)
        self.rect.center = (self.current_randX, self.current_randY)

    def move(self):
        move_x = randint(-50, 50)
        move_y = randint(-50, 50)
        self.rect.x = self.rect.x +  move_x
        self.rect.y = self.rect.y + move_y

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x_change = width/2
        self.y_change = height/2

    def move(self):
        key = pygame.key.get_pressed()
        dist = 0.25
  
        if key[pygame.K_DOWN]: # down key
            self.y_change += dist # move down
        elif key[pygame.K_UP]: # up key
            self.y_change -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x_change += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x_change -= dist # move left

    def draw(self, surface):
        surface.blit(self.image, (self.x_change, self.y_change))

movement = 10
init()

screen = display.set_mode((width, height))
display.set_caption('Doong Pygame')

sprites2 = pygame.sprite.Group()

for x in range(randint(15, 25)):
    monster = Monster()
    sprites2.add(monster)

player = Player()
# creates a group of sprites so all can be updated at once
sprites = RenderPlain(sprites2)

hits = 0
time.set_timer(USEREVENT + 1, DELAY)

movement = 10
start_x = 0
start_y = 0
x_change = 0
y_change = 0

gameExit = False
# loop until user quits
while not gameExit:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            break

        elif event.type == USEREVENT + 1: 
            for y in sprites2:
                y.move()
    # refill background color so that we can paint sprites in new locations
    screen.fill(bgcolor)

    player.move()
    player.draw(screen)
    
    # update and redraw sprites
    sprites.update()
    sprites.draw(screen)
    display.update()
