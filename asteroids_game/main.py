# this allows us to use code from
# the open-source pygame library
# throughout this file
import sys
import pygame
from constants import *
from player import Player, Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #This ensures that every instance of the Player class is automatically added to these groups upon creation.
    Player.containers = (updatable, drawable)

    #This ensures that every instance of the Asteroid class is automatically added to these groups upon creation.
    Asteroid.containers = (updatable, drawable, asteroids)

    Shot.containers = (updatable, drawable, shots)

    AsteroidField.containers = (updatable)


    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    dt = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(color="black")
        updatable.update(dt)

        # check if collision happened
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game Over!")
                sys.exit(0)

            # destroy asteroids colliding with bullets
            for bullet in shots:
                if asteroid.collides_with(bullet):
                    asteroid.split()
                    bullet.kill()

        for object in drawable:
            object.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()
