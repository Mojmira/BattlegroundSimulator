from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class Battlefield(Model):
    def __init__(self, army_1, army_2, width, height):
        super().__init__()
        self.numerical_army_1 = army_1
        self.numerical_army_2 = army_2
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        for i in range(self.numerical_army_1):
            a = Infantry(i, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (0, 0))

        for j in range(self.numerical_army_2):
            a = Infantry(10, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (0, 3))

    def step(self):
        self.schedule.step()


class MainAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.health = 0
        self.attack = 0

    def move(self):
        # bardzo uproszczone tak tylko żeby na siebie szli

        if self.pos[1] > 1:
            self.model.grid.move_agent(self, (0, self.pos[1] - 1))
        else:
            self.model.grid.move_agent(self, (0, self.pos[1] + 1))

    def fight(self):
        oponents = self.model.grid.get_cell_list_contents([self.pos])
        if len(oponents) > 1:

            #bije siebie też XDDD
            other = self.random.choice(oponents)
            other.health = other.health - self.attack
            self.health = self.health - other.attack

    def step(self):
        if self.pos[1] != 1:
            self.move()
        else:
            self.fight()


class Infantry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)

    def step(self):
        if self.pos[1] != 1:
            self.move()
        else:
            self.fight()
