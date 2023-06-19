# tk_enter.py
import tkinter as tk
import pyperclip

class InputDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        # 创建文本框
        self.text_box = tk.Text(self, height=8, width=40, font=("song ti", 16))
        self.text_box.pack()
        
        self.title("输入框:注意输入后按确认键")
        # 创建按钮
        self.button = tk.Button(self, text="确认", command=self.send_input, font=("song ti", 14, "bold"))
        self.button.pack()
        
    def send_input(self):
        self.input_text = self.text_box.get("1.0", tk.END).strip()  # 获取输入的文本内容
        pyperclip.copy(self.input_text)  # 将输入的文本复制到剪贴板
        self.destroy()  # 关闭输入框对话框

if __name__ == "__main__":
    InputDialog().mainloop()
