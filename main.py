import pygame
import json
import os
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    score_font = pygame.font.SysFont(None, 40)
    current_hs_font = pygame.font.SysFont(None, 30, False, True)
    gameover_font = pygame.font.SysFont(None, 100, False, True)
    background_image = pygame.image.load("./assets/img/background.png")
    high_score = 0
    new_high_score = False

    # Open the file and load the existing high score - no error handling... yet
    with open('data.json', 'r') as file:
        saved_data = json.load(file)
        high_score = saved_data['high_score']

    # Create the explosion sound effect
    explode_sound = pygame.mixer.Sound("./assets/sounds/explosion.mp3")
    
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
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
        if alive:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collision(player):
                    alive = False

                    if score > high_score:
                        new_high_score = True
                        high_score = score
            
                for shot in shots:
                    if asteroid.collision(shot):
                        explode_sound.play()
                        asteroid.split()
                        shot.kill()
                        score += 1

        screen.fill((0,0,0))
        screen.blit(background_image, (0,0))

        score_display = score_font.render("Score: " + str(score), True, "White")
        screen.blit(score_display, (25,25))
        highscore_display = current_hs_font.render("High Score: " + str(high_score), True, "White")
        screen.blit(highscore_display, (SCREEN_WIDTH - 150,25))

        if alive:
            for d in drawable:
                d.draw(screen)
        else: 
            if new_high_score:
                highscore_font = pygame.font.SysFont(None, 50, False, True)
                over = highscore_font.render("Game Over! NEW high score... now saving...", True, "White")
            else:
                over = gameover_font.render("Game Over!", True, "White")
           
            rect = over.get_rect(center=(SCREEN_HEIGHT/2, SCREEN_WIDTH/2))
            screen.blit(over, (rect))

        pygame.display.flip()
        
        # Limit frame rate to 180fps
        dt = clock.tick(180) / 1000

    if new_high_score:
        saved_data = {'high_score': high_score}
        with open('data.json', 'w') as file:
            json.dump(saved_data, file, indent=4)
        
if __name__ == "__main__":
    main()