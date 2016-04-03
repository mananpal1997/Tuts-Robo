from pymouse import *
import pyautogui

class Clickonacci(PyMouseEvent) :
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.m = PyMouse()
        self.a = []

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                self.a.append(self.m.position())
                if(len(self.a) == 2):
                    #print(self.a)
                    x1,y1,x2,y2 = self.a[0][0],self.a[0][1],self.a[1][0],self.a[1][1]
                    pyautogui.screenshot('C:/Python27/output.png',(x1,y1,x2-60,y2-150))
                    self.a = []
                    self.stop()
        else:  # Exit if any other mouse button used
            self.stop()
