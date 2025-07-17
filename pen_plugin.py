import tkinter as tk
from tool_plugin import ToolPlugin

class PenPlugin(ToolPlugin):
    def __init__(self):
        super().__init__('画笔')
        self.button_text = '画笔'
    def draw(self, canvas, x1, y1, x2, y2, size=2, color='#000000'):
        canvas.create_line(x1, y1, x2, y2, fill=color, width=size, capstyle=tk.ROUND)
