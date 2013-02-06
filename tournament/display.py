#!/bin/env python

import glob, os
import random, time
import shutil
import stat

def showGame(game):
    os.system("python Visualizer\main.py " + game)


while 1:
    games = glob.glob("*.gamelog")
    if not games:
        time.sleep(30)
        continue
    game = random.choice(games)
    
    showGame(game)
    shutil.move(game, "played/" + game)
    time.sleep(45)
    
    try:
        print os.stat(game)[stat.ST_SIZE]
        if os.stat(game)[stat.ST_SIZE] > 1000:
            showGame(game)
            shutil.move(game, "played/" + game)
    except:
        pass
    time.sleep(30)
