import pygame

# Initialize pygame
pygame.init()

# Set up the display
width, height = 480, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Test')

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up font
pygame.font.init()
font = pygame.font.SysFont(None, 40)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with white
    screen.fill(white)
    
    # Draw a red rectangle
    pygame.draw.rect(screen, red, (100, 100, 200, 300))
    
    # Draw a green circle
    pygame.draw.circle(screen, green, (width//2, height//2), 50)
    
    # Draw text
    text = font.render('Pygame is working!', True, (0, 0, 0))
    screen.blit(text, (width//2 - text.get_width()//2, 50))
    
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
