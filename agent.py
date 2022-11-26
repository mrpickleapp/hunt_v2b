import pygame
import numpy as np
import copy
import random

import constants
import calc
import ai
import vision


class Agent():

    def __init__(self, id, location, angle, health, colour, eyes=[], fovs=[]):
        self.id = id
        self.location = location
        self.angle = angle
        self.speed = 0
        self.health = health
        self.eyes = []
        self.fovs = []
        self.colour = colour
        self.evolution_rate = constants.evolutionRate
        self.dead = False

    def addEyes(self):
        for i, angle in enumerate(self.eyeAngles):
            self.eyes.append(
                vision.Eye(
                    parent=self, angle=angle, length=self.eyeDistances[i]
                )
            )

    def setPersonalSpace(self):
        self.personalSpace = vision.personalSpace(
            parent=self,
            channels=self.personal_space_channels,
            detection_range=self.personal_space_range
        )


    def think(self, targets=[]):

        input = []
        """
        for eye in self.eyes:
            output = eye.detectObstacles(targets)
            input.extend(output)
        """
        input.extend(self.personalSpace.detectEnemies(targets))

        output = self.AI.compute(input)

        self.speed += output[0]
        self.speed = min(self.speed, self.maxSpeed)
        self.speed = max(0, self.speed)

        self.angle += output[1]**2 * (1 if output[2] > 0 else -1)

        velocity = calc.scaleVector(calc.vectorFromAngle(self.angle), self.speed)

        self.move(velocity)


    def move(self, velocity):
        self.location = calc.addVectors(self.location, velocity)
        # self.location = calc.applyBoundaries(self.location)
        self.location = calc.wrapBoundaries(self.location)


    def evolve(self, evolution_rate):
        self.AI.evolve(evolution_rate=evolution_rate)


    def reproduce(self, n, evolution_rate, lst):

        offspring = []

        for i in range(n):
            child = copy.deepcopy(self)

            child.reset()
            
            child.evolve(evolution_rate)
            child.location[0] += random.randint(-5, 5)
            child.location[1] += random.randint(-5, 5)
            child.angle += (random.random() - 0.5) * 5
            offspring.append(child)

        lst.extend(offspring)


    def draw(self):
        screen_x = self.location[0]
        screen_y = calc.flipY(self.location[1])

        pygame.draw.circle(constants.screen, self.colour, [screen_x, screen_y], self.radius)

        if constants.renderEyes:
            """
            for eyeLine in self.eyes:
                eyeLine.draw()
            """
            self.personalSpace.draw()


class Hunter(Agent):

    # dies if it does not eat
    maxHealth = 750
    # speedCoeff = 2
    maxSpeed = 5
    # eyeAngles = [-0.2, -0.06, 0, 0.06, 0.2]
    # eyeDistances = [80, 150, 160, 150, 80,]
    personal_space_channels = 7
    personal_space_range = 150
    radius = 3
    eatHealth = 0
    eatHealthPerEat = 20
    eatCooldownMax = 2

    def __init__(self, id, location, colour, angle=0):
        super().__init__(id=id, location=location, angle=angle, health=self.maxHealth, colour=colour)
        self.setHealth()
        # self.addEyes()
        self.setPersonalSpace()
        self.AI = ai.AI(3)
        self.eatCooldown = self.eatCooldownMax

    def reset(self):
        self.setHealth()
        self.eatCooldown = self.eatCooldownMax

    def setHealth(self):
        self.health = np.random.normal(loc=self.maxHealth, scale=50, size=1)
    
    def tick(self):
        self.think(targets=constants.prey)
        self.checkEat(targets=constants.prey)
        self.health -= 5 + self.speed**2 / 10
        self.eatCooldown -= 1

    def checkEat(self, targets):
        for target in targets:
            distance = calc.pointDistance(self.location, target.location)
            if (distance <= (self.radius + target.radius)) & (self.eatCooldown <= 0):
                # eat has occured
                target.dead = True
                self.eat()
                self.eatCooldown = self.eatCooldownMax

    def eat(self):
        self.setHealth()
        self.eatHealth += self.eatHealthPerEat
        if self.eatHealth >= 100:
            self.eatHealth = 0
            if constants.maxHunters > len(constants.hunters):
                self.reproduce(n=1, evolution_rate=self.evolution_rate, lst=constants.hunters)

    def isDead(self):
        return True if self.health <= 0 else False



class Herbivore(Agent):

    # dies when runs out of health
    # can reproduce in the reproduction zone
    maxHealth = 1000
    maxSpeed = 3.5
    # speedCoeff = 1
    # eyeAngles = [-1.8, -1.5, -1.1, -0.7, 0.7, 1.1, 1.5, 1.8]
    # eyeDistances = [100, 100, 100, 100, 100, 100, 100, 100]
    personal_space_channels = 7
    personal_space_range = 100
    radius = 4
    reproductionCooldownCentre = 100

    def __init__(self, id, location, colour, angle=0):
        super().__init__(id=id, location=location, angle=angle, health=self.maxHealth, colour=colour)
        self.setHealth()
        # self.addEyes()
        self.setPersonalSpace()
        self.AI = ai.AI(3)
        self.setReprodCooldown()

    def reset(self):
        self.setHealth()
        self.setReprodCooldown()

    def setHealth(self):
        self.health = np.random.normal(loc=self.maxHealth, scale=50, size=1)

    def setReprodCooldown(self):
        self.reproductionCooldown = np.random.normal(loc=self.reproductionCooldownCentre, scale=50, size=1)

    def tick(self):

        self.think(targets=constants.hunters)
        self.health -= 1

        # reproduction cooldown
        # if self.speed == 0:
        self.reproductionCooldown -= 1

        if self.reproductionCooldown < 0:
            self.setReprodCooldown()
            if constants.maxPrey > len(constants.prey):
                self.reproduce(n=1, evolution_rate=self.evolution_rate, lst=constants.prey)


    def isDead(self):
        return (self.dead == True) | (self.health <= 0)

    