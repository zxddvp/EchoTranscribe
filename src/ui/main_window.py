"""
主窗口模块
实现应用程序的图形用户界面，包括文件选择、语言切换、进度显示等功能。
"""

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QProgressBar, QComboBox, QTextEdit, QMessageBox,
    QHBoxLayout, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from src.audio.audio_extractor import extract_audio, AudioExtractionError
from src.transcribe.transcriber import Transcriber, TranscriptionError
from src.utils.translator import Translator
from src.utils.config import (
    SUPPORTED_VIDEO_FORMATS, SUPPORTED_AUDIO_FORMATS,
    MAX_WORKERS, SUPPORTED_LANGUAGES
)
import logging
import os

class TranscriptionWorker(QThread):
    """后台转录工作线程"""
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    result = pyqtSignal(list)
    
    def __init__(self, files, language=None, parent=None):
        super().__init__(parent)
        self.files = files
        self.language = language
        
    def run(self):
        try:
            transcriber = Transcriber()
            results = transcriber.transcribe_batch(
                self.files,
                max_workers=MAX_WORKERS,
                language=self.language
            )
            self.result.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    """
    应用程序的主窗口类
    
    提供以下功能：
    - 视频文件选择
    - 音频提取和转录
    - 多语言界面切换
    - 转录结果显示
    - 进度显示
    - 并行处理控制
    - 结果保存
    """
    
    def __init__(self):
        """初始化主窗口及其UI组件"""
        super().__init__()
        self.translator = Translator(language="zh")
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(self.translator.translate("window_title"))
        self.setGeometry(200, 200, 800, 600)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 顶部控制区
        top_layout = QHBoxLayout()
        
        # 语言选择器
        self.language_selector = QComboBox()
        self.language_selector.addItems(["简体中文", "繁體中文", "English"])
        self.language_selector.currentIndexChanged.connect(self.change_language)
        top_layout.addWidget(self.language_selector)
        
        # 音频语言选择
        self.audio_language_selector = QComboBox()
        self.audio_language_selector.addItems(["自动检测"] + SUPPORTED_LANGUAGES)
        top_layout.addWidget(QLabel(self.translator.translate("audio_language")))
        top_layout.addWidget(self.audio_language_selector)
        
        main_layout.addLayout(top_layout)
        
        # 文件选择区域
        self.label = QLabel(self.translator.translate("select_video"))
        self.button = QPushButton(self.translator.translate("browse"))
        self.button.clicked.connect(self.browse_files)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.button)
        
        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.progress_bar)
        
        # 转录结果显示
        self.transcription_output = QTextEdit()
        self.transcription_output.setReadOnly(True)
        main_layout.addWidget(self.transcription_output)
        
        # 底部控制区
        bottom_layout = QHBoxLayout()
        
        # 保存结果按钮
        self.save_button = QPushButton(self.translator.translate("save_result"))
        self.save_button.clicked.connect(self.save_result)
        self.save_button.setEnabled(False)
        bottom_layout.addWidget(self.save_button)
        
        main_layout.addLayout(bottom_layout)
        
        # 设置主窗口部件
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
    def change_language(self, index):
        """切换界面语言"""
        languages = ["zh", "zh_TW", "en"]
        self.translator.set_language(languages[index])
        self.update_ui_texts()
        
    def update_ui_texts(self):
        """更新界面文本"""
        self.setWindowTitle(self.translator.translate("window_title"))
        self.label.setText(self.translator.translate("select_video"))
        self.button.setText(self.translator.translate("browse"))
        self.save_button.setText(self.translator.translate("save_result"))
        
    def browse_files(self):
        """处理文件选择和处理逻辑"""
        # 构建文件过滤器
        filters = []
        filters.extend(f"*{fmt}" for fmt in SUPPORTED_VIDEO_FORMATS)
        filters.extend(f"*{fmt}" for fmt in SUPPORTED_AUDIO_FORMATS)
        filter_str = f"Media Files ({' '.join(filters)})"
        
        # 打开文件选择对话框
        file_names, _ = QFileDialog.getOpenFileNames(
            self,
            self.translator.translate("select_files"),
            "",
            filter_str
        )
        
        if not file_names:
            return
            
        # 准备音频文件列表
        audio_files = []
        self.progress_bar.setValue(0)
        
        try:
            # 提取音频
            for idx, file_name in enumerate(file_names):
                try:
                    self.label.setText(
                        self.translator.translate(
                            "processing_file",
                            idx=idx + 1,
                            total=len(file_names)
                        )
                    )
                    audio_file = extract_audio(file_name)
                    audio_files.append(audio_file)
                    progress = int((idx + 1) / len(file_names) * 50)
                    self.progress_bar.setValue(progress)
                    
                except AudioExtractionError as e:
                    QMessageBox.warning(
                        self,
                        self.translator.translate("error"),
                        str(e)
                    )
                    return
                    
            # 开始转录
            self.label.setText(self.translator.translate("transcribing"))
            
            # 获取选择的音频语言
            language = None
            if self.audio_language_selector.currentIndex() > 0:
                language = SUPPORTED_LANGUAGES[self.audio_language_selector.currentIndex() - 1]
                
            # 创建并启动转录线程
            self.worker = TranscriptionWorker(audio_files, language)
            self.worker.progress.connect(self.update_transcription_progress)
            self.worker.error.connect(self.handle_transcription_error)
            self.worker.result.connect(self.handle_transcription_result)
            self.worker.start()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                self.translator.translate("error"),
                str(e)
            )
            self.progress_bar.setValue(0)
            self.label.setText(self.translator.translate("select_video"))
            
    def update_transcription_progress(self, value):
        """更新转录进度"""
        self.progress_bar.setValue(50 + value // 2)
        
    def handle_transcription_error(self, error_msg):
        """处理转录错误"""
        QMessageBox.critical(
            self,
            self.translator.translate("error"),
            error_msg
        )
        self.progress_bar.setValue(0)
        self.label.setText(self.translator.translate("select_video"))
        
    def handle_transcription_result(self, results):
        """处理转录结果"""
        # 显示转录文本
        combined_text = "\n\n".join(
            f"[{os.path.basename(r['audio_file'])}]\n{r['text']}"
            for r in results
        )
        self.transcription_output.setPlainText(combined_text)
        
        # 更新界面状态
        self.progress_bar.setValue(100)
        self.label.setText(self.translator.translate("transcription_complete"))
        self.save_button.setEnabled(True)
        
    def save_result(self):
        """保存转录结果"""
        if not self.transcription_output.toPlainText():
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            self.translator.translate("save_result"),
            "",
            "Text Files (*.txt);;JSON Files (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.transcription_output.toPlainText())
                QMessageBox.information(
                    self,
                    self.translator.translate("success"),
                    self.translator.translate("save_success")
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    self.translator.translate("error"),
                    str(e)
                )
