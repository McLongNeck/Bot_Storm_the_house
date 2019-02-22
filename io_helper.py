from pynput.mouse import Controller as mouseController
from pynput.mouse import Button as mouseButton
from pynput.keyboard import Controller as kbController
from pynput.keyboard import Key as kbKey


class IOHelper():
    def __init__(self):
        self.mouse = mouseController()
        self.keyboard = kbController()

    def click(self, count = 1):
        self.mouse.click(mouseButton.left, count)

    def space(self,):
        self.keyboard.release(kbKey.space)


static_io_helper = IOHelper()
