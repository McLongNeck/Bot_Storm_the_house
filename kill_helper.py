import time
import math
from pynput.mouse import Button
from pynput.keyboard import Key

import pixel_helper
import state_helper
import settings

class KillHelper():
    def __init__(self):
        self.last_kill_pos = []

    def can_kill(self, target_pos):
        for coord in self.last_kill_pos:
            result = math.hypot(coord[0] - target_pos[0], coord[1] - target_pos[1])
            if result < 40:
                return False
        return True

    def find_and_kill(self, screen):
        for y in range(len(screen)):
            for x in range(len(screen[y])):
                if screen[y][x] < 10:
                    if self.can_kill([x, y]):
                        state_helper.mouse.position = [
                            x + settings.top_left[0] + 2,
                            y + settings.top_left[1]]
                        self.last_kill_pos.insert(0, [x, y])
                        state_helper.mouse.click(
                            Button.left,
                            settings.shots_per_target)

        if state_helper.frame_count > 5:
            self.last_kill_pos = []
            state_helper.frame_count = 0

    def reload(self):
        if pixel_helper.get_pixel_greyscale(settings.reload_pos[0], settings.reload_pos[1]) > 170:
            state_helper.keyboard.press(Key.space)
            time.sleep(0.2)
            state_helper.keyboard.release(Key.space)
