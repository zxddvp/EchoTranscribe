"""
音频提取模块的单元测试
"""

import unittest
import os
from unittest.mock import patch
from src.audio.audio_extractor import extract_audio

class TestAudioExtractor(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.test_video_file = "test_video.mp4"
        
    def tearDown(self):
        """测试后的清理工作"""
        # 清理测试过程中生成的音频文件
        for file in os.listdir('.'):
            if file.startswith('output_audio_') and file.endswith('.wav'):
                try:
                    os.remove(file)
                except OSError:
                    pass

    @patch('subprocess.call')
    def test_extract_audio_success(self, mock_subprocess_call):
        """测试音频提取成功的情况"""
        # 模拟subprocess.call的成功调用
        mock_subprocess_call.return_value = 0
        
        # 执行音频提取
        output_file = extract_audio(self.test_video_file)
        
        # 验证结果
        self.assertTrue(output_file.startswith('output_audio_'))
        self.assertTrue(output_file.endswith('.wav'))
        mock_subprocess_call.assert_called_once()
        
    @patch('subprocess.call')
    def test_extract_audio_failure(self, mock_subprocess_call):
        """测试音频提取失败的情况"""
        # 模拟subprocess.call的失败调用
        mock_subprocess_call.side_effect = Exception("FFmpeg error")
        
        # 验证是否抛出异常
        with self.assertRaises(Exception):
            extract_audio(self.test_video_file)
            
    def test_extract_audio_invalid_input(self):
        """测试无效输入文件的情况"""
        with self.assertRaises(Exception):
            extract_audio("nonexistent_file.mp4") 