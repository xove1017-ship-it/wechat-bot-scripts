#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动回复脚本 - 简化版
功能：监控当前聊天窗口，检测新消息并自动回复
"""

import pyautogui
import pygetwindow as gw
import time
import hashlib
import subprocess
from datetime import datetime
from collections import deque

# 配置
CHECK_INTERVAL = 3  # 检查间隔（秒）
MAX_HISTORY = 50  # 最大历史消息数

# 自动回复规则（关键词 -> 回复）
AUTO_REPLIES = {
    "你好": "你好！我是AI助理 ✨",
    "你是谁": "我是AI助理，有什么可以帮您？",
    "在吗": "在的，有什么可以帮您？",
    "在不在": "在的，有什么可以帮您？",
    "谢谢": "不客气，很高兴能帮到您！",
    "thanks": "不客气，很高兴能帮到您！",
    "拜拜": "再见！有需要随时找我～",
    "再见": "再见！有需要随时找我～",
}

# 默认回复
DEFAULT_REPLY = "你好，我是AI助理。有什么可以帮您？"


class WeChatAutoReply:
    """微信自动回复类"""
    
    def __init__(self):
        self.wechat_window = None
        self.message_history = deque(maxlen=MAX_HISTORY)
        self.last_message = ""
        self.last_reply_time = 0
        self.reply_cooldown = 5  # 同一消息回复冷却时间（秒）
        
    def find_wechat_window(self):
        """找到微信窗口"""
        try:
            windows = gw.getWindowsWithTitle('微信')
            if windows:
                self.wechat_window = windows[0]
                return True
        except Exception as e:
            print(f"[{self.get_time()}] 查找微信窗口失败: {e}")
        return False
    
    def activate_wechat(self):
        """激活微信窗口"""
        if self.wechat_window:
            try:
                self.wechat_window.activate()
                time.sleep(0.3)
                return True
            except Exception as e:
                print(f"[{self.get_time()}] 激活微信窗口失败: {e}")
        return False
    
    def get_time(self):
        """获取当前时间字符串"""
        return datetime.now().strftime("%H:%M:%S")
    
    def get_message_hash(self, message):
        """获取消息的哈希值，用于去重"""
        return hashlib.md5(message.encode('utf-8')).hexdigest()
    
    def is_message_replied(self, message):
        """检查消息是否已回复过"""
        msg_hash = self.get_message_hash(message)
        return msg_hash in self.message_history
    
    def mark_message_replied(self, message):
        """标记消息已回复"""
        msg_hash = self.get_message_hash(message)
        self.message_history.append(msg_hash)
    
    def get_clipboard_text(self):
        """获取剪贴板文本"""
        try:
            result = subprocess.run(
                ['powershell', '-command', 'Get-Clipboard'],
                capture_output=True, text=True, encoding='gbk'
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"[{self.get_time()}] 获取剪贴板失败: {e}")
            return ""
    
    def copy_last_message(self):
        """复制最后一条消息"""
        if not self.wechat_window:
            return ""
        
        try:
            # 激活微信窗口
            if not self.activate_wechat():
                return ""
            
            # 点击聊天区域（窗口中间偏右）
            x = self.wechat_window.left + self.wechat_window.width * 2 // 3
            y = self.wechat_window.top + self.wechat_window.height // 2
            
            # 点击聊天区域
            pyautogui.click(x, y)
            time.sleep(0.3)
            
            # 按 Ctrl+End 跳到最后
            pyautogui.hotkey('ctrl', 'end')
            time.sleep(0.2)
            
            # 按向上箭头选择最后一条消息
            pyautogui.press('up')
            time.sleep(0.2)
            
            # 按 Ctrl+C 复制
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            
            # 获取剪贴板内容
            message = self.get_clipboard_text()
            return message
        except Exception as e:
            print(f"[{self.get_time()}] 复制消息失败: {e}")
            return ""
    
    def detect_new_message(self):
        """检测新消息"""
        try:
            # 复制最后一条消息
            current_message = self.copy_last_message()
            
            if not current_message:
                return None
            
            # 检查是否是新消息
            if current_message != self.last_message:
                self.last_message = current_message
                return current_message
            
            return None
        except Exception as e:
            print(f"[{self.get_time()}] 检测消息失败: {e}")
            return None
    
    def get_auto_reply(self, message):
        """根据消息内容获取自动回复"""
        if not message:
            return None
        
        message_lower = message.lower().strip()
        
        # 检查是否匹配自动回复规则
        for key, reply in AUTO_REPLIES.items():
            if key in message_lower:
                return reply
        
        # 默认回复
        return DEFAULT_REPLY
    
    def click_chat_input(self):
        """点击聊天输入框"""
        if not self.wechat_window:
            return False
        
        try:
            # 计算输入框位置（窗口底部中间）
            x = self.wechat_window.left + self.wechat_window.width // 2
            y = self.wechat_window.top + self.wechat_window.height - 100
            
            pyautogui.click(x, y)
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"[{self.get_time()}] 点击输入框失败: {e}")
        return False
    
    def type_message(self, message):
        """输入消息（使用剪贴板）"""
        try:
            # 清空输入框
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # 通过剪贴板输入中文
            temp = r'C:\temp\clip.txt'
            with open(temp, 'w', encoding='utf-8') as f:
                f.write(message)
            cmd = f'Get-Content "{temp}" -Encoding UTF8 | Set-Clipboard'
            subprocess.run(['powershell', '-command', cmd], capture_output=True)
            try:
                import os
                os.remove(temp)
            except:
                pass
            
            # 粘贴
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"[{self.get_time()}] 输入消息失败: {e}")
        return False
    
    def send_message(self):
        """发送消息"""
        try:
            pyautogui.press('enter')
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"[{self.get_time()}] 发送消息失败: {e}")
        return False
    
    def reply_to_message(self, message):
        """回复消息"""
        # 检查是否已回复过
        if self.is_message_replied(message):
            print(f"[{self.get_time()}] 消息已回复过，跳过: {message[:20]}...")
            return False
        
        # 检查冷却时间
        current_time = time.time()
        if current_time - self.last_reply_time < self.reply_cooldown:
            print(f"[{self.get_time()}] 回复冷却中，跳过")
            return False
        
        # 获取自动回复
        reply = self.get_auto_reply(message)
        if not reply:
            return False
        
        print(f"[{self.get_time()}] 收到消息: {message[:30]}...")
        print(f"[{self.get_time()}] 自动回复: {reply[:30]}...")
        
        # 激活微信窗口
        if not self.activate_wechat():
            return False
        
        # 点击输入框
        if not self.click_chat_input():
            return False
        
        # 输入回复
        if not self.type_message(reply):
            return False
        
        # 发送回复
        if not self.send_message():
            return False
        
        # 标记消息已回复
        self.mark_message_replied(message)
        self.last_reply_time = current_time
        
        print(f"[{self.get_time()}] ✅ 回复成功！")
        return True
    
    def monitor_and_reply(self):
        """监控并自动回复"""
        print("=" * 50)
        print("微信自动回复脚本 - 简化版")
        print("=" * 50)
        print(f"检查间隔: {CHECK_INTERVAL}秒")
        print(f"回复冷却: {self.reply_cooldown}秒")
        print("按 Ctrl+C 停止")
        print("=" * 50)
        
        while True:
            try:
                # 检查微信窗口
                if not self.find_wechat_window():
                    print(f"[{self.get_time()}] 未找到微信窗口，等待中...")
                    time.sleep(CHECK_INTERVAL)
                    continue
                
                # 检测新消息
                new_message = self.detect_new_message()
                if new_message:
                    # 自动回复
                    self.reply_to_message(new_message)
                
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                print(f"\n[{self.get_time()}] 停止监控")
                break
            except Exception as e:
                print(f"[{self.get_time()}] 监控出错: {e}")
                time.sleep(CHECK_INTERVAL)


def main():
    """主函数"""
    auto_reply = WeChatAutoReply()
    auto_reply.monitor_and_reply()


if __name__ == "__main__":
    main()
