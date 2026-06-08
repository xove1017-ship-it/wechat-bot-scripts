#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信消息发送脚本
支持发送消息给指定联系人或群聊
"""

import pyautogui
import time
import sys
import os

# 添加工具路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.window import find_wechat_window, activate_wechat, get_search_box_pos, get_input_box_pos
from utils.clipboard import set_clipboard

# 安全设置
pyautogui.FAILSAFE = True


def send_message(contact: str, message: str, wait_after_search: float = 2.0) -> bool:
    """
    发送消息给指定联系人
    
    Args:
        contact: 联系人名称或群聊名称
        message: 要发送的消息内容
        wait_after_search: 搜索后等待时间（群聊需要更长）
    
    Returns:
        bool: 是否发送成功
    """
    # 1. 找到微信窗口
    w = find_wechat_window()
    if not w:
        print("❌ 未找到微信窗口")
        return False
    
    # 2. 激活窗口
    if not activate_wechat(w):
        print("❌ 激活窗口失败")
        return False
    
    # 3. 点击搜索框
    search_x, search_y = get_search_box_pos(w)
    pyautogui.click(search_x, search_y)
    time.sleep(0.3)
    
    # 4. 搜索联系人
    set_clipboard(contact)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 5. 选择搜索结果
    # 注意：群聊需要用鼠标点击搜索结果，不能用 Tab/Enter
    pyautogui.press('enter')
    time.sleep(wait_after_search)
    
    # 6. 点击输入框
    input_x, input_y = get_input_box_pos(w)
    pyautogui.click(input_x, input_y)
    time.sleep(0.3)
    
    # 7. 输入消息
    set_clipboard(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    
    # 8. 发送
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print(f"✅ 消息已发送给 [{contact}]: {message[:30]}...")
    return True


def send_to_group(group_name: str, message: str) -> bool:
    """
    发送消息到群聊
    
    群聊特殊处理：
    - 搜索后需要更长等待时间
    - 搜索结果需要用鼠标点击
    """
    # 1. 找到微信窗口
    w = find_wechat_window()
    if not w:
        print("❌ 未找到微信窗口")
        return False
    
    # 2. 激活窗口
    if not activate_wechat(w):
        print("❌ 激活窗口失败")
        return False
    
    # 3. 点击搜索框
    search_x, search_y = get_search_box_pos(w)
    pyautogui.click(search_x, search_y)
    time.sleep(0.3)
    
    # 4. 搜索群聊
    set_clipboard(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    
    # 5. 用鼠标点击搜索结果（群聊不能用键盘选择）
    # 搜索结果通常在搜索框下方 55 像素处
    result_y = search_y + 55
    pyautogui.click(search_x, result_y)
    time.sleep(3)  # 等待群聊加载和滑动动画
    
    # 6. 点击输入框
    input_x, input_y = get_input_box_pos(w)
    pyautogui.click(input_x, input_y)
    time.sleep(0.3)
    
    # 7. 输入消息
    set_clipboard(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    
    # 8. 发送
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print(f"✅ 消息已发送到群 [{group_name}]: {message[:30]}...")
    return True


def main():
    """主函数 - 示例用法"""
    import argparse
    
    parser = argparse.ArgumentParser(description='微信消息发送')
    parser.add_argument('--contact', '-c', required=True, help='联系人或群聊名称')
    parser.add_argument('--message', '-m', required=True, help='要发送的消息')
    parser.add_argument('--group', '-g', action='store_true', help='是否为群聊')
    
    args = parser.parse_args()
    
    if args.group:
        success = send_to_group(args.contact, args.message)
    else:
        success = send_message(args.contact, args.message)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
