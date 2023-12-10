import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Collision Example")

# Set up colors
white = (255, 255, 255)
ground_color = (0, 0, 0)  # Brown color for the ground
gravity = 1

# Set up the ground rectangle
ground_width = width
ground_height = 50
ground_rect = pygame.Rect(0, height - ground_height, ground_width, ground_height)

# Set up the player
player_width = 50
player_height = 50
player_color = (0, 0, 255)  # Blue color for the player
player_rect = pygame.Rect((width - player_width) // 2, height - ground_height - player_height, player_width, player_height)

# Set up player movement
player_speed = 1
jump_height = 3
is_jumping = False
on_the_ground = False

class Player():
    def __init__(self) -> None:
        pass
    

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < width:
        player_rect.x += player_speed
    if keys[pygame.K_SPACE] and on_the_ground:
        is_jumping = True
        on_the_ground = False

    # Apply gravity and jumping
    if is_jumping:
        player_rect.y -= jump_height
        is_jumping = False
    

    # Check if player is on the ground
    on_the_ground = player_rect.colliderect(ground_rect)

    # Reset jump if player touches the ground
    if on_the_ground:
        player_rect.y = ground_rect.top - player_rect.height

    # Draw background
    screen.fill(white)

    # Draw the ground
    pygame.draw.rect(screen, ground_color, ground_rect)

    # Draw the player
    pygame.draw.rect(screen, player_color, player_rect)

    # Update the display
    pygame.display.flip()

# Exit the program
pygame.quit()
sys.exit()



def update(self):
    # ... (остальная логика)
    if keys[pygame.K_LEFT] and self.rect.left > 0:
        self.rect.x -= player_speed
        self.image = pygame.transform.flip(self.original_image, True, False)  # Поворот спрайта влево
    if keys[pygame.K_RIGHT] and self.rect.right < width:
        self.rect.x += player_speed
        self.image = self.original_image  # Возвращаем исходный спрайт