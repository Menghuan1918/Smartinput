# Smartinput
目前处于开始阶段，仅对不同api应用进行组合，应该可在linux/win平台可用。
旨在使用pyqt6编写一个gui界面，基于openai api对多种输入（文本，语言，图像）进行识别并进行操作（输出文本，语言，图像）。

Currently in the beginning stage, only a combination of different api applications, should be available in linux/win platform
Aim to write a gui interface using pyqt6 to recognize and manipulate multiple inputs (text, language, image) based on the openai api (output text, language, image).

# 0.0.1更新 / 0.0.1 update
完成了一个简单的将任意语言翻译为简体中文的GUI页面，支持剪切板实时监控自动翻译（默认开启，可关闭）。

Completed a simple GUI page for translating any language into Simplified Chinese, with support for clipboard real-time monitoring of automatic translation (enabled by default, can be turned off).

![Check the Clip](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/clip_show.gif?raw=true)

下一步：添加更多支持的目标语言，让gpt3.5根据输入内容自动识别操作：翻译/Gpt3.5生成文本/图像识别（预计使用bing api）。

Next step: add more supported target languages to allow gpt3.5 to automatically recognize operations based on input: translation / Gpt3.5 generated text / image recognition (expected to use bing api).

# About translation target language

If you want to change the target language, change 'zh' to your target language (expect to add the option in the next version)

![change the target language](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Change_lang.png?raw=true)

# 其他 / Other
已完成的api调用：图片至文本（基于pytesseract），gpt3.5 api请求，openai语言识别api请求，DALLE api调用,翻译api请求。纯新手，欢迎指正。

Completed api calls: image to text (based on pytesseract), gpt3.5 api request, openai language recognition api request, DALLE api call, translation api request. Pure novice, welcome to correct me.
