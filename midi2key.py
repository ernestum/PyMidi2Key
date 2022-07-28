import time
import os
import sys
import warnings
import pygame.midi
import pyautogui

pygame.midi.init()

def midi_input_device_ids(device_filter = ""):
    return [i for i in range(pygame.midi.get_count()) if device_filter in pygame.midi.get_device_info(i)[1].decode() and pygame.midi.get_device_info(i)[2] == 1]

def pick_midi_input_device(device_filter = ""):
    in_device_ids = midi_input_device_ids(device_filter)
    if len(in_device_ids) == 0:
        warnings.warn("no midi input devices found!")
        return None
    if len(in_device_ids) == 1:
        chosen_idx = 0
    else:
        chosen_idx = -1
    while not 0 <= chosen_idx <= len(in_device_ids):
        for num, idx in enumerate(in_device_ids):
            print(f"{num}: {pygame.midi.get_device_info(idx)[1].decode()}")
        try:
            chosen_idx = int(input(f"pick midi device (0-{len(in_device_ids)-1}):"))
        except ValueError:
            warnings.warn("can't parse this")
    print(f"Using {pygame.midi.get_device_info(in_device_ids[chosen_idx])[1].decode()}")
    return pygame.midi.Input(in_device_ids[chosen_idx])

held_tags= set()

def handle_event(event):
    (status, data1, data2, data3), timestamp = event

    if 41 <= data1 <= 49: # Tag switching logic for AwesomeWM. Press a chord to select multiple tags!
        tag = data1 - 41 + 1
        down = status == 144
        if down:
            held_tags.add(tag)
            if len(held_tags) > 1:
                pyautogui.keyDown('ctrl')
            pyautogui.keyDown('winleft')
            pyautogui.keyDown(str(tag))
        else:
            if len(held_tags) > 1:
                pyautogui.keyUp('ctrl')
            pyautogui.keyUp('winleft')
            pyautogui.keyUp(str(tag))
            held_tags.remove(tag)

    if status == 144 and data1 == 57: # Copy
        pyautogui.hotkey('ctrl', 'c')

    if status == 144 and data1 == 62: # Paste
        pyautogui.hotkey('ctrl', 'v')

    if status == 144 and data1 == 52: # Firefox
        os.system("firefox")

    # TODO: add more shortcuts here
            

if __name__ == "__main__":
    device = pick_midi_input_device(device_filter = sys.argv[1] if len(sys.argv) > 1 else "")
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
