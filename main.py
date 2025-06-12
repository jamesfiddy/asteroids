import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

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

        for a in asteroids:
            if a.collision(player):
                print("Game over!")
                exit()

        for asteroid in asteroids:
            for s in shots:
                if asteroid.collision(s):
                    asteroid.kill()
                    s.kill()

        screen.fill((0,0,0))

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        
        # Limit frame rate to 60fps
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()