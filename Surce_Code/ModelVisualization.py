from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

import Model
from Model import Battlefield


def agent_portrayal(agent):
    if agent.type == 'I':
        portrayal = {"Shape": "infantry_red.png",
                     "Layer": 0}
        if agent.color == "#00aab2":
            portrayal["Shape"] = "infantry_blue.png"
    elif agent.type == 'C':
        portrayal = {"Shape": "cavalry_red.png",
                     "Layer": 0}
        if agent.color == "#00aab2":
            portrayal["Shape"] = "cavalry_blue.png"
    elif agent.type == 'A':
        portrayal = {"Shape": "archer_red.png",
                     "Layer": 0}
        if agent.color == "#00aab2":
            portrayal["Shape"] = "archer_blue.png"
    elif agent.type == 'R':
        portrayal = {"Shape": "obstacle.png",
                     "Layer": 0}

    return portrayal


def StartSimulation(fieldSize):
    grid = CanvasGrid(agent_portrayal, fieldSize, fieldSize, 500, 500)

    chart = ChartModule([{"Label": "Suma przeżytych rund każdej jednostki do kosztu całej armii - czerwoni", "Color": "Red"},
                         {"Label": "Suma przeżytych rund każdej jednostki do kosztu całej armii - niebiescy", "Color": "Blue"}],
                        data_collector_name='datacollector')
    chart_hp = ChartModule([{"Label": "Punkty życia armii czerwonej", "Color": "Red"},
                            {"Label": "Punkty życia armii niebieskiej", "Color": "Blue"}],
                           data_collector_name='datacollector_health')

    server = ModularServer(Battlefield,
                           [grid, chart, chart_hp],
                           "Draw Model",
                           {"width": fieldSize, "height": fieldSize})
    server.port = 8521  # The default
    server.launch()
