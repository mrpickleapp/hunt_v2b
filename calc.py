import constants
import numpy as np
from random import randint
import math

def flipY(y):
    return constants.SCREEN_Y - y


def getLineVector(A, B):

    vector = [B[0] - A[0], B[1] - A[1]]

    return vector


def normaliseVector(vector):

    n = np.linalg.norm(vector)

    return [v / n for v in vector]


def addVectors(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def subVectors(a, b):
    return [a[0] - b[0], a[1] - b[1]]


def pointDistance(a, b):

    line = getLineVector(a, b)

    return np.linalg.norm(line)


def theta(v1, v2): 
    r"""Angle between two vectors, in radians, measured from vector roots
    :param v1 [x, y]
    :param v1 [x, y]
    :return angle (radians)
    """
    return np.arccos(np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))

def signedTheta(v1, v2):

    th = theta(v1, v2)

    if np.cross(v1, v2) > 0:
        return th
    else:
        return th * -1


def outOfBounds(location):
    if location[0] < 0:
        return True
    elif location[0] > constants.SCREEN_X:
        return True
    if location[1] < 0:
        return True
    elif location[1] > constants.SCREEN_Y:
        return True
    return False


def applyBoundaries(location):
    if location[0] < 0:
        location[0] = 0
    elif location[0] > constants.SCREEN_X:
        location[0] = constants.SCREEN_X
    if location[1] < 0:
        location[1] = 0
    elif location[1] > constants.SCREEN_Y:
        location[1] = constants.SCREEN_Y
    return location

def wrapBoundaries(location):
    if location[0] < 0:
        location[0] += constants.SCREEN_X
    elif location[0] > constants.SCREEN_X:
        location[0] -= constants.SCREEN_X
    if location[1] < 0:
        location[1] += constants.SCREEN_Y
    elif location[1] > constants.SCREEN_Y:
        location[1] -= constants.SCREEN_Y
    return location

def inZone(location):
    if (location[0] < 50) | (location[0] > constants.SCREEN_X - 50):
        return False
    if (location[1] < 50) | (location[1] > constants.SCREEN_Y - 50):
        return False
    return True


def vectorFromAngle(a):
    return [np.cos(a), np.sin(a)]


def scaleVector(vector, length):
    f = length / np.linalg.norm(vector)
    return [f * i for i in vector]

def randomColour():
    return [randint(0, 255), randint(0, 255), randint(0, 255)]


def applyEvolution(n, evolution_rate):

    n += 0.5
    n *= np.random.normal(loc=1, scale=evolution_rate, size=1)
    n -= 0.5

    return n


def lineIntersectsCircle(lineStart, lineEnd, circleCentre, circleRadius):

    d = subVectors(lineEnd, lineStart)       # direction vector of ray from start to end
    f = subVectors(lineStart, circleCentre)       # vector from centre circle to ray start

    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - circleRadius*circleRadius

    disc = b*b - 4 * a * c

    hit = 0

    if disc >= 0:

        disc = math.sqrt(disc)
        t1 = (-b - disc) / (2 * a)
        t2 = (-b + disc) / (2 * a)

        if (t1 >= 0) & (t1 <= 1):
            hit = 1

        elif (t2 >= 0) & (t2 <= 1):
            hit = 1

    return hit


def partAgents(agents):

    for i, agent in enumerate(agents):

        for other in agents[i+1:]:

            x_dist = agent.location[0] - other.location[0]
            y_dist = agent.location[1] - other.location[1]

            min_dist = agent.radius + other.radius

            if x_dist**2 + y_dist**2 < min_dist**2:

                # too close
                if agent.location[0] < other.location[0]:
                    agent.location[0] -= 2
                    other.location[0] -= 2
                else:
                    agent.location[0] += 2
                    other.location[0] += 2

                if agent.location[1] < other.location[1]:
                    agent.location[1] -= 2
                    other.location[1] -= 2
                else:
                    agent.location[1] += 2
                    other.location[1] += 2
