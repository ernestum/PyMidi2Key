import time
import os
import warnings
import pygame.midi
import pyautogui

pygame.midi.init()

def midi_input_device_ids():
    return [i for i in range(pygame.midi.get_count()) if pygame.midi.get_device_info(i)[2] == 1]

def pick_midi_input_device(chosen_idx = -1):
    in_device_ids = midi_input_device_ids()
    if len(in_device_ids) == 0:
        warnings.warn("no midi input devices found!")
        return None
    if len(in_device_ids) == 1:
        chosen_idx = 0
    while not 0 <= chosen_idx <= len(in_device_ids):
        for num, idx in enumerate(in_device_ids):
            print(f"{num}: {pygame.midi.get_device_info(idx)[1].decode()}")
        try:
            chosen_idx = int(input(f"pick midi device (0-{len(in_device_ids)-1}):"))
        except ValueError:
            warnings.warn("can't parse this")
    print(f"Using {pygame.midi.get_device_info(in_device_ids[chosen_idx])[1].decode()}")
    return pygame.midi.Input(in_device_ids[chosen_idx])

held_screens = set()

def handle_event(event):
    (status, data1, data2, data3), timestamp = event

    if 41 <= data1 <= 49: # Screen Switching Logic
        screen = data1 - 41 + 1
        down = status == 144
        if down:
            held_screens.add(screen)
            if len(held_screens) > 1:
                pyautogui.keyDown('ctrl')
            pyautogui.keyDown('winleft')
            pyautogui.keyDown(str(screen))
        else:
            if len(held_screens) > 1:
                pyautogui.keyUp('ctrl')
            pyautogui.keyUp('winleft')
            pyautogui.keyUp(str(screen))
            held_screens.remove(screen)

    if status == 144 and data1 == 57: # Copy
        pyautogui.hotkey('ctrl', 'c')

    if status == 144 and data1 == 62: # Paste
        pyautogui.hotkey('ctrl', 'v')

    if status == 144 and data1 == 52: # Firefox
        os.system("firefox")

    # TODO: add more shortcuts here
            

if __name__ == "__main__":
    device = pick_midi_input_device()
    if device is None:
        sys.exit(1)
    try:
        while True:
            events = device.read(100)
            for event in events:
                print(f"status == {event[0][0]} and data1 == {event[0][1]}")
                print(event)
                print()
                handle_event(event)
            time.sleep(0.02)
    finally:
        device.close()
