# Smartinput
([中文](README.md) | English)

This project is currently in its initial stage and should be available on both linux and windows platforms. It aims to use PyQt6 to create a GUI interface that uses OpenAI API to recognize and manipulate various inputs such as text, language, and images, and produce output in the form of text, language, and images. Support for additional APIs may be added in the future.

# 0.0.2 Update

Add input interface written by tkinter, it can solve the problem that linux can't use fcitx5 in some environment. Note that this input interface is communicating with main program through clipboard, so it will automatically open clipboard monitor when open. Next version is expected to improve this problem.

![tkinter]()

In the 0.0.2 version update, support for ChatGPT3.5 has been added which enables conversation functionality. It uses the official API of OpenAI, so you will need to register for an OpenAI account and obtain an API key. 

When the input is a program, the system will explain the functionality of the program, as shown in the following image:

![program]()

When the input is in the format of "language abbreviation: text to be translated", the system will provide translation functionality, as shown in the following image:

![trans_GPT]()

All of these features are implemented through prompts in the GPT_prompt.md file, which can be modified as needed. For example, you can modify the prompts to translate to a specific language and use automatic clipboard reading to implement quick translation.

# 0.0.1 Update

Completed a simple GUI page for translating any language into Simplified Chinese, with support for clipboard real-time monitoring of automatic translation (enabled by default, can be turned off).

![Check the Clip](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/clip_show.gif?raw=true)

# About translation target language

If you want to change the target language, change 'zh' to your target language (expect to add the option in the next version)

![change the target language](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Change_lang.png?raw=true)

# Known issues

If there is an error in calling the api of openai, it will cause the whole program to crash, this issue will be fixed in the next version (probably).

# Other

Completed api calls: image to text (based on pytesseract), gpt3.5 api request, openai language recognition api request, DALLE api call, translation api request. Pure novice, welcome to correct me.