import itertools
import math
import random

import pygame
from pygame import Vector2

from person import Person

screen_size = 750
stats_space = 100


class PersonView:
    def __init__(self, person, x, y):
        self.vel = None
        self.person = person
        self.pos = Vector2(x, y)
        self.set_random_velocity()
        self.adjust_radius = 10 / math.sqrt(1000/math.pi)

    def set_random_velocity(self):
        v = random.uniform(0.8, 1.2)
        theta = random.uniform(0, 2 * math.pi)
        self.vel = 4 * Vector2(v * math.cos(theta), v * math.sin(theta))

    @property
    def radius(self):
        return math.sqrt(self.person.wealth / math.pi) * self.adjust_radius

    def colliding(self, aPersonView):
        dist = self.pos.distance_to(aPersonView.pos)
        return dist <= self.radius + aPersonView.radius

    def move(self):
        if random.random() < 0.005:
            self.set_random_velocity()
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
        self.screen = pygame.display.set_mode((screen_size, screen_size + stats_space))
        self.clock = pygame.time.Clock()
        self.people = []
        self.populate()
        if pygame.get_init():
            self.score_font = pygame.font.SysFont("arial", 32)
            self.axis_font = pygame.font.SysFont("arial", 15)

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
            self.statistics(self.people, screen)
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    def statistics(self, views, screen):
        pygame.draw.line(screen, "green", (0, screen_size), (screen_size - 55, screen_size))
        wealths = sorted([view.person.wealth for view in views])
        poorest, richest = self.get_loser_and_winner(views, wealths)
        self.display_loser_and_winner(poorest, richest, screen)
        self.draw_histogram(richest, wealths, screen)

    def draw_histogram(self, richest, wealths, screen):
        self.draw_bars(wealths, richest, screen)
        scale_text = f'{scale_max(richest)}'
        scale_surface = self.axis_font.render(scale_text, True, "green")
        screen.blit(scale_surface, (700, screen_size - 8))

    def draw_bars(self, wealths, richest, screen):
        scale = stats_space / scale_max(richest)
        min_height = 2
        for wealth, x_pos in zip(wealths, itertools.count(7, 7)):
            self.draw_one_bar(wealth, x_pos, scale, min_height, screen)

    def draw_one_bar(self, wealth, x_pos, scale, min_height, screen):
        height_of_bar = max(wealth * scale, min_height)
        bottom_of_graph = screen_size + stats_space
        top_of_bar = bottom_of_graph - height_of_bar
        pygame.draw.rect(screen, "white", (x_pos, top_of_bar, 5, height_of_bar))

    def get_loser_and_winner(self, views, wealths):
        richest = wealths[-1]
        poorest = wealths[0]
        for v in views:
            w = v.person.wealth
            richest = max(richest, w)
            poorest = min(poorest, w)
        return poorest, richest

    def display_loser_and_winner(self, poorest, richest, screen):
        text = f'Min: {poorest:.0f} Max: {richest:.0f} ({richest / 1000:.0f}%)'
        score_surface = self.score_font.render(text, True, "green")
        screen.blit(score_surface, (20, screen_size))

    def check_collisions(self):
        pairs = itertools.combinations(self.people, 2)
        for p1, p2 in pairs:
            if p1.colliding(p2): # and p1.person.wealth > 100 and p2.person.wealth > 100:
                p1.person.transact(p2.person)
                p1.vel = -p1.vel
                p2.vel = -p2.vel
                p1.move()
                p2.move()


def scale_max(value):
    table = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]
    for limit in table:
        if value < limit:
            return limit
    return 100000
