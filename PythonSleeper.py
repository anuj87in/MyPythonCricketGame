import pyautogui
import time
import random
from datetime import datetime
import logging
import os
import subprocess

pyautogui.FAILSAFE = True

# Create log filename with timestamp
log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"PythonSleeper.{log_timestamp}.log"
log_path = os.path.join("C:\\Windows\\Temp", log_filename)

# Configure logging (only to file, not console)
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(log_path)
    ]
)

print ("Hello, you know what to do")

# Log script start
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info(f"Script started at {start_time}")

# Open Notepad and maximize it
#print("Opening Notepad...")
subprocess.Popen(['notepad.exe'])
time.sleep(2)  # Wait for Notepad to open

# Maximize the window
pyautogui.hotkey('win', 'up')  # Maximize window
time.sleep(1)
timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info(f"Notepad opened and maximized. Starting actions...at {timenow}")

# Define a list of keys to press randomly (removed some problematic keys for text input)
keys_to_press = ["f15", "f16", "f17", "f18", "f19", "f20", "ctrl", "shift", "alt", "tab", "space", "enter", 
'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 
'[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

# Define mouse actions (limited to within the text area)
mouse_actions = ["left_click", "right_click", "double_click"]

try:
    while True:
        # Randomly choose between key press or mouse action
        action_type = random.choice(["key", "mouse"])
        sleep_duration = random.randint(20, 50)
        timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if action_type == "key":
            random_key = random.choice(keys_to_press)
            message = f"Pressing key: \"{random_key}\" at {timenow}, and will be sleeping for: {sleep_duration} seconds"
            #print(message)
            logging.info(message)
            pyautogui.press(random_key)
        else:
            # Mouse action within Notepad text area
            mouse_action = random.choice(mouse_actions)
            # Get screen size and calculate Notepad text area (approximate)
            screen_width, screen_height = pyautogui.size()
            # Assuming Notepad text area is roughly 90% of screen with some margins
            text_area_left = int(screen_width * 0.05)
            text_area_right = int(screen_width * 0.95)
            text_area_top = int(screen_height * 0.15)  # Account for title bar and menu
            text_area_bottom = int(screen_height * 0.90)  # Account for status bar
            
            x = random.randint(text_area_left, text_area_right)
            y = random.randint(text_area_top, text_area_bottom)
            
            message = f"Mouse {mouse_action} at ({x}, {y}) in Notepad at {timenow}, and will be sleeping for: {sleep_duration} seconds"
            #print(message)
            logging.info(message)
            
            # Perform the mouse action
            if mouse_action == "left_click":
                pyautogui.click(x, y)
            elif mouse_action == "right_click":
                pyautogui.rightClick(x, y)
            elif mouse_action == "double_click":
                pyautogui.doubleClick(x, y)
        
        time.sleep(sleep_duration)
except KeyboardInterrupt:
    # Log script end
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Script ended at {end_time}")
    print ("Gosh , you did it")