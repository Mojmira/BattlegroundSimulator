from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import numpy as np
import matplotlib.pyplot as plt


class Battlefield(Model):
    def __init__(self, army_1, width, height):
        super().__init__()
        self.numerical_army_1 = army_1
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        i = 0
        for i in range(self.numerical_army_1):
            a = Infantry(i, self)
            self.schedule.add(a)

            x = self.random.randint(0, width - 1)
            y = self.random.randint(0, height - 1)
            if i % 2:
                a.color = "blue"

            self.grid.place_agent(a, (x, y))

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

    # Na nich się bazowałem robiąc główną klasę więc nie ma co na razie zmieniać XD


class Cavalry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)

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
