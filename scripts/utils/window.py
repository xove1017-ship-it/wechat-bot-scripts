#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信窗口管理工具
"""

import pygetwindow as gw
import time
from typing import Optional


def find_wechat_window() -> Optional[gw.Win32Window]:
    """找到微信窗口"""
    try:
        windows = gw.getWindowsWithTitle('微信')
        if windows:
            return windows[0]
    except Exception as e:
        print(f"查找微信窗口失败: {e}")
    return None


def activate_wechat(window: gw.Win32Window) -> bool:
    """激活微信窗口"""
    try:
        window.activate()
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"激活窗口失败: {e}")
        return False


def get_window_bounds(window: gw.Win32Window) -> dict:
    """获取窗口边界信息"""
    return {
        'left': window.left,
        'top': window.top,
        'width': window.width,
        'height': window.height,
        'right': window.right,
        'bottom': window.bottom
    }


def is_window_valid(window: gw.Win32Window) -> bool:
    """检查窗口是否有效"""
    try:
        return window.isActive or not window.isMinimized
    except:
        return False


# 坐标计算辅助函数
def get_search_box_pos(window: gw.Win32Window) -> tuple:
    """获取搜索框位置"""
    return (window.left + 200, window.top + 35)


def get_chat_area_pos(window: gw.Win32Window) -> tuple:
    """获取聊天区域位置（用于复制消息）"""
    return (window.left + window.width * 2 // 3, window.top + window.height // 2)


def get_input_box_pos(window: gw.Win32Window) -> tuple:
    """获取输入框位置"""
    return (window.left + window.width // 2 + 100, window.top + window.height - 80)


# 测试
if __name__ == "__main__":
    w = find_wechat_window()
    if w:
        print(f"找到微信窗口: {w.title}")
        print(f"位置: left={w.left}, top={w.top}, size={w.width}x{w.height}")
        print(f"搜索框: {get_search_box_pos(w)}")
        print(f"聊天区: {get_chat_area_pos(w)}")
        print(f"输入框: {get_input_box_pos(w)}")
    else:
        print("未找到微信窗口")
