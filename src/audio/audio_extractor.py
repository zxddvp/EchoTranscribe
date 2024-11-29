"""
音频提取模块
负责从视频文件中提取音频轨道，并将其保存为WAV格式。
使用ffmpeg作为底层音频处理工具。
"""

import subprocess
import os
import logging
from datetime import datetime
import shutil
from src.utils.config import (
    TEMP_DIR, MAX_FILE_SIZE_MB, SUPPORTED_VIDEO_FORMATS,
    SUPPORTED_AUDIO_FORMATS, AUDIO_SAMPLE_RATE, AUDIO_CHANNELS
)

class AudioExtractionError(Exception):
    """音频提取相关的异常"""
    pass

def validate_file(file_path):
    """
    验证输入文件的有效性
    
    Args:
        file_path (str): 输入文件路径
        
    Raises:
        AudioExtractionError: 当文件无效时抛出
    """
    if not os.path.exists(file_path):
        raise AudioExtractionError(f"文件不存在: {file_path}")
        
    # 检查文件大小
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise AudioExtractionError(f"文件大小超过限制 ({file_size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB)")
        
    # 检查文件格式
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_VIDEO_FORMATS and ext not in SUPPORTED_AUDIO_FORMATS:
        raise AudioExtractionError(f"不支持的文件格式: {ext}")
        
    # 检查文件权限
    if not os.access(file_path, os.R_OK):
        raise AudioExtractionError(f"没有文件的读取权限: {file_path}")

def cleanup_old_files():
    """清理临时目录中的旧文件"""
    try:
        for file in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file)
            if os.path.isfile(file_path):
                # 删除超过24小时的文件
                file_age = datetime.now().timestamp() - os.path.getctime(file_path)
                if file_age > 24 * 3600:  # 24小时
                    os.remove(file_path)
    except Exception as e:
        logging.warning(f"清理临时文件时出错: {str(e)}")

def extract_audio(video_file):
    """
    从视频文件中提取音频轨道
    
    Args:
        video_file (str): 输入视频文件的路径
        
    Returns:
        str: 输出的音频文件路径
        
    Raises:
        AudioExtractionError: 当音频提取失败时抛出
    """
    try:
        # 验证输入文件
        validate_file(video_file)
        
        # 清理旧文件
        cleanup_old_files()
        
        # 使用时间戳生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_audio_file = os.path.join(TEMP_DIR, f"audio_{timestamp}.wav")
        
        # 构建ffmpeg命令
        command = [
            'ffmpeg',
            '-i', video_file,
            '-vn',  # 不处理视频
            '-ar', str(AUDIO_SAMPLE_RATE),  # 设置采样率
            '-ac', str(AUDIO_CHANNELS),  # 设置声道数
            '-q:a', '0',  # 最高质量
            output_audio_file
        ]
        
        # 执行命令
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise AudioExtractionError(f"FFmpeg错误: {result.stderr}")
            
        logging.info(f"已从 {video_file} 提取音频到 {output_audio_file}")
        return output_audio_file
        
    except subprocess.SubprocessError as e:
        raise AudioExtractionError(f"FFmpeg执行失败: {str(e)}")
    except Exception as e:
        if isinstance(e, AudioExtractionError):
            raise
        raise AudioExtractionError(f"音频提取失败: {str(e)}")
        
def __del__():
    """清理临时文件"""
    try:
        cleanup_old_files()
    except:
        pass
