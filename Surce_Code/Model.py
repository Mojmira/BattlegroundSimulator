from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from FileManagement import *
import random
from FileManagement import *
import os


"""
Funkcje dla data collectora
"""

def compute_cost_red(model):
    model.survived_steps_red += model.count_units('#ff0000')
    print(model.survived_steps_red)
    return model.survived_steps_red / model.starting_cost_red


def compute_cost_blue(model):
    model.survived_steps_blue += model.count_units('#00aab2')
    return model.survived_steps_blue / model.starting_cost_blue

def compute_health_red(model):
    army_health = 0
    for agent in model.schedule.agents:
        if agent.get_color() == '#ff0000':
            army_health += agent.get_hp()

    return army_health


def compute_health_blue(model):
    army_health = 0
    for agent in model.schedule.agents:
        if agent.get_color() == '#00aab2':
            army_health += agent.get_hp()

    return army_health

"""
Model.py
================================
Tutaj znajduje się cały model 
"""


class Battlefield(Model):
    """
    Główna klasa modelu w której wszystko sie dzieje

    Arg:
    width (int): szerokość planszy
    height (int): wysokość planszy
    """

    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.survived_steps_blue = 0
        self.survived_steps_red = 0
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.spawn_from_file()
        self.initial_red_count = self.count_units("#ff0000")
        self.initial_blue_count = self.count_units("#00aab2")
        self.tmp = self.count_cost()
        self.starting_cost_blue = self.tmp[1][0]
        self.starting_cost_red = self.tmp[0][0]

        self.datacollector = DataCollector(
            model_reporters={"Suma przeżytych rund każdej jednostki do kosztu całej armii - czerwoni": compute_cost_red,
                             "Suma przeżytych rund każdej jednostki do kosztu całej armii - niebiescy": compute_cost_blue})

        self.datacollector_health = DataCollector(
            model_reporters={"Punkty życia armii czerwonej": compute_health_red,
                             "Punkty życia armii niebieskiej": compute_health_blue})

    def spawn_from_file(self):
        units = read_from_file('Data/army.txt')
        """
        Wkłada jednostki z listy na planszę
        :return:
        """

        for element in units:
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
            a.timer = random.choice([True, False])
            self.schedule.add(a)

            if self.grid.is_cell_empty((element[0], element[1])):
                self.grid.place_agent(a, (element[0], element[1]))
            else:
                print("Unable to place unit on that cell")

    def step(self):
        """
        Uruchamia losowo wszystkich agentów
        :return:
        """
        self.schedule.step()
        self.is_simulation_over()
        self.datacollector.collect(self)
        self.datacollector_health.collect(self)

    def count_cost(self):
        """
        Funkcja do liczenia kosztów armii
        :return: zwraca tablice krotek (koszt,kolor)
        """
        costs = []
        temp = [0, '#ff0000', 0, '#00aab2']
        for a in self.schedule.agents:
            if a.color == "#ff0000":
                temp[0] += a.cost
            elif a.color == "#00aab2":
                temp[2] += a.cost
        costs.append((temp[0], temp[1]))
        costs.append((temp[2], temp[3]))
        return costs

    def count_units(self, color):
        """
        Zlicza ilość jednostek danego koloru
        :param color: Kolor jednostek jakie ma liczyć
        :return: zwraca ilość jednostek
        """
        counter = 0
        for a in self.schedule.agents:
            if a.color == color:
                counter += 1
        return counter

    def is_simulation_over(self):
        """
        Sprawdza czy symulacja sie zakończyła
        :return:
        """
        temp = self.count_cost()
        if temp[0][0] == 0 or temp[1][0] == 0:
            self.running = False
            to_file(self.write_results(), "Data/results" + str(self.width) + "x" + str(self.height) + ".txt")

    def write_results(self):
        string = ""
        if self.who_won() == 1:
            string += "Blue won with "
            string += str(self.count_units("#00aab2"))
            string += " units left."
            string += "  Starting with || Blue units "
            string += str(self.initial_blue_count)
            string += " - "
            string += str(self.initial_red_count)
            string += " Red units\n"
        else:
            string += "Red won with "
            string += str(self.count_units("#ff0000"))
            string += " units left"
            string += "  Starting with || Blue units "
            string += str(self.initial_blue_count)
            string += " - "
            string += str(self.initial_red_count)
            string += " Red units\n"
        return string

    def who_won(self):
        """
        Sprawdza kto wygrał
        :return: zwraca 1 kiedy wygrali niebiescy i 0 jak wygralki czerwoni
        """
        temp = self.count_cost()
        if temp[0][0] > 0:
            return 0
        else:
            return 1


