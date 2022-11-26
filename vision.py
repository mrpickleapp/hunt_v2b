import pygame
import numpy as np

import constants
import calc

class Eye:

    def __init__(self, parent, angle=0, length=20):

        self.parent=parent
        self.angle=angle
        self.length=length
        self.obstacleDetected=False

    def detectObstacles(self, enemies):

        self.rayStart = self.parent.location

        angle = self.parent.angle + self.angle
        self.rayEnd = calc.addVectors(self.rayStart, calc.scaleVector(calc.vectorFromAngle(angle), self.length))

        for enemy in enemies:
            if calc.lineIntersectsCircle(self.rayStart, self.rayEnd, enemy.location, enemy.radius) > 0:
                self.obstacleDetected = True
                return [1, 1]   # detected, and is enemy

        # wall detection
        if calc.outOfBounds(self.rayEnd):
            self.obstacleDetected = True
            return [1, 0]   

        self.obstacleDetected = False
        return [0, 0]

    def draw(self):
        colour = "grey" if self.obstacleDetected == False else "red"
        pygame.draw.line(
            constants.screen, 
            colour, 
            [self.rayStart[0], calc.flipY(self.rayStart[1])], 
            [self.rayEnd[0], calc.flipY(self.rayEnd[1])],
            1
        )


class personalSpace:

    def __init__(self, parent, channels, detection_range):
        self.parent = parent
        self.channels = channels
        self.detection_range = detection_range

        self.channel_angles = []
        self.angle_delta = (2 * np.pi) / self.channels
        for i in range(1, self.channels+1):
            self.channel_angles.append(-np.pi + (self.angle_delta * i))


    def detectEnemies(self, enemies):

        # return output = list of channels
        # with number of enemies per channel
        # and 1/distance of closest enemy per channel
        # 

        self.enemy_flags = [0 for i in range(self.channels)]
        self.enemy_distances = [0 for i in range(self.channels)]

        heading = calc.vectorFromAngle(self.parent.angle)

        enemyInRange = 0
        nearestEnemyDistance = 0
        nearestEnemyAngle = 0

        nearestEnemyVector = None

        for enemy in enemies:

            vector = calc.getLineVector(self.parent.location, enemy.location)
            distance = np.linalg.norm(vector)

            if distance < (self.detection_range + enemy.radius):

                enemyInRange = 1
                d = 1/distance
                if d > nearestEnemyDistance:
                    nearestEnemyDistance = d
                    nearestEnemyVector = vector

        if enemyInRange == 1:

            nearestEnemyAngle = calc.signedTheta(heading, nearestEnemyVector)

        return [enemyInRange, nearestEnemyDistance, nearestEnemyAngle]

        """
        # for each enemy, if in range, find angle
        for enemy in enemies:

            vector = calc.getLineVector(self.parent.location, enemy.location)
            distance = np.linalg.norm(vector)

            if distance < (self.detection_range + enemy.radius):

                # find angle to enemy
                angle = calc.signedTheta(heading, vector)

                for i, channel_angle in enumerate(self.channel_angles):

                    if angle < channel_angle:
                        self.enemy_flags[i] += 1
                        d = 1/distance
                        self.enemy_distances[i] = max(d, self.enemy_distances[i])
        """

        output = []
        output.extend(self.enemy_flags)
        output.extend(self.enemy_distances)

        return output

    def draw(self):

        for i, angle in enumerate(self.channel_angles):

            channel_vector = calc.vectorFromAngle(self.parent.angle + angle)
            channel_vector = calc.scaleVector(channel_vector, self.detection_range)
            ray_start = self.parent.location
            ray_end = calc.addVectors(self.parent.location, channel_vector)
            colour = "grey" if self.enemy_flags[i] == 0 else "red"

            pygame.draw.line(
                constants.screen, 
                colour, 
                [ray_start[0], calc.flipY(ray_start[1])], 
                [ray_end[0], calc.flipY(ray_end[1])],
                1
            )


# Field of Vision
# Eg, animal can see in an arc forwards and to the right
# Test radius + angle
class FoV:

    def __init__(self, parent, startAngle, endAngle, range):
        self.parent = parent
        self.startAngle = startAngle,
        self.endAngle = endAngle,
        self.range = range

        self.obstacleDetected = False


    def detectObstacles(self, obstacles):

        self.obstacleDetected = False

        obstaclesDetected = 0
        nearestObstacleDistance = 0
        nearestObstacleAngle = 0

        for obstacle in obstacles:

            # all obstacles are circles
            vector = calc.getLineVector(self.parent.location, obstacle['centre'])
            distance = np.linalg.norm(vector)

            # object is in range
            if distance <= (obstacle['radius'] + self.range):

                # angle to obstacle
                angle = calc.signedTheta(calc.vectorFromAngle(self.parent.angle), vector)

                # in FoV
                if (angle >= self.startAngle) & (angle <= self.endAngle):

                    if self.obstacleDetected == False:
                        self.obstacleDetected = True
                        obstaclesDetected = 1
                        nearestObstacleDistance = distance
                        nearestObstacleAngle = angle
                    
                    else:
                        obstaclesDetected += 1
                        if distance < nearestObstacleDistance:
                            nearestObstacleDistance = distance
                            nearestObstacleAngle = angle

        return [obstaclesDetected, nearestObstacleDistance, nearestObstacleAngle]


    def draw(self):
        colour = "grey" if self.obstacleDetected == False else "red"

        startEnd = calc.addVectors(self.parent.location, calc.scaleVector(calc.vectorFromAngle(self.parent.angle + self.startAngle), self.range))
        endEnd = calc.addVectors(self.parent.location, calc.scaleVector(calc.vectorFromAngle(self.parent.angle + self.endAngle), self.range))

        # start
        pygame.draw.line(
            constants.screen, 
            colour, 
            [self.parent.location[0], calc.flipY(self.parent.location[1])], 
            [int(startEnd[0]), calc.flipY(int(startEnd[1]))],
            1
        )

        # end
        pygame.draw.line(
            constants.screen, 
            colour, 
            [self.parent.location[0], calc.flipY(self.parent.location[1])], 
            [int(endEnd[0]), calc.flipY(int(endEnd[1]))],
            1
        )





