from engi1020.arduino.api import *



def lightsoff():

    light = analog_read(6)
    if light <= 180:
        return True 
    else:
        return False
           
    
def lightson():

    light = analog_read(6)
    if light >= 180:
        return True
    else:
        return False


def pressbut():

    but = digital_read(6)
    if but:
        return True  
    else:
        return False
    
    
def swipeleft():

    Y = three_axis_get_accelY()
    if Y >= 0.9:
        return True
    
    else:
        return False
    
    
def swiperight():

    Y = three_axis_get_accelY()
    if Y <= -0.9:
        return True
    else:
        return False
    

def dialright():

    dial = analog_read(0)
    if dial <= 23:
        return True 
    else:
        return False
    
    
def dialleft():

    dial = analog_read(0)
    if dial >= 1000:
        return True
    else:
        return False
    
