"""
全局配置模块
管理应用程序的全局设置和常量
"""

import os
import tempfile

# 文件和目录配置
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'echotranscribe')
MAX_FILE_SIZE_MB = 500  # 最大允许的文件大小（MB）
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
SUPPORTED_AUDIO_FORMATS = ['.wav', '.mp3', '.aac', '.m4a', '.flac']

# 音频转换配置
AUDIO_SAMPLE_RATE = 16000
AUDIO_FORMAT = 'wav'
AUDIO_CHANNELS = 1

# 并行处理配置
MAX_WORKERS = 4  # 最大并行处理线程数

# Whisper模型配置
WHISPER_MODEL = 'base'
SUPPORTED_LANGUAGES = ['zh', 'en', 'ja', 'ko', 'fr', 'de', 'es', 'ru']

# 创建必要的目录
os.makedirs(TEMP_DIR, exist_ok=True) 