from Model import *

if (__name__ == '__main__'):

    battle = Battlefield(1,1,1,5)
    for i in range(3):
        battle.step()
    for agent in battle.schedule.agents:
        print(agent.health)
