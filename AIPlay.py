#%%
import numpy as np
import time
from game import ConsoleGame
#%%
class stepPlay:
    def __init__(self, probs):
        self.probs = probs
        self.x, self.y = probs
        nextProbs = self.nextProbs()
        if nextProbs != None:
            self.next = stepPlay(nextProbs)
        else:
            self.next = None

    def nextProbs(self):
        x,y = self.probs
        if x<7:
            x = x + 1
            nProbs = (x,y)
        elif y<7:
            x = 0
            y = y + 1
            nProbs = (x,y)
        else:
            nProbs = None
        return nProbs
        
#%%
def AIcontrol(step, game, countP, countL):
    if game.getMap() is not game.getAnswerMap():
        nextStep = step.next
        result = game.paint(nextStep.x,nextStep.y)
        print(f'paint at {nextStep.probs}\tresult: {result}')
        game.render()
        time.sleep(0.1)
        if nextStep.x == 0:
            countP = 0
            countL = 0
        if nextStep.next == None:
            if game.getMap() is not game.getAnswerMap():
                return True
            else:
                game.resetMap(nextStep.probs)
                return False

        if result:
            if AIcontrol(nextStep,game, countP+1, countL):
                return True
            else:
                game.resetMap(nextStep.probs)
                return False

        else:
            if game.getRow(nextStep.y)==[]:
                if AIcontrol(nextStep,game, countP, countL):
                    return True
                else:
                    return False
            elif countP<game.getRow(nextStep.y)[countL]:
                if countP>0:
                    game.resetMap(nextStep.probs)
                    return False
                else:
                    if AIcontrol(nextStep,game, countP, countL):
                        return True
                    else:
                        game.resetMap(nextStep.probs)
                        return False
            else:
                if countP > 0:
                    if countL < len(game.getRow(step.y))-1:
                        if AIcontrol(nextStep,game, 0, countL+1):
                            return True
                        else:
                            if AIcontrol(nextStep.next,game, 0, countL+1):
                                return True
                            else:
                                game.resetMap(nextStep.probs)
                                return False
                    else:
                        if AIcontrol(nextStep,game, countP, countL):
                            return True
                        else:
                            game.resetMap(nextStep.probs)
                            return False
                return True
    return True




#%%
game = ConsoleGame('Map/B.txt')
game.render()
back = False

probs = (-1,0)
step = stepPlay(probs)
AIcontrol(step, game, 0, 0)

#%%