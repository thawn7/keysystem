# MISA

import dearpygui.dearpygui as dpg
import torch
import cv2
import numpy as np
from mss import mss
import ctypes
from termcolor import colored
import win32api,win32con
import csv
import time
import mss
import os
import sys

if not os.getenv('778877s'):
    print("Please run from START.bat.")
    sys.exit(1)
#if "RUN_FROM_BAT" not in os.environ:
    #print("Error: Please run the 'run.py'")
    #sys.exit(1)

dpg.create_context()
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

dpg.create_viewport(title='Misa', width=508, height=265, resizable=False)
dpg.set_viewport_always_top(True)
width, height, channels, data = dpg.load_image(r'settings/misa.png')
model = torch.hub.load(r'settings/yolov5', 'custom', path=r'settings/s.pt', source='local').cuda()
model.apm = True
model.conf = 0.61

# default values
aim_speed = None
speed_val = 0
smooth_val = 0
dead_val = 0
enable_opencv = False
fov_size = 130

colores = (47, 136,165, 250,255)
rio_center = 125


def mouse(sender, data):
    global speed_val
    speed_val = float(dpg.get_value(mouse_slider))
def smooth(sender, data):
    global smooth_val
    smooth_val = float(dpg.get_value(smooth_slider))
def dead(sender, data):
    global dead_val
    dead_val = float(dpg.get_value(dead_slider))
def fovv(sender, data):
    global fov_size
    fov_size = float(dpg.get_value(fov_slider))

def save_settings(sender, data):
    with open(r'settings/settings.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['speed_val', 'smooth_val', 'dead_val','fov_size'])
        writer.writerow([speed_val, smooth_val, dead_val, fov_size])
    print(colored('''Settings saved!''', "light_cyan"))
    
def load_settings(sender, data):
    with open(r'settings/settings.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        row = next(reader)
        global speed_val, smooth_val, dead_val, fov_size
        speed_val, smooth_val, dead_val, fov_size = [int(x) if x.isdigit() else float(x) for x in row]
        rio_center = 250 // 2  # update rio_center based on loaded region_size
    print(colored('''Settings loaded!''', "light_cyan"))
    dpg.set_value(mouse_slider, speed_val)
    dpg.set_value(smooth_slider, smooth_val)
    dpg.set_value(dead_slider, dead_val)
    dpg.set_value(fov_slider,fov_size)
def toggle_opencv(sender, data):
    global enable_opencv
    enable_opencv = dpg.get_value(sender)
    

with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="picture")

with dpg.window(tag="Primary Window"):
    with dpg.window(label="girl", no_title_bar=True,no_resize=True,no_move=True,no_background=True,no_scrollbar=False, width=400, height=435, pos=(140, -130)):
        with dpg.drawlist(width=400, height=400):
            dpg.draw_image("picture", (80, 80), (width, height), uv_min=(0, 0), uv_max=(1, 1))
with dpg.window(label="Main Menu", no_title_bar=True,no_resize=True, no_background=True,no_scrollbar=False,no_move=True,width=800):
    dpg.add_text("                          Misa",color=(0,0,0))
    
    mouse_slider = dpg.add_slider_float(label="MAIN SPEED", default_value=0, min_value=0, max_value=5,width=210,
                                        callback=mouse, format="%.1f")
    smooth_slider = dpg.add_slider_float(label="SMOOTH SPEED", default_value=0, min_value=0, max_value=20,width=210,
                                        callback=smooth, format="%.0f")
    dead_slider = dpg.add_slider_float(label="DEADZONE", default_value=0, min_value=0, max_value=200,width=210,
                                        callback=dead, format="%.1f")
    fov_slider = dpg.add_slider_float(label="FOV Size", default_value=130, min_value=0, max_value=300, width=210,
                                        callback=fovv, format="%.2f")
    dpg.add_checkbox(label="Enable OpenCV", default_value=False, callback=toggle_opencv)

    dpg.add_button(label="Save Settings", callback=save_settings)
    dpg.add_button(label="Load Settings", callback=load_settings)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (250, 250, 250), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (204, 204, 204), category=dpg.mvThemeCat_Core) # good
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(247, 226, 190), category=dpg.mvThemeCat_Core) # good
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (128, 128, 128), category=dpg.mvThemeCat_Core) 
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (242, 242, 242), category=dpg.mvThemeCat_Core) # good
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 0, 0), category=dpg.mvThemeCat_Core) # good
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (247, 226, 190), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (247, 226, 190), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (241, 237, 237), category=dpg.mvThemeCat_Core)


dpg.bind_theme(global_theme)
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
#dpg.show_style_editor()
dpg.setup_dearpygui()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    # Capture screen using mss
    fullscreen = (1920,1080)
    right, bottom = 250, 250
    left = (fullscreen[0] - right) // 2
    top = (fullscreen[1] - bottom) // 2
    right = left + right
    bottom = top + bottom
    rejoin = (left, top, right, bottom)

    fov_width, fov_height = fov_size, fov_size
    fov_left = rio_center - fov_width // 2
    fov_right = rio_center + fov_width // 2
    fov_top = rio_center - fov_height // 2
    fov_bottom = rio_center + fov_height // 2

    with mss.mss() as sct:
        screenshot = np.array(sct.grab(rejoin))
        df = model(screenshot, size=416).pandas().xyxy[0]
        rio_center = rio_center
        min_distance = float('inf')
        closest_object = None
        for i in range(len(df)):
            xmin, ymin, xmax, ymax = map(int, df.iloc[i, :4])
            height = ymax - ymin
            object_center = int((xmin + xmax) / 2), int((ymin + ymax) / 2 - height / 5)
            cv2.circle(screenshot, object_center, radius=3, color=(214, 51, 255), thickness=3)
            cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (8, 171, 252), 3)
            distance = ((object_center[0] - rio_center) ** 2 + (object_center[1] - rio_center) ** 2) ** 0.6
            
            if distance < min_distance:
                min_distance = distance
                closest_object = object_center

        if win32api.GetKeyState(0xA0) in (-127, -128):
            if closest_object is not None and closest_object[0] >= fov_left and closest_object[0] <= fov_right and \
                    closest_object[1] >= fov_top and closest_object[1] <= fov_bottom:
                for i in range(len(df)):
                    xmin, ymin, xmax, ymax = map(int, df.iloc[i, :4])
                    if distance <= dead_val + max((xmax - xmin), (ymax - ymin)) // 2:
                        aim_speed = speed_val # FAST FOR TRACKING
                        break
                else:
                    aim_speed = smooth_val # SLOW FOR SMOOTHING
            if aim_speed is not None and aim_speed != 0 and closest_object is not None:
                dx = int((closest_object[0] - rio_center) / aim_speed)
                dy = int((closest_object[1] - rio_center) / aim_speed)
                mouse_input = MouseInput(dx, dy, 0, win32con.MOUSEEVENTF_MOVE, 0, None)
                input_data = Input(win32con.INPUT_MOUSE, Input_I(mi=mouse_input))
                ctypes.windll.user32.SendInput(1, ctypes.byref(input_data), ctypes.sizeof(input_data))
        else:
            aim_speed = smooth_val
            
        #cv2.putText(screenshot, f"mouse: {aim_speed}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if enable_opencv:
        cv2.imshow('Screen', screenshot)
    else:
        cv2.destroyAllWindows()

sct.close()
cv2.destroyAllWindows()
dpg.destroy_context()
