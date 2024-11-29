"""
EchoTranscribe - 视频音频转录工具
这是应用程序的主入口文件，负责初始化GUI应用程序和日志系统。
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import setup_logging

def main():
    """
    应用程序的主入口函数
    - 初始化日志系统
    - 创建并启动PyQt5应用程序
    - 显示主窗口
    """
    # 设置日志
    setup_logging()

    # 启动应用程序
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
