import tkinter as tk
from tool_plugin import ToolPlugin

class EraserPlugin(ToolPlugin):
    def __init__(self):
        super().__init__('橡皮')
        self.button_text = '橡皮'
    def draw(self, canvas, x1, y1, x2, y2, size=20):
        canvas.create_line(x1, y1, x2, y2, fill='white', width=size, capstyle=tk.ROUND)
