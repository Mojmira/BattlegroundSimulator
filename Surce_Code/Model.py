from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import matplotlib.pyplot as plt
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from Data import *

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
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.timer = True
        self.running = True
        self.spawn_from_file()

    def spawn_from_file(self):

        """
        Wkłada jednostki z listy na planszę
        :return:
        """

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
        """
        Uruchamia losowo wszystkich agentów
        :return:
        """
        self.schedule.step()
        if self.timer:
            self.timer = False
        else:
            self.timer = True


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
        self.model = model
        self.color = "red"
        self.type = 'I'
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
            if a.get_color() == self.get_color() or a.get_color() == 'black':
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

    def move(self):

        """
        Metoda poruszająca agenta
        Kiedy nikogo nie widzi porusza się losowo
        Jak widzi to idzie w jego stronę najszybszą ścieżką
        :return:
        """


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

        if len(neighbors) < 1 & self.model.timer:
            self.move()
        else:
            self.attack_opponent()

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

        if len(neighbors) < 1 & self.model.timer:
            self.move()
        else:
            self.attack_opponent()


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
