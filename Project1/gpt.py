import glfw
from OpenGL.GL import *
import glm
import numpy as np

# Constants for window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Camera parameters
camera_position = glm.vec3(0.0, 0.0, 3.0)
camera_target = glm.vec3(0.0, 0.0, 0.0)
camera_up = glm.vec3(0.0, 1.0, 0.0)
camera_yaw = -90.0
camera_pitch = 0.0
camera_fov = 45.0
is_perspective = True

# Mouse input parameters
is_mouse_left_button_pressed = False
is_mouse_right_button_pressed = False
is_mouse_scroll = False
last_mouse_x = 0.0
last_mouse_y = 0.0

# Projection and view matrices
projection_matrix = glm.mat4(1.0)
view_matrix = glm.mat4(1.0)

# Helper function to handle GLFW errors
def error_callback(error, description):
    print(f"GLFW Error: {description}")

# GLFW key callback function to toggle projection mode
def key_callback(window, key, scancode, action, mods):
    global is_perspective
    if action == glfw.PRESS and key == glfw.KEY_V:
        is_perspective = not is_perspective

# GLFW mouse button callback function to handle camera manipulation
def mouse_button_callback(window, button, action, mods):
    global is_mouse_left_button_pressed, is_mouse_right_button_pressed, last_mouse_x, last_mouse_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            is_mouse_left_button_pressed = True
            last_mouse_x, last_mouse_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            is_mouse_left_button_pressed = False
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            is_mouse_right_button_pressed = True
            last_mouse_x, last_mouse_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            is_mouse_right_button_pressed = False

# GLFW scroll callback function to handle zooming
def scroll_callback(window, xoffset, yoffset):
    global camera_fov, is_mouse_scroll
    camera_fov -= yoffset
    if camera_fov < 1.0:
        camera_fov = 1.0
    if camera_fov > 45.0:
        camera_fov = 45.0
    is_mouse_scroll = True

# Helper function to update the view matrix based on camera parameters
def update_view_matrix():
    global view_matrix
    rotation_matrix = glm.mat4(1.0)
    rotation_matrix = glm.rotate(rotation_matrix, glm.radians(camera_yaw), glm.vec3(0.0, 1.0, 0.0))
    rotation_matrix = glm.rotate(rotation_matrix, glm.radians(camera_pitch), glm.vec3(1.0, 0.0, 0.0))
    view_matrix = glm.lookAt(camera_position, camera_target, camera_up) * rotation_matrix

# Initialize GLFW
if not glfw.init():
    print("Failed to initialize GLFW")
    exit()

# Create a window
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "OpenGL Viewer", None, None)
if not glfw.init():
    print("Failed to initialize GLFW")
    exit()

# Create a window
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "OpenGL