class MainAgent(Agent):
    """
    Klasa główna z której dziedziczą potem poszczególne typy jednostek

    Arg:
    id (int): unikalny id agenta
    model : model w którym agent będzie działać
    """

    def __init__(self, id, model):
        super().__init__(id, model)
        self.pos = None
        self.health = 100
        self.attack = 10
        self.defence = 0.25
        self.cost = 0
        self.model = model
        self.color = "red"
        self.type = 'I'
        self.timer = True
        self.help_grid = []
        self.Grid = Grid(matrix=self.help_grid)

    def update_path(self, enemy):

        """
        Aktualizuje plansze przeszkód widzianych przez agenta
        :param enemy: Agent który ma być widziany nie jako przeszkoda
        :return:
        """

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

        """
        Getter pozycji
        :return: zwraca pozycję
        """

        return self.pos

    def get_cost(self):
        """
        Getter kosztu
        :return: zwraca koszt
        """
        return self.cost

    def get_dmg(self):

        """
        Getter obrażeń
        :return: zwraca atak jednostki
        """

        return self.attack

    def get_hp(self):

        """
        getter życia
        :return: zwraca aktualne życie agenta
        """

        return self.health

    def get_color(self):

        """
        getter koloru
        :return: zwraca kolor agenta
        """

        return self.color

    def set_hp(self, hp):

        """
        ustawia życie agenta
        :param hp: nowe życie agenta
        :return:
        """

        self.health = hp

    def set_color(self, color):

        """
        ustawia kolor agenta
        :param color: nowy kolor agenta
        :return:
        """

        self.color = color

    def scout(self, n):

        """
        Szuka w zasiegu (n) przeciwników
        :param n: zasięg
        :return: zwraca listę przeciwników
        """

        field = self.model.grid.get_neighbors(
            self.pos,  # Pozycja jednostki
            True,  # True=Moore neighborhood False=Von Neumann neighborhood
            False,  # Srodek
            n  # Promien
        )
        opponents = []
        for a in field:
            if a.get_color() == self.get_color() or a.get_color() == '#000000':
                pass
            else:
                opponents.append(a)
        return opponents

    def nearest_fields(self, n):
        """
        sprawdza pola na które agent może przejść w zasięgu
        :param n: zasięg
        :return: zwraca listę krotek
        """
        fields_around = self.model.grid.get_neighborhood(
            self.pos,
            True,
            False,
            n
        )
        return fields_around

    # def advanced_scout(self,pos):

    def move(self):

        """
        Metoda poruszająca agenta
        Kiedy nikogo nie widzi porusza się losowo
        Jak widzi to idzie w jego stronę najszybszą ścieżką
        :return:
        """

        others = self.scout(18)

        if len(others) < 1:
            self.model.grid.move_agent(
                self,
                self.random.choice(
                    self.nearest_fields(1)
                ))
        else:
            nemesis = self.random.choice(others)
            self.update_path(nemesis)

            start = self.Grid.node(self.pos[0], self.pos[1])
            end = self.Grid.node(nemesis.pos[0], nemesis.pos[1])

            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
            path, runs = finder.find_path(start, end, self.Grid)

            if len(path) > 0:
                if self.model.grid.is_cell_empty((path[1][0], path[1][1])):
                    self.model.grid.move_agent(self, (path[1][0], path[1][1]))
            else:
                print("im stuck")
            self.Grid.cleanup()

    def attack_opponent(self):

        """
        Szuka w swojej okolicy przeciwników i atakuje ich
        :return:
        """

        opponents = self.scout(1)

        if len(opponents) > 0:
            other = self.random.choice(opponents)
            other.hurt_me(self.get_dmg())

    def hurt_me(self, dmg):

        """
        Zadaje obrażenia agentowi
        :param dmg: ilośc obrażeń
        :return:
        """
        hit = random.randint(1, 100) / 100
        if hit > self.defence:
            hp = self.get_hp()
            hp -= dmg
            self.set_hp(hp)
            self.check_dead()

    def step(self):

        """
        Co ma robić podczas wywołania przez scheduler modelu
        :return:
        """

        neighbors = self.scout(1)

        if len(neighbors) < 1 & self.timer:
            self.move()
            self.timer = not self.timer
        else:
            self.attack_opponent()
            self.timer = not self.timer

    def check_dead(self):

        """
        Sprawdza czy agent jest martwy,
        Jak jest to usuwa go z modelu
        :return:
        """

        if self.get_hp() <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Infantry(MainAgent):
    """
    Klasa dizedzicząca po głównym agencie

    Arg:
    id (int): unikalny id agenta
    model : model w którym agent będzie działać
    """

    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'I'
        self.health = 120
        self.attack = 10
        self.defence = 0.25
        self.cost = 40

    # Na nich się bazowałem robiąc główną klasę więc nie ma co na razie zmieniać XD


