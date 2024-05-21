<br>

<div align=center>
<h1 aligh="center">
<img src="icon.png" width="100"> 

Smartinput
</h1>

[![License][License-image]][License-url]
[![Releases][Releases-image]][Releases-url]
[![Commit][GitHub-last-commit]][Commit-url]
[![PR][PRs-image]][PRs-url]

[License-image]: https://img.shields.io/github/license/Menghuan1918/Smartinput
[Releases-image]: https://img.shields.io/github/v/release/Menghuan1918/Smartinput
[GitHub-last-commit]: https://img.shields.io/github/last-commit/Menghuan1918/Smartinput
[PRs-image]: https://img.shields.io/badge/PRs-welcome-pink?style=flat-square

[License-url]: https://github.com/Menghuan1918/Smartinput/blob/master/LICENSE
[Releases-url]: https://github.com/Menghuan1918/Smartinput/releases
[Commit-url]: https://github.com/Menghuan1918/Smartinput/commits/master/
[PRs-url]: https://github.com/Menghuan1918/Smartinput/pulls
</div>
<br>

> We're rolling out the macOS app to Plus users starting today, and we will make it more broadly available in the coming weeks. We also plan to launch a Windows version later this year.

Here's a paragraph from GPT-4o's introductory page about the desktop client, without Linux anything of course... So I decided to try to make one myself! And make it have better support for more models. Its intended to run on **native models**, but is also compatible with the online API.

🗺️ ENGLISH | [简体中文](README_CN.md)

> [!NOTE]
> Unless otherwise noted, all videos or images shown are on **3060M** mobile graphics cards running **llama3-8B** on ollama, and the videos are not **accelerated or multiplied**!

# What's new
- New showtext window, now able to stream output/edit final text(show in gif here:)
  
  ![New_window](https://github.com/Menghuan1918/Smartinput/assets/122662527/0704fea4-19c4-4716-a953-cbeca4dcb653)

- Windows support(⚠️ Note: Windows currently only supports listening to the clipboard)
  
  ![Win](https://github.com/Menghuan1918/Smartinput/assets/122662527/1060aae1-9a2a-480d-b679-7ded34f1376b)

- Listening Mode Selection

  ![Select](https://github.com/Menghuan1918/Smartinput/assets/122662527/44da57e6-fea5-42bd-b677-e5b667784ea9)
- Processing mode selection:Direct processing/pop-up secondary confirmation
  
  ![Go](https://github.com/Menghuan1918/Smartinput/assets/122662527/a6823094-0da4-4558-8630-d9dd178f502b)

# Functions
Sit-click window to drag and drop, middle-click window to copy content, right-click window to hide, tray menu for mode switching.

Currently only global underline word fetching and translation or explanation is implemented, see the video:

[Vedio!](https://github.com/Menghuan1918/Smartinput/assets/122662527/2f1c85ad-e6f1-448c-bcb9-9b6cc26cb161)

<span><img src="https://github.com/Menghuan1918/Smartinput/assets/122662527/197062eb-9980-4b87-acce-0f94cf690d9d" alt="tary"> <img src="https://github.com/Menghuan1918/Smartinput/assets/122662527/497b8878-fcd2-43a4-bb1b-6406f650a366" alt="Traslate"> <img src="https://github.com/Menghuan1918/Smartinput/assets/122662527/cf835c41-922e-45e6-baae-f869ee672d19" alt="Coding!"></span>

# Models Supported
Multiple models are supported! As long as the model's API is compatible with the OpenAI format it will work, just change `APIKEY`, `llm_model`, `endpoint` in the config file. Including but not limited to (the bolded ones are verified, although the others are theoretically fine):
- **Ollama**
- **Groq**
- **Deepseek**
- Openai
- Yi Models
- Zhipu
- Moonshot

Of course, those accessed using [one-api](https://github.com/songquanpeng/one-api) are fully supported.

# Configuration
By default the configuration file is saved in `$HOME/.config/Smartinput/config`.
- APIKEY: secret key, empty by default.
- llm_model: model name, default
- max_tokens: the maximum tokens for a single reply from the model, default 4000
- temperature: temperature of the model, default 0.3
- endpoint: model request
- proxies: not implemented yet, just put it here.
- timeout: timeout of the request, default is 60 seconds.
- max_retry: maximum retries, default is 3.
- font: the font used, default is DejaVu Sans
- font_size: font size, default is 12.
- lang: the detected language, it will be recognised automatically when you start it for the first time. You can also change it after.**The software interface and answer target language will follow this setting.**

# Use
> [!IMPORTANT]
> Since `xclip` is used, it does not support reading selected text in **wayland** windows! Also please install `xclip` before using it:
> 
> Ubuntu/Debian: `sudo apt install xclip`
> 
> Arch/Manjaro:`sudo pacman -S xclip`.

Download the packaged binary from [releases](https://github.com/Menghuan1918/Smartinput/releases).The configuration file is automatically stored in `$HOME/.config/Smartinput/config` after the first run

## Linux
Unzip and run `Refresh_Desktopfile.sh`, it will be automatically installed in the system desktop

## Windows
Unzip and run `main.exe`

Or you can clone the source code to use it, please refer to:

```bash
conda create -n smart_input python=3.12
conda activate smart_input
pip install -r requirements.txt
python main.py
```

# TODO
- [x] Improve smoothness
- [ ] Allow customised prompts
- [ ] Shortcut Binding
- [ ] Wayland support
- [ ] Completing the further Q&A interface
- [ ] Reading files using RAGs


# Reference and Learning
The code references many designs from other great projects that have inspired me as well as given me ideas, thanks to the selfless developers! In no particular order:

https://github.com/bianjp/popup-dict

https://github.com/binary-husky/gpt_academic
