# Smartinput
([中文](README.md) | English)

This project is currently in its initial stage and should be available on both linux and windows platforms. It aims to use PyQt6 to create a GUI interface that uses OpenAI API to recognize and manipulate various inputs such as text, language, and images, and produce output in the form of text, language, and images. Support for additional APIs may be added in the future.

# 0.0.2A update

Changed to use [PyDeepLX](https://github.com/OwO-Network/PyDeepLX) for translation, now the auto-read clipboard translation is more useful, you can open it in the main window again.

# 0.0.2 Update

Add input interface written by tkinter (click the button above clear button to bring up), which can solve the problem that <b>linux</b> cannot use fcitx5 in some environment. Note, this input interface is communicating with main program through clipboard, so it will open clipboard monitor automatically when open. Next version is expected to improve this problem, so it is normal that windows can't use it.

![tkinter](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Input.png?raw=true)

Support for ChatGPT3.5 has been added which enables conversation functionality. It uses the official API of OpenAI, so you will need to register for an OpenAI account and obtain an API key. 

![chat](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/chatGPT.png?raw=true)

When the input is a program, the system will explain the functionality of the program, as shown in the following image:

![program](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Gpt_ans.png?raw=true)

When the input is in the format of "language abbreviation: text to be translated", the system will provide translation functionality, as shown in the following image:

![trasns_GPT](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/GPT_trans.png?raw=true)

All of these features are implemented through prompts in the GPT_prompt.md file, which can be modified as needed. For example, you can modify the prompts to translate to a specific language and use automatic clipboard reading to implement quick translation.

# 0.0.1 Update

Completed a simple GUI page for translating any language into Simplified Chinese, with support for clipboard real-time monitoring of automatic translation (enabled by default, can be turned off).

![Check the Clip](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/clip_show.gif?raw=true)

# About translation target language

If you want to change the target language, change 'zh' to your target language (expect to add the option in the next version)

![change the target language](https://github.com/Menghuan1918/Smartinput/blob/main/pictures/Change_lang.png?raw=true)

# Known issues

If there is an error in calling the api of openai, it will cause the whole program to crash, this issue will be fixed in the next version (probably).

The gpt history function cannot display languages other than English.

# Other

Completed api calls: image to text (based on pytesseract), gpt3.5 api request, openai language recognition api request, DALLE api call, translation api request. Pure novice, welcome to correct me.