from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import matplotlib.pyplot as plt
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from Data import *


class Battlefield(Model):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.timer = True
        self.running = True
        self.spawn_from_file()

    def spawn_from_file(self):
        for element in mylist:
            if element[2] == 'I':
                a = Infantry(self.current_id, self)
            elif element[2] == 'A':
                a = Archers(self.current_id, self)
            elif element[2] == 'C':
                a = Cavalry(self.current_id, self)
            elif element[2] == 'R':
                a = Rock(self.current_id, self)
            self.next_id()
            a.set_color(element[3])
            self.schedule.add(a)

            if self.grid.is_cell_empty((element[0], element[1])):
                self.grid.place_agent(a, (element[0], element[1]))
            else:
                print("Unable to place unit on that cell")

    def step(self):
        self.schedule.step()
        if self.timer:
            self.timer = False
        else:
            self.timer = True


class MainAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.pos = None
        self.health = 100
        self.attack = 10
        self.model = model
        self.color = "red"
        self.type = 'I'
        self.help_grid = []
        self.Grid = Grid(matrix=self.help_grid)

    def update_path(self, enemy):
        self.help_grid.clear()
        temp = []
        for i in range(self.model.height):
            temp.clear()
            for j in range(self.model.width):
                if self.model.grid.is_cell_empty((j, i)) or self.pos == (j, i) or enemy.pos == (j, i):
                    temp.append(1)
                else:
                    temp.append(0)
            self.help_grid.append(temp[:])
        self.Grid = Grid(matrix=self.help_grid)

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
        opponents = []
        for a in field:
            if a.get_color() == self.get_color() or a.get_color() == 'black':
                pass
            else:
                opponents.append(a)
        return opponents

    def nearest_fields(self, n):
        fields_around = self.model.grid.get_neighborhood(
            self.pos,
            True,
            False,
            n
        )
        return fields_around

    def move(self):

        others = self.scout(9)

        if len(others) < 1:
            self.model.grid.move_agent(
                self,
                self.random.choice(
                    self.nearest_fields(1)
                ))
        else:
            nemesis = self.random.choice(others)
            self.update_path(nemesis)
            """        
            new_pos = [0,0]
            if others[0].pos[0] > self.pos[0]:
                new_pos[0] = self.pos[0] + 1
            elif others[0].pos[0] < self.pos[0]:
                new_pos[0] = self.pos[0] - 1
            else:
                new_pos[0] = self.pos[0]

            if others[0].pos[1] > self.pos[1]:
                new_pos[1] = self.pos[1] + 1
            elif others[0].pos[1] < self.pos[1]:
                new_pos[1] = self.pos[1] - 1
            else:
                new_pos[1] = self.pos[1]

            new_pos_tup = (new_pos[0], new_pos[1])
            if self.model.grid.is_cell_empty(new_pos_tup):
                self.model.grid.move_agent(self, new_pos_tup)
            else:
                pass"""
            start = self.Grid.node(self.pos[0], self.pos[1])
            end = self.Grid.node(nemesis.pos[0], nemesis.pos[1])

            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
            path, runs = finder.find_path(start, end, self.Grid)
            #print(self.Grid.grid_str(path=path, start=start, end=end))
            #print(path)

            if len(path) > 0:
                if self.model.grid.is_cell_empty((path[1][0], path[1][1])):
                    self.model.grid.move_agent(self, (path[1][0], path[1][1]))
            else:
                print("im stuck")
            self.Grid.cleanup()

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

        if len(neighbors) < 1 & self.model.timer:
            self.move()
        else:
            self.attack_opponent()

    def check_dead(self):
        if self.get_hp() <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Infantry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'I'

    # Na nich się bazowałem robiąc główną klasę więc nie ma co na razie zmieniać XD


class Cavalry(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'C'

    def step(self):
        neighbors = self.scout(1)

        if len(neighbors) < 1:
            self.move()
        else:
            self.attack_opponent()


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

        if len(neighbors) < 1 & self.model.timer:
            self.move()
        else:
            self.attack_opponent()


class Rock(MainAgent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.color = 'black'
        self.type = 'R'

    def step(self):
        pass