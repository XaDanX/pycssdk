import random
import string
import time
from dataclasses import dataclass
from OpenGL.GL import *
from glfw import window_hint, get_video_mode
import glfw
import win32api
import win32con
import win32gui


@dataclass
class Result:
    width: float
    height: float
    mid_x: float
    mid_y: float
    hwnd: None


class Overlay:
    def __init__(self, target="F"):

        self.result: Result

        self.running = True

        glfw.init()
        window_hint(glfw.FLOATING, True)
        window_hint(glfw.DECORATED, False)
        window_hint(glfw.RESIZABLE, False)
        window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
        window_hint(glfw.SAMPLES, 8)

        if target == "F":
            video_mode = get_video_mode(glfw.get_primary_monitor())
            self.result = Result(video_mode.size.width,
                                 video_mode.size.height,
                                 video_mode.size.width / 2,
                                 video_mode.size.height / 2,
                                 None)
        else:
            hwnd = win32gui.FindWindow(None, target)
            rect = win32gui.GetWindowRect(hwnd)
            self.result = Result(rect[2],
                                 rect[3],
                                 rect[2] / 2,
                                 rect[3] / 2,
                                 None)

        self.window = glfw.create_window(self.result.width - 1, self.result.height - 1,
                                         title := ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                                         None, None)

        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.result.width, 0, self.result.height, -1, 1)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.result.hwnd = win32gui.FindWindow(None, title)
        exstyle = win32gui.GetWindowLong(self.result.hwnd, win32con.GWL_EXSTYLE)
        exstyle |= win32con.WS_EX_LAYERED
        exstyle |= win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(self.result.hwnd, win32con.GWL_EXSTYLE, exstyle)
        win32gui.SetWindowLong(self.result.hwnd, win32con.GWL_EXSTYLE,
                               exstyle | win32con.WS_EX_LAYERED)

    def update(self):
        glfw.swap_buffers(self.window)
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.poll_events()

    def close(self):
        glfw.set_window_should_close(self.window, True)
        glfw.destroy_window(self.window)
        glfw.terminate()

    def overlay_loop(self):
        if win32api.GetAsyncKeyState(win32con.VK_F4):
            self.running = False
            self.close()
        self.update()
        time.sleep(0.001)
        return self.running

    def line(self, x1, y1, x2, y2, width, color):
        glLineWidth(width)
        glBegin(GL_LINES)
        glColor3f(color[0], color[1], color[2])
        glVertex2f(x2, y2)
        glVertex2f(x1, y1)
        glEnd()

    def box(self, x, y, width, height, line_width, color):
        glLineWidth(line_width)
        glBegin(GL_LINE_LOOP)
        glColor4f(color[0], color[1], color[2], 255)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def _draw_corner(self, x, y, lineW, lineH, width, height):
        glBegin(GL_LINES)
        glVertex2f(x, y)
        glVertex2f(x + lineW, y)
        glVertex2f(x, y)
        glVertex2f(x, y + lineH)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + lineH)
        glVertex2f(x + width, y)
        glVertex2f(x + width - lineW, y)
        glVertex2f(x, y + height)
        glVertex2f(x, y + height - lineH)
        glVertex2f(x, y + height)
        glVertex2f(x + lineW, y + height)
        glVertex2f(x + width, y + height)
        glVertex2f(x + width, y + height - lineH)
        glVertex2f(x + width, y + height)
        glVertex2f(x + width - lineW, y + height)
        glEnd()

    def corner_box(self, x, y, width, height, line_width, color, outline_color):
        lineW = width / 4
        lineH = height / 3
        glLineWidth(line_width + 2)
        glColor3f(*outline_color)
        self._draw_corner(x, y, lineW, lineH, width, height)
        glLineWidth(line_width)
        glColor3f(*color)
        self._draw_corner(x, y, lineW, lineH, width, height)
