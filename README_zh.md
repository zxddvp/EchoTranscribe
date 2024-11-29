# EchoTranscribe

EchoTranscribe 是一个强大的视频音频转录工具，支持多种格式的视频和音频文件，可以将语音内容转换为文本。

## 主要特性

- 支持多种视频格式 (mp4, avi, mkv, mov, flv, wmv)
- 支持多种音频格式 (wav, mp3, aac, m4a, flac)
- 多语言界面 (简体中文、繁体中文、英文)
- 自动语言检测和指定语言转录
- 并行处理多个文件
- 转录结果保存为文本或JSON格式
- 自动清理临时文件
- 文件大小和格式验证
- 进度显示和错误处理

## 系统要求

- Python 3.8 或更高版本
- FFmpeg（用于音频提取）
- 足够的磁盘空间用于临时文件

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/EchoTranscribe.git
cd EchoTranscribe
```

2. 创建虚拟环境：
```bash
python -m venv .etvenv
source .etvenv/bin/activate  # Linux/Mac
.etvenv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 安装FFmpeg：
- Windows: 从 https://ffmpeg.org/download.html 下载并添加到系统PATH
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

## 使用方法

1. 启动程序：
```bash
python main.py
```

2. 使用界面：
   - 选择界面语言
   - 选择要转录的音频语言（可选）
   - 点击"浏览"选择文件
   - 等待处理完成
   - 保存转录结果

## 配置

可以在 `src/utils/config.py` 中修改以下配置：

- 最大文件大小限制
- 支持的文件格式
- 音频转换参数
- 并行处理线程数
- Whisper模型选择

## 注意事项

- 临时文件保存在系统临时目录，24小时后自动清理
- 大文件处理可能需要较长时间
- 建议保持足够的磁盘空间

## 开发

### 运行测试

```bash
python -m pytest tests/
```

### 项目结构

```
EchoTranscribe/
├── src/
│   ├── audio/          # 音频处理模块
│   ├── transcribe/     # 转录模块
│   ├── ui/            # 用户界面
│   ├── utils/         # 工具函数
│   └── translations/  # 翻译文件
├── tests/             # 测试文件
├── main.py           # 主程序
└── requirements.txt  # 依赖列表
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.1.0
- 添加并行处理支持
- 添加文件验证和安全检查
- 添加临时文件自动清理
- 改进错误处理
- 添加转录结果保存功能
- 支持更多音频格式

### v1.0.0
- 初始发布
