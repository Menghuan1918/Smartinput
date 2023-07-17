# Smartinput
(中文 | [English](README_en.md))

目前处于起步阶段，应该可在linux/win平台可用。
旨在使用pyqt6编写一个gui界面，(包括但不限于openai api）对多种输入（文本，语言，图像）进行识别并进行操作（输出文本，语言，图像）。

# 0.0.2A 更新

改为使用[PyDeepLX](https://github.com/OwO-Network/PyDeepLX)进行翻译,现在自动读取剪切板翻译更加好用了,你可以再main窗口中将其打开.

# 0.0.2更新
添加使用tkinter编写的输入界面(点击clear按钮上方的按钮调出)，可解决<b>某些环境下linux</b>无法使用fcitx5的问题。注意，这个输入界面是通过剪切板与主程序通讯的，因此打开的同时会自动打开剪切板监控。预计下一版会改进这个问题,因此windows不能用是很正常的.

![tkinter](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Input.png?raw=true)

添加ChatGPT3.5的支持，可实现对话功能,使用官方api实现，需要自行注册openai账号并获取api key。

![chat](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/chatGPT.png?raw=true)

当输入为程序时，反应为解释程序的功能，如下图所示：

![program](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Gpt_ans.png?raw=true)

当输入格式为 “某种语言或者其缩写” ： “所需翻译的文本” 时，反应为翻译功能，如下图所示：

![trasns_GPT](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/GPT_trans.png?raw=true)

以上均为通过GPT_prompt.md中的prompt实现，可自行修改。例如，你可以自行修改为翻译为某种特定语言，配合自动读取剪切板功能，可以实现使用的翻译。
# 0.0.1更新 
完成了一个简单的将任意语言翻译为简体中文的GUI页面，支持剪切板实时监控自动翻译（默认关闭）。

![Check the Clip](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/clip_show.gif?raw=true)

# 已知问题

如在调用openai的api出错时，会导致整个程序崩溃，这个问题会在下一版中修复（大概）。

gpt历史记录功能不能显示除英文外的其他语言。

# 其他 
已完成的api调用：图片至文本（基于pytesseract），gpt3.5 api请求，openai语言识别api请求，DALLE api调用,翻译api请求。纯新手，欢迎指正。
