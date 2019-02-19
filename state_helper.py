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


class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    STORE = 3


state = GameState.MAIN_MENU
frame_count = 0
money = 0


def check_state():
    global state

    if state != GameState.MAIN_MENU:
        tmp = pixel_helper.get_pixel_greyscale(
            settings.start_menu[0], settings.start_menu[1])
        if tmp > 220:
            state = GameState.STORE
        else:
            state = GameState.GAME


def handle_menu():
    global state

    time.sleep(1)
    mouse.position = settings.start_pos
    mouse.click(Button.left, 1)
    time.sleep(1)
    state = GameState.GAME


def handle_game():
    global frame_count

    frame_count += 1
    bbox = settings.top_left + settings.bot_right
    screen = np.array(ImageGrab.grab(bbox=bbox))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    kill_helper.find_and_kill(screen)
    kill_helper.reload()
    check_state()


def handle_store():
    global state
    global money

    money = int(pixel_helper.get_text_from_screen([850, 420], [970, 435])[1:])
    mouse.position = settings.clip_buy_pos

    for i in range(int(money / 1000)):
        if (i % 2):
            mouse.position = [settings.clip_buy_pos[0] +
                              1, settings.clip_buy_pos[1] + 1]
        else:
            mouse.position = settings.clip_buy_pos
        mouse.click(Button.left, 1)
        time.sleep(0.5)

    mouse.position = settings.done_pos
    mouse.click(Button.left, 1)
    state = GameState.GAME
    time.sleep(2)


def handle_tates():
    if state == GameState.MAIN_MENU:
        handle_menu()
    elif state == GameState.GAME:
        handle_game()
    elif state == GameState.STORE:
        handle_store()
    else:
        print("Gamestate not know: ", state)
