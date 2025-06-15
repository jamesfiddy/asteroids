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
    
    clock = pygame.time.Clock()
    dt = 0
    score = 0

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                exit()
            
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
                    score += 1

        s = score_font.render("Score: " + str(score), True, "White")

        screen.fill((0,0,0))
        screen.blit(s, (25,25))

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        
        # Limit frame rate to 60fps
        dt = clock.tick(180) / 1000
        
if __name__ == "__main__":
    main()