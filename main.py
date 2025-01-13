import argparse
import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot


def main():
    parser = argparse.ArgumentParser(
        prog="asteroids",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Runs the game 'Asteroids'.

        Player 1 Controls:
        W, S - forward and backward, respectively
        A, D - rotate left and right, respectively
        Space - shoot
        
        Player 2 Controls:
        Up, Down - forward and backward, respectively
        Left, Right - rotate left and right, respectively
        Return/Enter - shoot
        """,
    )
    parser.add_argument(
        "-m", "--multiplayer",
        help="add a second player to the game",
        action="store_true",
    )
    args = parser.parse_args()
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    asteroids = pygame.sprite.Group()
    players = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (players, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    if(args.multiplayer):
        player1 = Player(x - (PLAYER_RADIUS * 2), y, PLAYER1)
        player2 = Player(x + (PLAYER_RADIUS * 2), y, PLAYER2)
    else:
        player1 = Player(x, y, PLAYER1)

    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for u in updatable:
            u.update(dt)

        for asteroid in asteroids:
            for player in players:
                if asteroid.check_collision(player):
                    player.kill()
                    
                    if len(players) == 0:
                        print("\nGame over!\n")
                        sys.exit()

            for shot in shots:
                if shot.check_collision(asteroid):
                    shot.kill()
                    asteroid.split()

        screen.fill("black")

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()