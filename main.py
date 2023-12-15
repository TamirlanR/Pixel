from typing import Any
import pygame
import sys



pygame.init()

clock = pygame.time.Clock()
fps = 60

# Screen
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pixel")


#Global veriables 
gravity = 1
player_speed = 5
mirror_work =False
jump_height = 14
on_the_ground = False
double_jump = False
game_over = False
walking=False

#function to draw the text: 
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
    
class coin(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
            pygame.sprite.Sprite.__init__(self)
            pygame.mixer.init()
            self.coin_sound = pygame.mixer.Sound('sound/coin_sound.mp3')
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 7):
                img = pygame.image.load(f'img/coin{num}.png')
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.currentx=x
            self.currenty=y

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
            self.kill()
            target.points+=1
            self.coin_sound.play()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.standing_animation_right = []
        self.standing_animation_left=[]
        self.right_walk=[]
        self.left_walk=[]
        self.falling_animation=pygame.image.load('img/falling.png')
        self.double_jumping_right=pygame.image.load('img/double_jump.png')
        
        self.index = 0
        self.counter = 0
        for num in range(1, 6):
            img_stand_right = pygame.image.load(f'img/selesta{num}.png')
            #img_stand_right = pygame.transform.scale(img_stand_right, (40, 80))
            self.standing_animation_right.append(img_stand_right)
            img_stand_left = pygame.transform.flip(img_stand_right, True, False) 
            self.standing_animation_left.append(img_stand_left)
        for num in range(1,7):
            img_right = pygame.image.load(f'img/walk{num}.png')
            #img_right = pygame.transform.scale(img_right, (40, 80))
            self.right_walk.append(img_right)
            img_left= pygame.transform.flip(img_right, True, False) 
            self.left_walk.append(img_left)
        
        self.image = self.standing_animation_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = 1 # 1 right # -1 left 
        self.vel = 0
        self.points = 0
        self.on_platform = False
        self.platform_vel = 0
    def update(self,platforms) -> None:
        cooldown = 6
        self.counter+=1
        global walking
        global double_jump
        global on_the_ground
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.top == platform.rect.bottom:
                    # Player hit the head, start falling
                    self.rect.y += 25  # Adjust the player's position slightly
                    on_the_ground = False

                on_the_ground = True
                self.vel = 0
                self.rect.y = platform.rect.y - self.rect.height
                self.on_platform = True
                self.platform_vel = platform.platform_vel

                break
            else:
                self.on_platform = False
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= player_speed 
            walking=True
            self.direction=-1
        
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += player_speed
            walking=True
            self.direction=1
            
        if keys[pygame.K_SPACE] and (on_the_ground or double_jump):
            jump_height =13 if (on_the_ground==True or self.on_platform ==True) else 20
            on_the_ground = False
            double_jump = False
            self.vel =-(jump_height)
        
        if keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            walking=False
            
        #handal animation
        if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.standing_animation_right):
                    self.index = 0
                if self.direction==1 and walking and on_the_ground:
                    self.image=self.right_walk[self.index]
                if self.direction==-1 and walking and on_the_ground:
                    self.image=self.left_walk[self.index]
                if self.direction==1 and not walking and on_the_ground:
                    self.image=self.standing_animation_right[self.index]
                if self.direction==-1 and not walking and on_the_ground:
                    self.image=self.standing_animation_left[self.index]
                if self.direction==1 and not on_the_ground:
                    self.image=self.falling_animation
                if self.direction==-1 and not on_the_ground:
                    self.image=pygame.transform.flip(self.falling_animation,True,False)
                if double_jump==True and self.direction==1 and not on_the_ground:
                    self.image=self.double_jumping_right
                if double_jump==True and self.direction==-1 and not on_the_ground:
                    self.image=pygame.transform.flip(self.double_jumping_right,True,False)
        
        if game_over == False:
        

            # Check for collisions with the ground
            if self.rect.y >= 507:
                on_the_ground = True
                self.rect.y = 507

            if not self.on_platform:
                self.vel += gravity
                if self.vel > 10:
                    self.vel = 10
                self.rect.y += int(self.vel)

            if self.on_platform:
                # Update the player's position based on the platform's movement
                self.rect.x -= self.platform_vel*2

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
            global double_jump
            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            if self.rect.colliderect(target.rect): 
                double_jump = True
            if not self.rect.colliderect(target.rect): 
                double_jump = False

class Platform(pygame.sprite.Sprite):
     def __init__(self, x,y) -> None:
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.image.load('img/platform.png')
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          self.currentx=x
          self.currenty=y
          self.platform_vel=3
     def move(self):
          self.image = self.image
          self.rect.x -= self.platform_vel
          if self.rect.right < 0:
            self.rect.x = width
               

background=pygame.image.load('img/bg3.png')
ground = pygame.image.load('img/ground.png')

#Group objects
player_group = pygame.sprite.Group()
double_jump_group = pygame.sprite.Group()
player = Player(200, int(height/2))
player_group.add(player)
double_jump_poit_1= Double_jump_object(int((width+200)/2), int(height/1.2)+10)
double_jump_poit_2= Double_jump_object(int((width)), int(height/2))
double_jump_group.add(double_jump_poit_1)
double_jump_group.add(double_jump_poit_2)
coins_group = pygame.sprite.Group()
coin1 = coin(250,300)
coins_group.add(coin1)
coin2 = coin(350 ,325)
coins_group.add(coin2)
platform_group = pygame.sprite.Group()
platform1 = Platform(400, 500)
platform2 = Platform(600, 400)
platform_group.add(platform1, platform2)
#Animation, coin, levels, moving platform 
text_col = (255, 255, 255)
text = "COINS: "
font = pygame.font.Font('font/Grand9K Pixel.ttf',16)
#music
main_music = pygame.mixer.Sound('sound/main_sound.mp3')
main_music.play(-1)

while True:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Move platforms
    for platform in platform_group:
        platform.move()

    screen.blit(background, (0,0))
    # Update
    player_group.update(platform_group)
    double_jump_group.update(player)
    coins_group.update(player)
    
    # Draw
    draw_text(text+str(player.points),font,text_col,20,20)
    # Screen
    

    # Draw the ground
    screen.blit(ground, (0, 575))
    platform_group.draw(screen)
    # Draw the player
    player_group.draw(screen)
    # Draw the double_jump_poit
    double_jump_group.draw(screen)
    #end_point
    coins_group.draw(screen)
    pygame.display.update()
