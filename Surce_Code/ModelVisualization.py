from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from Model import Battlefield

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 200, 200)
server = ModularServer(Battlefield,
                       [grid],
                       "Draw Model",
                       {"army_1": 2, "width": 20, "height": 20})
server.port = 8521  # The default
server.launch()
