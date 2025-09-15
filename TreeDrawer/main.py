#!/usr/bin/env python3
"""
目录树生成器 - TreeDrawer
一个用于生成目录树状图的GUI工具

使用方法:
    python main.py

作者: Claude Code Assistant
"""

import sys
import os

# 确保能导入同目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tree_gui import main

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保 tree_gui.py 和 tree_generator.py 文件在同一目录下")
    sys.exit(1)
except Exception as e:
    print(f"程序运行出错: {e}")
    sys.exit(1)