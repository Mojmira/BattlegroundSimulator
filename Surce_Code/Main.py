from Model import *
from Data import *

if __name__ == '__main__':
    #print(army_list)


    battle = Battlefield([2, 2, 2], [2, 2, 2], 20, 20)

    battle.spawn_from_file()
    '''
    for i in range(1):
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
    print(primes(100))
    '''