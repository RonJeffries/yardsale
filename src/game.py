import itertools
import math
import random

import pygame
from pygame import Vector2

from person import Person

screen_size = 750


class PersonView:
    def __init__(self, person, x, y):
        self.person = person
        self.pos = Vector2(x, y)
        v = 1.0 if random.random() > 0.5 else -1.0
        v = v * random.uniform(0.8, 1.2)
        theta = random.uniform(0, 2*math.pi)
        self.vel = 4 * Vector2(v * math.cos(theta), v * math.sin(theta))
        self.adjust_radius = 10 / math.sqrt(1000/math.pi)

    @property
    def radius(self):
        return math.sqrt(self.person.wealth / math.pi) * self.adjust_radius

    def colliding(self, aPersonView):
        dist = self.pos.distance_to(aPersonView.pos)
        return dist <= self.radius + aPersonView.radius

    def move(self):
        self.pos += self.vel
        if self.pos.x < self.radius or self.pos.x > screen_size - self.radius:
            self.vel = Vector2(-self.vel.x, self.vel.y)
        if self.pos.y < self.radius or self.pos.y > screen_size - self.radius:
            self.vel = Vector2(self.vel.x, -self.vel.y)

    def draw(self, screen):
        wealth = self.person.wealth
        if wealth < 250:
            color = "red"
        elif wealth < 500:
            color = "yellow"
        else:
            color = "cyan"
        pygame.draw.circle(screen, color, self.pos, max(4, int(self.radius)), 0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Wealth")
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        self.clock = pygame.time.Clock()
        self.people = []
        self.populate()

    def populate(self):
        for i in range(100):
            self.add_person(self.people)

    def add_person(self, person_views):
        safe = False
        margin = 20
        person = Person()
        while not safe:
            safe = True
            x = random.uniform(0 + margin, screen_size - margin)
            y = random.uniform(0 + margin, screen_size - margin)
            trial = PersonView(person, x, y)
            for view in person_views:
                if view.colliding(trial):
                    safe = False
        person_views.append(trial)


    def main_loop(self):
        running = True
        moving = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                moving = True
            screen = self.screen
            screen.fill("midnightblue")
            if moving:
                self.check_collisions()
                for pv in self.people:
                    pv.move()
            for pv in self.people:
                pv.draw(screen)
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def check_collisions(self):
        pairs = itertools.combinations(self.people, 2)
        for p1, p2 in pairs:
            if p1.colliding(p2) and p1.person.wealth > 100 and p2.person.wealth > 100:
                p1.person.transact(p2.person)
                p1.vel = -p1.vel
                p2.vel = -p2.vel
                p1.move()
                p2.move()
