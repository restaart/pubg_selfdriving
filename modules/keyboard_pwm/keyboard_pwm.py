import time
import threading
import keyboard
from .direct_input import keyCodes,PressKey,ReleaseKey

class KeyThread(threading.Thread):
    def __init__(self, key,period=0.1,duty=0):
        super().__init__()
        self.keyCode = keyCodes[key]
        self.period = period
        self.duty = duty
        self.enabled = True
        
    @property
    def duty(self):
        return self.__duty
    
    @duty.setter
    def duty(self,value):
        if value < 0:
            value = 0
        elif value > 1:
            value = 1
        self.__duty = value
        if value == 0:
            ReleaseKey(self.keyCode)
        elif value == 1:
            PressKey(self.keyCode)  
       
    def run(self):
        while(self.enabled):
            if(0<self.duty<1):
                PressKey(self.keyCode)
                time.sleep(self.period*self.duty)
                ReleaseKey(self.keyCode)
                time.sleep(self.period*(1-self.duty))
    def stop(self):
        self.enabled = False
        self.duty = 0
        self.join()

class KeyWatchThread(threading.Thread):
    def __init__(self, key,period=0.001):
        super().__init__()
        self.key = key
        self.recordedData = []
        self.enabled = True
        self.period = period
        
    def run(self):
        zero_time = time.time()
        while(self.enabled):
            self.recordedData.append((keyboard.is_pressed(self.key),time.time()-zero_time))
            time.sleep(self.period)

    def stop(self):
        self.enabled = False
        self.join()