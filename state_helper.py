from enum import Enum
import time

import settings
import pixel_helper
from kill_helper import static_kill_helper as kh
from io_helper import static_io_helper as ioh


class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    STORE = 3


class StateHelper():
    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.money = 0
        self.frame_count = 0

    def check_state(self):
        if self.state != GameState.MAIN_MENU:
            tmp = pixel_helper.get_pixel_greyscale(
                settings.start_menu[0],
                settings.start_menu[1])
            if tmp > 220:
                self.state = GameState.STORE
            else:
                self.state = GameState.GAME

    def handle_menu(self):
        time.sleep(1)
        ioh.mouse.position = settings.start_pos
        ioh.mouse.click()
        time.sleep(1)
        self.state = GameState.GAME

    def handle_game(self):
        self.frame_count += 1
        kh.find_and_kill()
        kh.reload()
        self.check_state()

    def handle_store(self):
        money = int(pixel_helper.get_text_from_screen(
            [850, 420],
            [970, 435])[1:])
        ioh.mouse.position = settings.clip_buy_pos

        for i in range(int(money / 1000)):
            if i % 2:
                ioh.mouse.position = [
                    settings.clip_buy_pos[0] + 1,
                    settings.clip_buy_pos[1] + 1]
            else:
                ioh.mouse.position = settings.clip_buy_pos
            ioh.click()
            time.sleep(0.5)

        ioh.mouse.position = settings.done_pos
        ioh.click()
        self.state = GameState.GAME
        time.sleep(2)

    def handle_states(self):
        if self.state == GameState.MAIN_MENU:
            self.handle_menu()
        elif self.state == GameState.GAME:
            self.handle_game()
        elif self.state == GameState.STORE:
            self.handle_store()
        else:
            print("Gamestate not know: ", self.state)


static_state_helper = StateHelper()
