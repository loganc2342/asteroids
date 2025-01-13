import pygame

from circleshape import CircleShape
from constants import (PLAYER_RADIUS,
                       PLAYER_TURN_SPEED,
                       PLAYER_MAX_SPEED,
                       PLAYER_ACCELERATION,
                       PLAYER_DECELERATION,
                       PLAYER_SHOOT_SPEED,
                       PLAYER_SHOOT_COOLDOWN,
                       PLAYER1,
                       PLAYER2,)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, player_num):
        super().__init__(x, y, PLAYER_RADIUS)
        self.player_num = player_num
        self.rotation = 0
        self.timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        acceleration = pygame.Vector2(0, 1)
        acceleration = acceleration.rotate(self.rotation)
        acceleration *= PLAYER_ACCELERATION
        self.acceleration = acceleration * dt

    def update(self, dt):
        if self.velocity.length() < PLAYER_MAX_SPEED * dt:
            self.velocity += self.acceleration
        self.position += self.velocity
        self.timer -= dt
        self.__check_input(dt)

    def __check_input(self, dt):
        keys = pygame.key.get_pressed()

        if self.player_num == PLAYER1:
            if keys[pygame.K_a]:
                self.rotate(-dt)

            if keys[pygame.K_d]:
                self.rotate(dt)

            if keys[pygame.K_w] or keys[pygame.K_s]:
                if keys[pygame.K_w]:
                    self.move(dt)

                if keys[pygame.K_s]:
                    self.move(-dt)
            else:
                self.__decelerate()

            if keys[pygame.K_SPACE]:
                self.shoot()

        elif self.player_num == PLAYER2:
            if keys[pygame.K_LEFT]:
                self.rotate(-dt)

            if keys[pygame.K_RIGHT]:
                self.rotate(dt)

            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                if keys[pygame.K_UP]:
                    self.move(dt)

                if keys[pygame.K_DOWN]:
                    self.move(-dt)
            else:
                self.__decelerate()

            if keys[pygame.K_RETURN]:
                self.shoot()
        

    def __decelerate(self):
        if self.velocity.length() > 0:
            deceleration = self.velocity.copy()
            deceleration /= self.velocity.length()
            deceleration *= PLAYER_DECELERATION

            if deceleration.length() > self.velocity.length():
                self.velocity = pygame.Vector2(0, 0)
                self.acceleration = pygame.Vector2(0, 0)
            else:
                self.velocity -= deceleration

    def shoot(self):
        if not self.timer > 0:
            self.timer = PLAYER_SHOOT_COOLDOWN
            shot = Shot(self.position.x, self.position.y)
            velocity = pygame.Vector2(0, 1)
            velocity = velocity.rotate(self.rotation)
            velocity *= PLAYER_SHOOT_SPEED
            shot.velocity = velocity