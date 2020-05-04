from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class Battlefield(Model):
    def __init__(self, army_1, army_2, width, height):
        self.numerical_army_1 = army_1
        self.numerical_army_2 = army_2
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        for i in range(self.numerical_army_1):

            # TODO
            #dodawanie 1


        for j in range(self.numerical_army_2):

            # TODO
            #dodawanie 2

    def step(self):
        self.schedule.step()

class Infantry(Agent):
    def __init__(self,id,model):
        super().__init__(self,id,model)
        self.health = 10
        self.attack = 3

    def move(self):
        #bardzo uproszczone tak tylko żeby na siebie szli

        if(self.pos[1]>1):
            self.model.grid.move_agent(self,(0,self.pos[1]-1))
        else:
            self.model.grid.move_agent(self, (0, self.pos[1] + 1))

    def fight(self):
        oponents = self.model.grid.get_cell_list_contents([self.pos])
        if len(oponents)>1:




