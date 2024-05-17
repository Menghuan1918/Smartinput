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
> 如无特殊说明，展示的所有视频均使用**3060M**移动端显卡，在ollama上运行**llama3-8B**，并且没有**进行加速或倍速处理**！

# 功能
目前仅实现了全局划线取词并翻译或解释，请看视频，注意视频中我将程序以及目标语言都设置为了英文：

[演示视频](https://github.com/Menghuan1918/Smartinput/assets/122662527/2f1c85ad-e6f1-448c-bcb9-9b6cc26cb161)

# 支持的模型
支持多种模型！只要模型的API与OpenAI格式兼容就能用，只要更改配置文件中`APIKEY`，`llm_model`，`endpoint`就行。包括但不限于(加粗的是验证过的，虽然其他的理论上也没问题)：
- **Ollama**
- **Groq**
- **Deepseek**
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
- lang：检测的语言环境，第一次启动时会自动识别。你也可以在其后进行更改
