import numpy as np

def turn(angle):
    angles = [90,80,70,60,50,45,0]

    left = ['q','a','y','w','s','x','g']
    right = ['p','k','-','o','l','.','g']
    
    if angle > 0:
        return left[angles.index(angle)]
    return right[angles.index(-angle)]

def add(x, y):
    return [x[0] + y[0], x[1] + y[1]]
def sub(x,y):
    return [x[0] - y[0], x[1] - y[1]]

def dir(car,goal,dist):
    # print(car, goal)
    angle = (car-goal+360) % 360
    if angle > 350 or angle <= 10:
        return 'g'
    #turn right
    if (angle > 10 and angle <= 30):
        return turn(45)
    if (angle > 30 and angle <= 50):
        return turn(60)
    if (angle > 50 and angle <= 70):
        return turn(70)
    if (angle > 70 and angle <= 90):
        return turn(80)
    if (angle > 90 and angle <= 180):
        return turn(90)
    #turn left
    if (angle > 330 and angle <= 350):
        return turn(-45)
    if (angle > 310 and angle <= 330):
        return turn(-60)
    if (angle > 290 and angle <= 310):
        return turn(-70)
    if (angle > 270 and angle <= 290):
        return turn(-80)
    if (angle > 180 and angle <= 270):
        return turn(-90)
    return 'g'

def angle(x,y):
    if x == 0:
        if y > 0:
            return 90
        else:
            return 270
    
    angle = np.arctan(y/x) * 180 / np.pi
    if x > 0 and y > 0: 
        return angle
    if x > 0 and y < 0:
        return 360 + angle
    if x < 0 and y < 0:
        return angle + 180
    if x < 0 and y > 0:
        return angle + 180
def foreach(ls, fn):
    for i in range(len(ls)):
        ls[i] = fn(ls[i])