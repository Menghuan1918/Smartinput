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

这是GPT-4o的介绍页面中关于桌面客户端的一段，当然没Linux任何事情...因此我决定尝试自己做一个！并且使其对更多的模型有更好的支持。其旨在在**本地模型**上运行，但是也兼容在线API。

> [!NOTE]
> 如无特殊说明，展示的所有视频或者图片均使用**3060M**移动端显卡，在ollama上运行**llama3-8B**，并且视频没有**进行加速或倍速处理**！

# 功能
坐键点击窗口拖拽，中键点击窗口复制内容，右键点击窗口隐藏，托盘菜单进行模式切换。

目前仅实现了全局划线取词并翻译或解释，请看视频，注意视频中我将程序以及目标语言都设置为了英文：

[演示视频](https://github.com/Menghuan1918/Smartinput/assets/122662527/2f1c85ad-e6f1-448c-bcb9-9b6cc26cb161)

<span><img src="https://github.com/Menghuan1918/Smartinput/assets/122662527/c3dbe68f-62d0-4ccc-8e4c-b837009217c7" alt="托盘图标"> <img src="https://github.com/Menghuan1918/Smartinput/assets/122662527/682ac9f0-3239-4c4c-966a-887295bb5525" alt="一个翻译的示范"> <img src="https://github.com/Menghuan1918/Smartinput/assets/122662527/4be09fab-429e-4c5e-a9b6-78fe7de98288" alt="代码解释"></span>

# 支持的模型
支持多种模型！只要模型的API与OpenAI格式兼容就能用，只要更改配置文件中`APIKEY`，`llm_model`，`endpoint`就行。包括但不限于(加粗的是验证过的，虽然其他的理论上也没问题)：
- **Ollama**
- **Groq**
- **Deepseek**
- OpenAI
- 零一万物
- 智谱
- 月之暗面

当然，使用[one-api](https://github.com/songquanpeng/one-api)接入的也完全支持。

# 配置
默认情况下配置文件会保存在`$HOME/.config/Smartinput/config`中。
- APIKEY：密匙，默认情况下为空。
- llm_model：模型名字，默认
- max_tokens：模型单次回复的最大token，默认4000
- temperature：模型的温度，默认为0.3
- endpoint：模型请求
- proxies：目前还没实现，只是放在这儿而已
- timeout：请求超时时长，默认60秒
- max_retry：最大重试次数，默认3次
- font：使用的字体，默认为DejaVu Sans
- font_size：使用的字号，默认为12
- lang：检测的语言环境，第一次启动时会自动识别。你也可以在其后进行更改,**软件界面和回答目标语言会遵循这个设置。**

# 使用
> [!IMPORTANT]
> 由于使用了`xclip`，其不支持读取**wayland**窗口中选中的文本！此外使用前请先安装`xclip`：
> 
> Ubuntu/Debian:`sudo apt install xclip`
> 
> Arch/Manjaro:`sudo pacman -S xclip`

从[releases](https://github.com/Menghuan1918/Smartinput/releases)下载打包好的二进制文件，将文件夹解压并运行Refresh_Desktopfile.sh，其会自动安装到桌面启动项中。卸载请运行Refresh_Desktopfile.sh uninstall并删除文件夹。
修改好配置文件程序后就能用了！

或者你也可以克隆源代码进行使用，请参照：

```bash
conda create -n smart_input python=3.12
conda activate smart_input
pip install -r requirements.txt
python main.py
```
# TODO
- [ ] 改进流畅度
- [ ] 允许自定义提示词
- [ ] 快捷键绑定
- [ ] Wayland支持
- [ ] 完成进一步问答界面
- [ ] 利用RAG对文件进行读取

# 参考与学习
代码中参考了很多其他优秀项目中的设计，是这些项目给我了灵感以及思路，感谢无私的开发者们！顺序不分先后：

https://github.com/bianjp/popup-dict

https://github.com/binary-husky/gpt_academic
