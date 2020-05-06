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
            if i%2:
                a.color="blue"

            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()


class MainAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.health = 0
        self.attack = 0
        self.model = model
        self.color = "red"

    def scout(self):
        field = self.model.grid.get_neighbors(
            self.pos,  # Pozycja jednostki
            True,  # True=Moore neighborhood False=Von Neumann neighborhood
            False,  # Srodek
            7  # Promien
        )
        return field

    def nearest9fields(self):
        fields_around = self.model.grid.get_neighborhood(
            self.pos,
            True,
            True,
            1
        )
        return fields_around

    def move(self):

        others = self.scout()

        if len(others) < 1:
            print("I'm mooving hehe")

            self.model.grid.move_agent(
                self,
                self.random.choice(
                    self.nearest9fields()
                ))
        else:
            print("I'm in touch with somebody ")
            new_pos = [0, 0]

            if others[0].pos[0]>self.pos[0]:
                new_pos[0] = self.pos[0]+1
            elif others[0].pos[0]<self.pos[0]:
                new_pos[0] = self.pos[0] - 1
            else:
                pass

            if others[0].pos[1]>self.pos[1]:
                new_pos[1] = self.pos[1] + 1
            elif others[0].pos[1]<self.pos[1]:
                new_pos[1] = self.pos[1] - 1
            else:
                pass

            new_pos_tup = (new_pos[0], new_pos[1])
            self.model.grid.move_agent(self, new_pos_tup)

    def fight(self):
        opponents = self.model.grid.get_neighbors(
            self.pos,
            True,
            False,
            1
        )
        if len(opponents) > 0:
            print("F")
            other = self.random.choice(opponents)
            other.health = other.health - self.attack
            self.health = self.health - other.attack

    def step(self):
        self.move()
        self.fight()


class Infantry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)


