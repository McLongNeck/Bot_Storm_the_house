import time
import math
from pynput.mouse import Button, Controller, Listener
from pynput.keyboard import Key, Controller as keyController
from PIL import ImageGrab
from enum import Enum
import numpy as np
import cv2
import pixel_helper

class GameState(Enum):
    MAIN_MENU = 1
    GAME = 2
    STORE = 3

state = GameState.MAIN_MENU

mouse = Controller()
keyboard = keyController()

top_left = [650, 660]
bot_right = [1150, 850]
start_menu = [1030, 830]
start_pos = [1100, 735]
reload_pos = [660, 425]
done_pos = [980, 830]
clip_buy_pos = [700, 512]

shots_per_target = 2
last_kill_pos = []
click_count = 0
width = 0
height = 0
bot_started = False
frame_count = 0
money = 0

def can_kill(target_pos):
    global last_kill_pos

    result = 0

    for coord in last_kill_pos:
        result = math.hypot(coord[0] - target_pos[0], coord[1] - target_pos[1])
        if result < 40:
            return False

    return True

def find_and_kill(screen):
    global mouse
    global last_kill_pos
    global frame_count
    global shots_per_target

    for y in range(len(screen)):
        for x in range(len(screen[y])):
            if screen[y][x] < 10:
                if can_kill([x, y]):
                    mouse.position = [x + top_left[0] + 2, y + top_left[1]]
                    last_kill_pos.insert(0, [x, y])
                    mouse.click(Button.left, shots_per_target)

    if frame_count > 5:
        last_kill_pos = []
        frame_count = 0

def reload():
    global keyboard

    if pixel_helper.get_pixel_greyscale(reload_pos[0], reload_pos[1]) > 170:
        keyboard.press(Key.space)
        time.sleep(0.2)
        keyboard.release(Key.space)
        print("Reloading!")

def check_state():
    global state

    if state != GameState.MAIN_MENU:
        tmp = pixel_helper.get_pixel_greyscale(start_menu[0], start_menu[1])
        if tmp > 220:
            state = GameState.STORE
        else:
            state = GameState.GAME

#state = GameState.STORE

while True:
    if state == GameState.MAIN_MENU:
        time.sleep(1)
        mouse.position = start_pos
        mouse.click(Button.left, 1)
        time.sleep(1)
        state = GameState.GAME
    elif state == GameState.GAME:
        frame_count += 1
        bbox = top_left + bot_right
        screen = np.array(ImageGrab.grab(bbox=bbox))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        find_and_kill(screen)
        reload()
        check_state()
    elif state == GameState.STORE:
        money = int(pixel_helper.get_text_from_screen([850, 420], [970, 435])[1:])
        mouse.position = clip_buy_pos

        for i in range(int(money / 1000)):
            if(i % 2):
                mouse.position = [clip_buy_pos[0] + 1, clip_buy_pos[1] + 1]
            else:
                mouse.position = clip_buy_pos
            mouse.click(Button.left, 1)
            time.sleep(0.5)

        mouse.position = done_pos
        mouse.click(Button.left, 1)
        state = GameState.GAME
        time.sleep(2)
    else:
        print("Gamestate not know: ", state)
