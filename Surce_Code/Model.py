from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import numpy as np
import matplotlib.pyplot as plt


def primes(n):  # simple Sieve of Eratosthenes
    odds = range(3, n + 1, 2)
    sieve = set(sum([list(range(q * q, n + 1, q + q)) for q in odds], []))
    return [2] + [p for p in odds if p not in sieve]


class Battlefield(Model):
    def __init__(self, army_1, army_2, width, height):
        super().__init__()
        self.primes = primes(100)
        self.width = width
        self.height = height
        self.army_1 = army_1
        self.army_2 = army_2
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.spawn(army_1, "red", 1)
        self.spawn(army_2, "blue", 4)

    def spawn(self, army, color, prime):
        for i in range(len(army)):
            if i == 0:
                for j in range(army[i]):
                    a = Infantry(self.primes[1*prime] * (j+1), self)
                    self.add_at_random(a, color)
            elif i == 1:
                for k in range(army[i]):
                    a = Archers(self.primes[2*prime] * (k+1), self)
                    self.add_at_random(a, color)
            elif i == 2:
                for l in range(army[i]):
                    a = Cavalry(self.primes[3*prime] * (l+1), self)
                    self.add_at_random(a, color)

    def add_at_random(self, agent, color):
        self.schedule.add(agent)
        agent.set_color(color)
        # Na razie randomowe ale zmienimy potem na dokładniejsze
        # TODO
        x = self.random.randint(0, self.width - 1)
        y = self.random.randint(0, self.height - 1)

        self.grid.place_agent(agent, (x, y))

    def step(self):
        self.schedule.step()


class MainAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.pos = None
        self.health = 100
        self.attack = 10
        self.model = model
        self.color = "red"

    def get_pos(self):
        return self.pos

    def get_dmg(self):
        return self.attack

    def get_hp(self):
        return self.health

    def get_color(self):
        return self.color

    def set_hp(self, hp):
        self.health = hp

    def set_color(self, color):
        self.color = color

    def scout(self, n):
        field = self.model.grid.get_neighbors(
            self.pos,  # Pozycja jednostki
            True,  # True=Moore neighborhood False=Von Neumann neighborhood
            False,  # Srodek
            n  # Promien
        )

        for a in field:
            if a.get_color() == self.get_color():
                field.remove(a)

        return field

    def nearest_fields(self, n):
        fields_around = self.model.grid.get_neighborhood(
            self.pos,
            True,
            False,
            n
        )
        return fields_around

    def move(self):

        others = self.scout(7)

        if len(others) < 1:
            self.model.grid.move_agent(
                self,
                self.random.choice(
                    self.nearest_fields(1)
                ))
        else:
            new_pos = [0, 0]

            if others[0].pos[0] > self.pos[0]:
                new_pos[0] = self.pos[0] + 1
            elif others[0].pos[0] < self.pos[0]:
                new_pos[0] = self.pos[0] - 1
            else:
                pass

            if others[0].pos[1] > self.pos[1]:
                new_pos[1] = self.pos[1] + 1
            elif others[0].pos[1] < self.pos[1]:
                new_pos[1] = self.pos[1] - 1
            else:
                pass

            new_pos_tup = (new_pos[0], new_pos[1])
            if self.model.grid.is_cell_empty(new_pos_tup):
                self.model.grid.move_agent(self, new_pos_tup)
            else:
                pass

    def attack_opponent(self):
        opponents = self.scout(1)

        if len(opponents) > 0:
            other = self.random.choice(opponents)
            other.hurt_me(self.get_dmg())

    def hurt_me(self, dmg):
        hp = self.get_hp()
        hp -= dmg
        self.set_hp(hp)
        self.check_dead()

    def step(self):
        neighbors = self.scout(1)
        if len(neighbors) < 1:
            self.move()
        self.attack_opponent()

    def check_dead(self):
        for a in self.model.schedule.agents:
            if a.get_hp() <= 0:
                print('RIP')
                self.model.grid.remove_agent(a)
                self.model.schedule.remove(a)


class Infantry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'I'

    # Na nich się bazowałem robiąc główną klasę więc nie ma co na razie zmieniać XD


class Cavalry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'C'

    def move(self):
        possible_fields = self.nearest_fields(2)
        others = self.scout(7)

        if len(others) < 1:

            self.model.grid.move_agent(
                self,
                self.random.choice(
                    possible_fields
                ))
        else:
            new_pos = [0, 0]

            if others[0].pos[0] > self.pos[0]:
                new_pos[0] = self.pos[0] + 2
            elif others[0].pos[0] < self.pos[0]:
                new_pos[0] = self.pos[0] - 2
            else:
                pass

            if others[0].pos[1] > self.pos[1]:
                new_pos[1] = self.pos[1] + 2
            elif others[0].pos[1] < self.pos[1]:
                new_pos[1] = self.pos[1] - 2
            else:
                pass

            new_pos_tup = (new_pos[0], new_pos[1])
            if self.model.grid.is_cell_empty(new_pos_tup):
                self.model.grid.move_agent(self, new_pos_tup)
            else:
                pass


class Archers(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'A'

    def attack_opponent(self):
        opponents = self.scout(2)
        if len(opponents) > 0:
            other = self.random.choice(opponents)
            other.hurt_me(self.get_dmg())

    def step(self):
        neighbors = self.scout(2)
        if len(neighbors) < 1:
            self.move()
        self.attack_opponent()
