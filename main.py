import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pixel")

# Colors
white = (255, 255, 255)
ground_color = (0, 0, 0)

gravity = 1
player_speed = 10
jump_height = 20
on_the_ground = False
game_over = False

class end_level(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 3):
                img = pygame.image.load(f'img/next_level_point{num}.png')
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
    def update(self,target) -> None:
        global on_the_ground
        self.counter += 1
        cooldown = 4
        if self.counter > cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        if self.rect.colliderect(target.rect): 
            on_the_ground = True


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('img/cude.png')  # Red color for the player
        self.image = self.original_image  # Red color for the player
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
    def update(self) -> None:
        
        global on_the_ground
        
        if game_over == False:
            self.vel += gravity
            if self.vel > 10:
                self.vel = 10

            # Check for collisions with the ground
            if self.rect.y >= 476:
                on_the_ground = True
                self.rect.y = 476

            self.rect.y += int(self.vel)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= player_speed 
                self.image = pygame.transform.flip(self.original_image, True, False)
                
                
            if keys[pygame.K_RIGHT] and self.rect.right < width:
                self.rect.x += player_speed
                

            if keys[pygame.K_SPACE] and on_the_ground:
                on_the_ground = False
                self.vel =-(jump_height)
            
class Double_jump_object(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                img = pygame.image.load(f'img/double_circul{num}.png')
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
    def update(self,target):
            global on_the_ground
            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            if self.rect.colliderect(target.rect): 
                on_the_ground = True


player_group = pygame.sprite.Group()
double_jump_group = pygame.sprite.Group()
player = Player(100, int(height / 2))
player_group.add(player)
double_jump_poit_1= Double_jump_object(int((width+200)/2), int(height/2))
double_jump_poit_2= Double_jump_object(int((width)), int(height/2))
double_jump_group.add(double_jump_poit_1)
double_jump_group.add(double_jump_poit_2)
en_lvl = end_level(20,20)
#Animation, coin, levels, moving platform 


ground_width = width
ground_height = 50
ground_rect = pygame.Rect(0, height - ground_height, ground_width, ground_height)

while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    player_group.update()
    double_jump_group.update(player)
    en_lvl.update(player)


    # Screen
    screen.fill(white)

    # Draw the ground
    pygame.draw.rect(screen, ground_color, ground_rect)

    # Draw the player
    player_group.draw(screen)
    # Draw the double_jump_poit
    double_jump_group.draw(screen)
    #end_point
    screen.blit(en_lvl.image, en_lvl.rect)

    

    pygame.display.update()
