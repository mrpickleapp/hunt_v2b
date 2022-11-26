import pygame
import sys
import numpy as np
import random
import copy

import constants
import calc
import agent

import random

def main(**kwargs):

    print()
    for k, v in kwargs.items():
        print('Arg: {} = {}'.format(k, v))
    print()

    window_title = kwargs.get("window_title")
    if window_title == None:
        window_title = "Evolution"

    pygame.init()
    logo = pygame.image.load("logo_32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption(window_title)

    # create a surface on screen
    constants.screen = pygame.display.set_mode((constants.SCREEN_X, constants.SCREEN_Y))
    fontSize = 20
    font = pygame.font.Font('freesansbold.ttf', fontSize)

    # clock
    clock = pygame.time.Clock()
    TICK = 60
    gameTick = 0

    # recording
    rec = kwargs.get('record')

    if kwargs.get('evo_rate') != None:
        constants.evolutionRate = kwargs.get('evo_rate')

    # Create a screen recorder object
    if rec:
        fname = kwargs.get('fname')
        if fname != None:
            fname = 'Output Video/' + fname + '.mp4'
        else:
            fname = 'Output Video/output.mp4'
        
        import record
        recorder = record.ScreenRecorder(constants.SCREEN_X, constants.SCREEN_Y, TICK, fname)
     
    # define a variable to control the main loop
    running = True

    # actors
    preyNumber = 150
    constants.prey = []
    hunterNumber = 75
    constants.hunters = []


    def randomCoords():
        return [random.randint(10, constants.SCREEN_X-10), random.randint(10, constants.SCREEN_Y-10)]

    def randomAngle():
        return random.random() * 6 - 3


    for i in range(preyNumber):
        p = agent.Herbivore(
            id=0,
            location=randomCoords(),
            angle=randomAngle(),
            colour="chartreuse4"
        )
        constants.prey.append(p)

    for i in range(hunterNumber):
        h = agent.Hunter(
            id=0,
            location=randomCoords(),
            angle=randomAngle(),
            colour="blue"
        )
        constants.hunters.append(h)

    
    while running:

        clock.tick(TICK)
        gameTick += 1

        if gameTick%60==0:
            print(gameTick/60, "seconds")

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # TOGGLE EYES
                if event.key == 46:
                    constants.renderEyes = not(constants.renderEyes)

            # QUIT
            if event.type == pygame.QUIT:
                running = False


        # RENDERING
        constants.screen.fill("white")


        # UPDATE HUNTERS - keep living
        livingHunters = []
        for h in constants.hunters:

            if not(h.isDead()):
                h.tick()
                livingHunters.append(h)
                h.draw()

        constants.hunters = livingHunters

        calc.partAgents(constants.hunters)


        # UPDATE PREY - keep living
        livingPrey = []
        for p in constants.prey:
                
            if not(p.isDead()):
                p.tick()
                livingPrey.append(p)
                p.draw()

        constants.prey = livingPrey

        calc.partAgents(constants.prey)


        # Capture the frame
        if rec:
            recorder.capture_frame(constants.screen)

        if (len(constants.prey) == 0) | (len(constants.hunters) == 0) | (gameTick/60 >= 300):
            running = False

        pygame.display.flip()


    if rec:
        print()
        print("Saving recording...")
        recorder.end_recording()
        print("Recording Saved")
        print()

    return 0

    
if __name__ == "__main__":
    main(
        **dict(
            arg.split('=') for arg in sys.argv[1:]
        )
    )