class Cavalry(MainAgent):
    """
    Klasa dizedzicząca po głównym agencie

    Arg:
    id (int): unikalny id agenta
    model : model w którym agent będzie działać
    """

    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'C'
        self.health = 200
        self.attack = 20
        self.defence = 0.40
        self.cost = 120

    def step(self):
        """
        Do zwykłego stepa różni sie tym że wykonuje akcję co wywołanie a nie jak standardowy co 2
        :return:
        """
        neighbors = self.scout(1)
        if len(neighbors) < 1:
            self.move()
        else:
            self.attack_opponent()


class Archers(MainAgent):
    """
    Klasa dizedzicząca po głównym agencie

    Arg:
    id (int): unikalny id agenta
    model : model w którym agent będzie działać
    """

    def __init__(self, id, model):
        super().__init__(id, model)
        self.type = 'A'
        self.health = 70
        self.attack = 30
        self.defence = 0.15
        self.cost = 60

    def attack_opponent(self):

        """
        Różni się tylko tym że ma większy zasięg sprawdzania przeciwników
        :return:
        """

        opponents = self.scout(2)
        if len(opponents) > 0:
            other = self.random.choice(opponents)
            other.hurt_me(self.get_dmg())

    def step(self):

        """
        Różni się tylko tym że ma większy zasięg sprawdzania przeciwników
        :return:
        """

        neighbors = self.scout(2)

        if len(neighbors) < 1 & self.timer:
            self.move()
            self.timer = not self.timer
        else:
            self.attack_opponent()
            self.timer = not self.timer


class Rock(MainAgent):
    """
    Klasa dizedzicząca po głównym agencie

    Arg:
    id (int): unikalny id agenta
    model : model w którym agent będzie działać
    """

    def __init__(self, id, model):
        super().__init__(id, model)
        self.color = 'black'
        self.type = 'R'

    def step(self):
        """
        Skała,
        Nic
        Nie
        Robi
        :return:
        """

        pass


def run_n_sim(n, width, height):
    """
    Funkcja do przeprowadzania dużej ilości symulacji bez potrzeby oglądania ich
    :param n: Ilość symulacji
    :return:
    """
    wins = [[], []]
    for i in range(n):
        model = Battlefield(width, height)
        while model.running:
            model.step()
        if model.who_won() == 0:
            wins[0].append(0)
        else:
            wins[1].append(2)

    bars = ("red", "blue")
    y_pos = np.arange(0.5, len(bars))

    plt.hist(wins, bins=[0, 2], histtype='bar', align='mid', orientation='vertical', label="WINS",
             color=["#ff0000", "#00aab2"])
    plt.xticks(y_pos, bars)

    plt.show()
