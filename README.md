# Smartinput
(中文 | [English](README_en.md))

目前处于起步阶段，应该可在 linux/win 平台可用。
旨在使用 pyqt6 编写一个 gui 界面，(包括但不限于 openai api）对多种输入（文本，语言，图像）进行识别并进行操作（输出文本，语言，图像）。
# 0.0.2B 更新

翻译改为首先使用 [PyDeepLX](https://github.com/OwO-Network/PyDeepLX)，如过不成功，再使用 [py-googletrans](https://github.com/ssut/py-googletrans) 翻译，如还是不成功，使用 [translate-python ](https://github.com/terryyin/translate-python/tree/master) 进行翻译。

# 0.0.2A 更新

改为使用 [PyDeepLX](https://github.com/OwO-Network/PyDeepLX) 进行翻译, 现在自动读取剪切板翻译更加好用了, 你可以在 main 窗口的菜单中将其打开.

# 0.0.2 更新
添加使用 tkinter 编写的输入界面(点击 clear 按钮上方的按钮调出)，可解决 <b> 某些环境下 linux </b> 无法使用 fcitx5 的问题。注意，这个输入界面是通过剪切板与主程序通讯的，因此打开的同时会自动打开剪切板监控。预计下一版会改进这个问题, 因此 windows 不能用是很正常的.

![tkinter](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Input.png?raw=true)

添加 ChatGPT3.5 的支持，可实现对话功能, 使用官方 api 实现，需要自行注册 openai 账号并获取 api key。

![chat](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/chatGPT.png?raw=true)

当输入为程序时，反应为解释程序的功能，如下图所示：

![program](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Gpt_ans.png?raw=true)

当输入格式为 “某种语言或者其缩写” ： “所需翻译的文本” 时，反应为翻译功能，如下图所示：

![trasns_GPT](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/GPT_trans.png?raw=true)

以上均为通过 GPT_prompt.md 中的 prompt 实现，可自行修改。例如，你可以自行修改为翻译为某种特定语言，配合自动读取剪切板功能，可以实现使用的翻译。
# 0.0.1 更新 
完成了一个简单的将任意语言翻译为简体中文的 GUI 页面，支持剪切板实时监控自动翻译（默认关闭）。

![Check the Clip](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/clip_show.gif?raw=true)

# 已知问题

如在调用 openai 的 api 出错时，会导致整个程序崩溃，这个问题会在下一版中修复（大概）。

gpt 历史记录功能不能显示除英文外的其他语言。

# 其他 
已完成的 api 调用：图片至文本（基于 pytesseract），gpt3.5 api 请求，openai 语言识别 api 请求，DALLE api 调用, 翻译 api 请求。纯新手，欢迎指正。
