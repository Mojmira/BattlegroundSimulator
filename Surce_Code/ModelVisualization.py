from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Model import Battlefield


def agent_portrayal(agent):
    if agent.type == 'I':
        portrayal = {"Shape": "infantry_red.png",
                     "Layer": 0,
                     "text": agent.get_hp(),
                     "text_color": "white"}
        if agent.color == "#00aab2":
            portrayal["Shape"] = "infantry_blue.png"
    elif agent.type == 'C':
        portrayal = {"Shape": "cavalry_red.png",
                     "Layer": 0,
                     "text": agent.get_hp(),
                     "text_color": "white"}
        if agent.color == "#00aab2":
            portrayal["Shape"] = "cavalry_blue.png"
    elif agent.type == 'A':
        portrayal = {"Shape": "archer_red.png",
                     "Layer": 0,
                     "text": agent.get_hp(),
                     "text_color": "white"}
        if agent.color == "#00aab2":
            portrayal["Shape"] = "archer_blue.png"
    elif agent.type == 'R':
        portrayal = {"Shape": "rect",
                     "Color": agent.color,
                     "Filled": "true",
                     "Layer": 0,
                     "w": 0.5,
                     "h": 0.5}

    return portrayal


def StartSimulation(fieldSize):
    grid = CanvasGrid(agent_portrayal, fieldSize, fieldSize, 500, 500)
    server = ModularServer(Battlefield,
                           [grid],
                           "Draw Model",
                           {"width": fieldSize, "height": fieldSize})
    server.port = 8521  # The default
    server.launch()
