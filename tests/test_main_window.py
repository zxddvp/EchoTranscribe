"""
主窗口模块的单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
import sys
from src.ui.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """在所有测试开始前创建QApplication实例"""
        cls.app = QApplication(sys.argv)
        
    def setUp(self):
        """每个测试前的准备工作"""
        self.window = MainWindow()
        
    def test_window_initialization(self):
        """测试窗口初始化"""
        # 验证窗口标题和大小
        self.assertIsNotNone(self.window.windowTitle())
        self.assertEqual(self.window.geometry().width(), 600)
        self.assertEqual(self.window.geometry().height(), 500)
        
        # 验证UI组件
        self.assertIsNotNone(self.window.label)
        self.assertIsNotNone(self.window.button)
        self.assertIsNotNone(self.window.progress_bar)
        self.assertIsNotNone(self.window.transcription_output)
        self.assertIsNotNone(self.window.language_selector)
        
    def test_language_change(self):
        """测试语言切换功能"""
        # 测试切换到繁体中文
        self.window.change_language(1)
        self.assertEqual(self.window.translator.language, "zh_TW")
        
        # 测试切换到英文
        self.window.change_language(2)
        self.assertEqual(self.window.translator.language, "en")
        
        # 测试切换回简体中文
        self.window.change_language(0)
        self.assertEqual(self.window.translator.language, "zh")
        
    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileNames')
    @patch('src.audio.audio_extractor.extract_audio')
    @patch('src.transcribe.transcriber.transcribe_audio')
    def test_browse_files_success(self, mock_transcribe, mock_extract, mock_dialog):
        """测试文件处理成功的情况"""
        # 模拟文件选择
        mock_dialog.return_value = (["test1.mp4", "test2.mp4"], None)
        # 模拟音频提取
        mock_extract.return_value = "test_audio.wav"
        # 模拟转录
        mock_transcribe.return_value = "测试转录结果"
        
        # 执行文件处理
        self.window.browse_files()
        
        # 验证结果
        self.assertEqual(mock_extract.call_count, 2)
        self.assertEqual(mock_transcribe.call_count, 2)
        self.assertEqual(self.window.progress_bar.value(), 100)
        self.assertEqual(self.window.transcription_output.toPlainText(), "测试转录结果")
        
    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileNames')
    @patch('src.audio.audio_extractor.extract_audio')
    def test_browse_files_extraction_failure(self, mock_extract, mock_dialog):
        """测试音频提取失败的情况"""
        # 模拟文件选择
        mock_dialog.return_value = (["test.mp4"], None)
        # 模拟音频提取失败
        mock_extract.side_effect = Exception("Extraction failed")
        
        # 执行文件处理
        self.window.browse_files()
        
        # 验证错误处理
        self.assertEqual(self.window.transcription_output.toPlainText(), "")
        
    def test_progress_bar(self):
        """测试进度条功能"""
        # 测试初始值
        self.assertEqual(self.window.progress_bar.value(), 0)
        
        # 测试设置进度
        self.window.progress_bar.setValue(50)
        self.assertEqual(self.window.progress_bar.value(), 50)
        
        # 测试完成状态
        self.window.progress_bar.setValue(100)
        self.assertEqual(self.window.progress_bar.value(), 100)
        
    @classmethod
    def tearDownClass(cls):
        """在所有测试结束后清理QApplication"""
        cls.app.quit() 