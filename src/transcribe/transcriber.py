"""
音频转录模块
使用OpenAI的Whisper模型将音频文件转录为文本。
支持多种语言的自动识别和转录。
"""

import whisper
import logging
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utils.config import TEMP_DIR, WHISPER_MODEL, SUPPORTED_LANGUAGES

class TranscriptionError(Exception):
    """转录相关的异常"""
    pass

class Transcriber:
    """音频转录器类"""
    
    def __init__(self):
        """初始化转录器"""
        try:
            self.model = whisper.load_model(WHISPER_MODEL)
            self._model_loaded = True
        except Exception as e:
            self._model_loaded = False
            raise TranscriptionError(f"无法加载Whisper模型: {str(e)}")
            
    def transcribe_single(self, audio_file, language=None):
        """
        转录单个音频文件
        
        Args:
            audio_file (str): 音频文件路径
            language (str, optional): 音频语言代码
            
        Returns:
            dict: 包含转录结果的字典
            
        Raises:
            TranscriptionError: 转录失败时抛出
        """
        try:
            # 验证文件存在
            if not os.path.exists(audio_file):
                raise TranscriptionError(f"音频文件不存在: {audio_file}")
                
            # 执行转录
            options = {"language": language} if language in SUPPORTED_LANGUAGES else {}
            result = self.model.transcribe(audio_file, **options)
            
            # 准备输出结果
            output = {
                "text": result["text"],
                "language": result.get("language", "unknown"),
                "segments": result.get("segments", []),
                "audio_file": audio_file,
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存转录结果
            self._save_transcription(output, audio_file)
            
            return output
            
        except Exception as e:
            if isinstance(e, TranscriptionError):
                raise
            raise TranscriptionError(f"转录失败: {str(e)}")
            
    def transcribe_batch(self, audio_files, max_workers=None, language=None):
        """
        并行转录多个音频文件
        
        Args:
            audio_files (list): 音频文件路径列表
            max_workers (int, optional): 最大并行工作线程数
            language (str, optional): 音频语言代码
            
        Returns:
            list: 转录结果列表
            
        Raises:
            TranscriptionError: 当任何文件转录失败时抛出
        """
        results = []
        errors = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self.transcribe_single, audio_file, language): audio_file
                for audio_file in audio_files
            }
            
            for future in as_completed(future_to_file):
                audio_file = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    errors.append(f"文件 {audio_file} 转录失败: {str(e)}")
                    
        if errors:
            raise TranscriptionError("\n".join(errors))
            
        return results
        
    def _save_transcription(self, result, audio_file):
        """保存转录结果到文件"""
        try:
            # 创建转录结果目录
            output_dir = os.path.join(TEMP_DIR, "transcriptions")
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_transcription.json")
            
            # 保存结果
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                
            logging.info(f"转录结果已保存到: {output_file}")
            
        except Exception as e:
            logging.error(f"保存转录结果失败: {str(e)}")
            
def transcribe_audio(audio_file, language=None):
    """
    转录音频文件的便捷函数
    
    Args:
        audio_file (str): 音频文件路径
        language (str, optional): 音频语言代码
        
    Returns:
        str: 转录文本
        
    Raises:
        TranscriptionError: 转录失败时抛出
    """
    transcriber = Transcriber()
    result = transcriber.transcribe_single(audio_file, language)
    return result["text"]
