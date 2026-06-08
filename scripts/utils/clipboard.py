#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板工具模块
解决 pyautogui 不支持中文输入的问题
"""

import subprocess
import os
import time

# 临时文件路径
TEMP_CLIP_FILE = r'C:\temp\clip.txt'


def set_clipboard(text: str) -> bool:
    """
    设置剪贴板内容（支持中文）
    
    原理：写入临时文件 → PowerShell 读取 → 设置剪贴板
    """
    try:
        # 写入临时文件
        with open(TEMP_CLIP_FILE, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # PowerShell 设置剪贴板
        cmd = f'Get-Content "{TEMP_CLIP_FILE}" -Encoding UTF8 | Set-Clipboard'
        subprocess.run(['powershell', '-command', cmd], capture_output=True, encoding='gbk')
        
        # 清理临时文件
        time.sleep(0.1)
        try:
            os.remove(TEMP_CLIP_FILE)
        except:
            pass
        
        return True
    except Exception as e:
        print(f"设置剪贴板失败: {e}")
        return False


def get_clipboard() -> str:
    """获取剪贴板内容"""
    try:
        result = subprocess.run(
            ['powershell', '-command', 'Get-Clipboard'],
            capture_output=True,
            encoding='gbk'
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"获取剪贴板失败: {e}")
        return ""


def clear_clipboard():
    """清空剪贴板"""
    try:
        subprocess.run(
            ['powershell', '-command', 'Set-Clipboard -Value $null'],
            capture_output=True
        )
    except:
        pass


# 测试
if __name__ == "__main__":
    # 测试设置中文
    test_text = "你好，我是AI助理！✨"
    print(f"设置剪贴板: {test_text}")
    set_clipboard(test_text)
    
    # 读取验证
    result = get_clipboard()
    print(f"读取剪贴板: {result}")
    
    if result == test_text:
        print("✅ 剪贴板测试通过")
    else:
        print("❌ 剪贴板测试失败")
