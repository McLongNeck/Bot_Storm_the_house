import time
import math

import pixel_helper
from state_helper import static_state_helper as sh
from io_helper import static_io_helper as ioh
import settings


class KillHelper():
    def __init__(self):
        self.last_kill_pos = []

    def can_kill(self, target_pos):
        for coord in self.last_kill_pos:
            result = math.hypot(
                coord[0] - target_pos[0], coord[1] - target_pos[1])
            if result < 40:
                return False
        return True

    def find_and_kill(self):
        screen = pixel_helper.get_gray_image(
            settings.top_left, settings.bot_right)
        for y in range(len(screen)):
            for x in range(len(screen[y])):
                if screen[y][x] < 10:
                    if self.can_kill([x, y]):
                        ioh.mouse.position = [
                            x + settings.top_left[0] + 2,
                            y + settings.top_left[1]]
                        self.last_kill_pos.insert(0, [x, y])
                        ioh.click(settings.shots_per_target)

        if sh.frame_count > 5:
            self.last_kill_pos = []
            sh.frame_count = 0

    def reload(self):
        if pixel_helper.get_pixel_greyscale(settings.reload_pos[0], settings.reload_pos[1]) > 170:
            ioh.space()
            time.sleep(0.2)
            ioh.space()


static_kill_helper = KillHelper()
