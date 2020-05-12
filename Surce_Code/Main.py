from Model import *
from Data import *
from ArmyCreation import *
import time

if __name__ == '__main__':
    #in_line(0, 19, 0, "blue", "I")
    #in_line(0, 19, 19, "red", "I")
    battle = Battlefield([2, 2, 2], [2, 2, 2], 20, 20)

    #clear_file()


    for i in range(100):
        battle.step()

    for agent in battle.schedule.agents:
        print(agent.get_color())
        print(agent.type)

    agent_counts = np.zeros((battle.grid.width, battle.grid.height))
    for cell in battle.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
    plt.imshow(agent_counts, interpolation='nearest')
    plt.colorbar()
    plt.show()

