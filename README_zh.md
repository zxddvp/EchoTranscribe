# EchoTranscribe

## 介绍

**EchoTranscribe** 是一个强大的跨平台工具，旨在从任何视频文件中提取音频并转录为文本。它利用了 PyQt 提供的无缝图形界面和 Whisper 的尖端语音识别能力，使得在多个平台上将视频内容转换为文本变得简单易行。

## 功能

- **多平台支持**：在 Windows、macOS 和 Linux 上轻松运行 EchoTranscribe。
- **音频提取**：使用 FFmpeg 从任何视频文件中提取高质量音频。
- **高级语音识别**：使用 Whisper 的尖端模型将提取的音频转换为文本。
- **用户友好界面**：使用 PyQt 构建，提供直观和流畅的用户体验。
- **实时进度**：实时监控提取和转录过程。
- **文本导出**：轻松保存转录的文本以供进一步使用。

## 安装

### 前提条件

- **Python 3.8+**
- **FFmpeg**（确保 FFmpeg 已安装并添加到系统路径中）
- **PyQt5**
- **Whisper**
- **其他依赖项**：请参阅 `requirements.txt`

### 设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/zxddvp/EchoTranscribe.git
   cd EchoTranscribe
   ```

2. 安装所需的 Python 包：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用程序：
   ```bash
   python main.py
   ```

## 用法

1. 打开应用程序。
2. 从本地存储中选择一个视频文件。
3. 点击“开始”提取音频并转录为文本。
4. 在应用程序中直接查看进度和最终输出。
5. 如有需要，导出转录的文本。

## 贡献

我们欢迎贡献！如果您有想法或改进意见，请随时 fork 此仓库，进行修改并提交 pull request。

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- 感谢 **Whisper** 提供强大的语音识别模型。
- 感谢 **PyQt** 提供灵活且强大的 GUI 框架。
- 感谢 **FFmpeg** 提供在多媒体处理中的必备工具。
