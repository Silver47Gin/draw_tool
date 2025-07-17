import tkinter as tk
from pen_plugin import PenPlugin
from eraser_plugin import EraserPlugin

class DrawBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('画板程序')
        self.geometry('900x600')

        # 插件注册
        from bucket_plugin import BucketPlugin
        self.plugins = {
            'pen': PenPlugin(),
            'eraser': EraserPlugin(),
            'bucket': BucketPlugin()
        }
        self.current_tool = 'pen'

        # 侧边栏
        self.sidebar = tk.Frame(self, width=100, bg='#f0f0f0')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)


        self.tool_var = tk.StringVar(value='pen')
        # 动态生成按钮，text由插件提供
        for key, plugin in self.plugins.items():
            btn = tk.Radiobutton(
                self.sidebar,
                text=getattr(plugin, 'button_text', plugin.name),
                variable=self.tool_var,
                value=key,
                indicatoron=False,
                width=10,
                command=self.change_tool
            )
            btn.pack(pady=20)

        # 笔刷大小调节
        tk.Label(self.sidebar, text='笔刷大小').pack(pady=(40, 5))
        self.brush_size = tk.IntVar(value=2)
        self.size_scale = tk.Scale(self.sidebar, from_=1, to=50, orient=tk.HORIZONTAL, variable=self.brush_size)
        self.size_scale.pack(pady=5)

        # 颜色选择面板（仅画笔可用）
        tk.Label(self.sidebar, text='画笔颜色').pack(pady=(30, 5))
        self.color_var = tk.StringVar(value='#000000')
        colors = ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
        color_frame = tk.Frame(self.sidebar)
        color_frame.pack(pady=5)
        for c in colors:
            btn = tk.Radiobutton(color_frame, bg=c, width=2, variable=self.color_var, value=c, indicatoron=False)
            btn.pack(side=tk.LEFT, padx=2)

        self.canvas = tk.Canvas(self, bg='white', width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 初始化油桶插件的PIL画布
        if 'bucket' in self.plugins:
            self.plugins['bucket'].set_canvas(self.canvas, 800, 600)

        # 撤销按钮
        self.undo_stack = []
        undo_btn = tk.Button(self.sidebar, text='撤销', command=self.undo)
        undo_btn.pack(pady=(30, 5))

        self.last_x, self.last_y = None, None
        self.canvas.bind('<Button-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def change_tool(self):
        self.current_tool = self.tool_var.get()

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        # 记录当前画布状态
        self.save_state()
        # 油桶工具点击时直接填充
        if self.current_tool == 'bucket':
            plugin = self.plugins.get('bucket')
            if plugin:
                plugin.draw(self.canvas, event.x, event.y, self.brush_size.get(), self.color_var.get())
    def save_state(self):
        # 保存当前画布和PIL图像状态
        # 保存canvas所有item id
        items = self.canvas.find_all()
        # 保存PIL图像
        pil_image = None
        if 'bucket' in self.plugins:
            bucket = self.plugins['bucket']
            if bucket.image:
                pil_image = bucket.image.copy()
        self.undo_stack.append((items, pil_image))

    def undo(self):
        if not self.undo_stack:
            return
        items, pil_image = self.undo_stack.pop()
        # 清空画布
        self.canvas.delete('all')
        # 重新绘制所有item
        for item in items:
            # 这里简单恢复，实际可扩展为保存item属性
            pass
        # 恢复PIL图像
        if 'bucket' in self.plugins and pil_image:
            bucket = self.plugins['bucket']
            bucket.image = pil_image
            bucket.update_canvas()

    def on_move(self, event):
        if self.last_x is not None and self.last_y is not None:
            plugin = self.plugins.get(self.current_tool)
            if plugin:
                # 传递笔刷大小和颜色参数
                if self.current_tool == 'pen':
                    plugin.draw(self.canvas, self.last_x, self.last_y, event.x, event.y, self.brush_size.get(), self.color_var.get())
                    # 同步到油桶PIL画布
                    if 'bucket' in self.plugins:
                        bucket = self.plugins['bucket']
                        if bucket.image:
                            from PIL import ImageDraw
                            draw = ImageDraw.Draw(bucket.image)
                            draw.line([(self.last_x, self.last_y), (event.x, event.y)], fill=bucket._hex_to_rgb(self.color_var.get()), width=self.brush_size.get())
                            bucket.update_canvas()
                elif self.current_tool == 'eraser':
                    plugin.draw(self.canvas, self.last_x, self.last_y, event.x, event.y, self.brush_size.get())
                    # 同步到油桶PIL画布（橡皮为白色）
                    if 'bucket' in self.plugins:
                        bucket = self.plugins['bucket']
                        if bucket.image:
                            from PIL import ImageDraw
                            draw = ImageDraw.Draw(bucket.image)
                            draw.line([(self.last_x, self.last_y), (event.x, event.y)], fill=(255,255,255), width=self.brush_size.get())
                            bucket.update_canvas()
        self.last_x, self.last_y = event.x, event.y

    def on_button_release(self, event):
        self.last_x, self.last_y = None, None

if __name__ == '__main__':
    app = DrawBoard()
    app.mainloop()
