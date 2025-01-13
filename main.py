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
    parser.add_argument(
        "-v", "--verbose",
        help="give a detailed score breakdown upon game over",
        action="store_true"
    )
    args = parser.parse_args()
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0
    score = 0
    kind_count = [-1, 0, 0, 0] # first value is placeholder to prevent off-by-one error

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
                    seconds_passed = pygame.time.get_ticks() // 1000
                    score += seconds_passed * POINTS_PER_SECOND

                    if len(players) == 0:
                        print("\nGame over!")

                        if args.verbose:
                            __score_breakdown(kind_count, score, seconds_passed)
                        else:
                            print(f"Score: {score}\n")

                        sys.exit()

            for shot in shots:
                if shot.check_collision(asteroid):
                    shot.kill()
                    try:
                        points, kind = __give_points(asteroid)
                        score += points
                        kind_count[kind] += 1
                    except Exception as e:
                        print(f"WARN: {e}")
                    asteroid.split()

        screen.fill("black")

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


def __give_points(asteroid):
    kind = asteroid.radius // ASTEROID_MIN_RADIUS
    
    if kind == SMALL_KIND:
        points = SMALL_POINTS
    elif kind == MEDIUM_KIND:
        points = MEDIUM_POINTS
    elif kind == LARGE_KIND:
        points = LARGE_POINTS
    else:
        raise Exception("unknown asteroid kind")
    
    return points, kind


def __score_breakdown(kind_count, score, seconds_passed):
    print(f"\nLarge Asteroids Destroyed: {kind_count[LARGE_KIND]} x {LARGE_POINTS} = {kind_count[LARGE_KIND] * LARGE_POINTS}")
    print(f"Medium Asteroids Destroyed: {kind_count[MEDIUM_KIND]} x {MEDIUM_POINTS} = {kind_count[MEDIUM_KIND] * MEDIUM_POINTS}")
    print(f"Small Asteroids Destroyed: {kind_count[SMALL_KIND]} x {SMALL_POINTS} = {kind_count[SMALL_KIND] * SMALL_POINTS}")
    print(f"Seconds Survived: {seconds_passed} x {POINTS_PER_SECOND} = {seconds_passed * POINTS_PER_SECOND}")
    print(f"\nTotal Score: {score}\n")


if __name__ == "__main__":
    main()