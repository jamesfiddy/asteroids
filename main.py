import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    score_font = pygame.font.SysFont(None, 40)
    gameover_font = pygame.font.SysFont(None, 100, False, True)
    background_image = pygame.image.load("./assets/img/background.png")
    
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    alive = True
    running = True

    # Create groups of objects for Pygame
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    Shot.containers = (updatable, drawable, shots)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
        if alive:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collision(player):
                    alive = False
            
                for shot in shots:
                    if asteroid.collision(shot):
                        asteroid.split()
                        shot.kill()
                        score += 1

        screen.fill((0,0,0))
        screen.blit(background_image, (0,0))

        s = score_font.render("Score: " + str(score), True, "White")
        screen.blit(s, (25,25))

        if alive:
            for d in drawable:
                d.draw(screen)
        else: 
            over = gameover_font.render("Game Over!", True, "White")
            rect = over.get_rect(center=(SCREEN_HEIGHT/2, SCREEN_WIDTH/2))
            screen.blit(over, (rect))

        pygame.display.flip()
        
        # Limit frame rate to 180fps
        dt = clock.tick(180) / 1000
        
if __name__ == "__main__":
    main()