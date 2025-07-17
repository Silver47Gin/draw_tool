import tkinter as tk
from tool_plugin import ToolPlugin
from PIL import Image, ImageDraw, ImageTk

class BucketPlugin(ToolPlugin):
    def __init__(self):
        super().__init__('油桶')
        self.button_text = '油桶'
        self.image = None
        self.tk_image = None

    def set_canvas(self, canvas, width, height):
        # 初始化画布对应的PIL图像
        self.image = Image.new('RGB', (width, height), 'white')
        self.tk_image = ImageTk.PhotoImage(self.image)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas = canvas

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def draw(self, canvas, x, y, size=2, color='#000000'):
        # 只有初始化后才能填充
        if self.image is None:
            self.set_canvas(canvas, int(canvas['width']), int(canvas['height']))
        # 获取点击点颜色
        target_color = self.image.getpixel((x, y))
        fill_color = self._hex_to_rgb(color)
        if target_color == fill_color:
            return
        self._flood_fill(x, y, target_color, fill_color)
        self.update_canvas()

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _flood_fill(self, x, y, target_color, fill_color):
        width, height = self.image.size
        pixels = self.image.load()
        stack = [(x, y)]
        while stack:
            px, py = stack.pop()
            if px < 0 or px >= width or py < 0 or py >= height:
                continue
            if pixels[px, py] != target_color:
                continue
            pixels[px, py] = fill_color
            stack.extend([(px+1, py), (px-1, py), (px, py+1), (px, py-1)])
