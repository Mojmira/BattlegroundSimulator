from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Model import Battlefield


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": agent.color,
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5,
                 "text": agent.get_hp(),
                 "text_color": "black"}


    return portrayal


grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(Battlefield,
                       [grid],
                       "Draw Model",
                       {"army_1": [2, 2, 2], "army_2": [2, 2, 2], "width": 20, "height": 20})
server.port = 8521  # The default
server.launch()
