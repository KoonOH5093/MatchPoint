#%%
import numpy as np
import time
from game import ConsoleGame
import random
#%%
class stepPlay:
    def __init__(self, probs, preMap = None):
        self.probs = probs
        self.Map = None
        if preMap != None:
            self.preMap = preMap
        else:
            self.preMap = None
        self.nextMap = self.nextMap()

    def nextMap(self):
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
        if nProbs == None:
            return None
        else:
            return stepPlay(nProbs, self)
        
#%%
def AIcontrol(step, game, countP, countL):
    if step is not None:
        result = False
        x,y = step.probs
        if x >= 0 :
            result, step.Map = game.paint(x,y)
            print(f'paint at {step.probs}\tresult: {result} countP: {countP} countL: {countL}')
        game.render()
        #time.sleep(0.1)

        if x == 7:
            if y == 7:
                if result:
                    if countL==len(game.row_counts[y])-1 and countP+1 == game.row_counts[y][countL]:
                        return True
                else:
                    if countL==len(game.row_counts[y])-1 and countP == game.row_counts[y][countL]:
                        return True
            if result:
                if countL<len(game.row_counts[y])-1:
                    game.erase(x,y)
                    return False
                if countP+1<game.row_counts[y][countL]:
                    game.erase(x,y)
                    return False
            else:
                if countP==0 and game.row_counts[y] != []:
                    return False
                if countL<len(game.row_counts[y])-1:
                    return False

        if x == 0:
            countP = 0
            countL = 0

        if result:
            if AIcontrol(step.nextMap,game, countP+1, countL):
                return True
            else:
                game.erase(x,y)
                if step != None:
                    if countP==0 and x<7-countP:
                        if AIcontrol(step.nextMap,game, countP, countL):
                            return True
                        else:
                            game.erase(x,y)
                            return False
                    else:
                        if x > 7-countP:
                            return False
                return False

        else:
            if game.row_counts[y]==[]:
                if AIcontrol(step.nextMap,game, countP, countL):
                    return True
                else:
                    return False
            elif countP<game.row_counts[y][countL]:
                if countP>0:
                    game.erase(x,y)
                    return False
                else:
                    if AIcontrol(step.nextMap,game, countP, countL):
                        return True
                    else:
                        game.erase(x,y)
                        return False
            else:
                if countP > 0:
                    if countL < len(game.row_counts[y])-1:
                        if AIcontrol(step.nextMap,game, 0, countL+1):
                            return True
                        else:
                            game.erase(x,y)
                            return False
                    else:
                        if AIcontrol(step.nextMap,game, countP, countL):
                            return True
                        else:
                            game.erase(x,y)
                            return False
                return True
    return True




#%%
#game_map = [random.choice([' ','O']) for i in range(64)]
game = ConsoleGame('Map/B.txt')
game.render()
back = False

probs = (-1,0)
step = stepPlay(probs)
AIcontrol(step, game, 0, 0)
print(time.process_time())
#print(game_map)
#%%