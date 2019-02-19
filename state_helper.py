from enum import Enum
import time
from PIL import ImageGrab
from pynput.mouse import Button, Controller, Listener
from pynput.keyboard import Key, Controller as keyController
import numpy as np
import cv2

import settings
import pixel_helper
import kill_helper

mouse = Controller()
keyboard = keyController()
frame_count = 0

class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    STORE = 3


class StateHelper():
    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.money = 0

    def check_state(self):
        if self.state != GameState.MAIN_MENU:
            tmp = pixel_helper.get_pixel_greyscale(
                settings.start_menu[0], settings.start_menu[1])
            if tmp > 220:
                self.state = GameState.STORE
            else:
                self.state = GameState.GAME

    def handle_menu(self):
        time.sleep(1)
        mouse.position = settings.start_pos
        mouse.click(Button.left, 1)
        time.sleep(1)
        self.state = GameState.GAME

    def handle_game(self):
        global frame_count
        frame_count += 1
        bbox = settings.top_left + settings.bot_right
        screen = np.array(ImageGrab.grab(bbox=bbox))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        kill_helper.find_and_kill(screen)
        kill_helper.reload()
        self.check_state()

    def handle_store(self):
        money = int(pixel_helper.get_text_from_screen(
            [850, 420],
            [970, 435])[1:])
        mouse.position = settings.clip_buy_pos

        for i in range(int(money / 1000)):
            if i % 2:
                mouse.position = [
                    settings.clip_buy_pos[0] + 1,
                    settings.clip_buy_pos[1] + 1]
            else:
                mouse.position = settings.clip_buy_pos
            mouse.click(Button.left, 1)
            time.sleep(0.5)

        mouse.position = settings.done_pos
        mouse.click(Button.left, 1)
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
