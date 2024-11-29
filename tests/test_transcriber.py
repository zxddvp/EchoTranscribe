"""
音频转录模块的单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
from src.transcribe.transcriber import transcribe_audio

class TestTranscriber(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.test_audio_file = "test_audio.wav"
        self.test_transcription = "这是一段测试音频的转录文本"
        
    @patch('whisper.load_model')
    def test_transcribe_audio_success(self, mock_load_model):
        """测试音频转录成功的情况"""
        # 创建模拟的whisper模型
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {'text': self.test_transcription}
        mock_load_model.return_value = mock_model
        
        # 执行转录
        result = transcribe_audio(self.test_audio_file)
        
        # 验证结果
        self.assertEqual(result, self.test_transcription)
        mock_load_model.assert_called_once_with("base")
        mock_model.transcribe.assert_called_once_with(self.test_audio_file)
        
    @patch('whisper.load_model')
    def test_transcribe_audio_model_load_failure(self, mock_load_model):
        """测试模型加载失败的情况"""
        # 模拟模型加载失败
        mock_load_model.side_effect = Exception("Model loading failed")
        
        # 验证是否抛出异常
        with self.assertRaises(Exception):
            transcribe_audio(self.test_audio_file)
            
    @patch('whisper.load_model')
    def test_transcribe_audio_transcription_failure(self, mock_load_model):
        """测试转录过程失败的情况"""
        # 创建模拟的whisper模型，但转录失败
        mock_model = MagicMock()
        mock_model.transcribe.side_effect = Exception("Transcription failed")
        mock_load_model.return_value = mock_model
        
        # 验证是否抛出异常
        with self.assertRaises(Exception):
            transcribe_audio(self.test_audio_file)
            
    def test_transcribe_audio_invalid_input(self):
        """测试无效输入文件的情况"""
        with self.assertRaises(Exception):
            transcribe_audio("nonexistent_audio.wav") 