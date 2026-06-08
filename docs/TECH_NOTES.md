# 微信自动化技术要领

## 一、核心技术栈

| 技术 | 用途 |
|------|------|
| Python 3.x | 主要编程语言 |
| pyautogui | 键鼠模拟 |
| pygetwindow | 窗口管理 |
| PowerShell | 剪贴板操作 |
| OpenClaw | AI 助理平台 |
| iLink API | 微信 Bot 协议 |

## 二、关键技术点

### 1. 中文输入难题

**问题**：pyautogui.typewrite() 不支持中文

**解决方案**：剪贴板中转

```python
def set_clipboard(text):
    """通过文件 + PowerShell 设置剪贴板"""
    temp = r'C:\temp\clip.txt'
    with open(temp, 'w', encoding='utf-8') as f:
        f.write(text)
    cmd = f'Get-Content "{temp}" -Encoding UTF8 | Set-Clipboard'
    subprocess.run(['powershell', '-command', cmd], capture_output=True)
    try:
        os.remove(temp)
    except:
        pass
```

**关键点**：
- 必须写入文件再读取，不能直接在 PowerShell 命令中传中文
- 编码必须是 UTF-8
- 操作完删除临时文件

### 2. 窗口坐标系统

微信窗口关键坐标：

```
┌─────────────────────────────────────┐
│  搜索框 (200, 35)                   │
├──────────┬──────────────────────────┤
│          │                          │
│  会话列表 │      聊天区域             │
│          │    (2/3W, 1/2H)          │
│          │                          │
│          ├──────────────────────────┤
│          │    输入框                 │
│          │    (1/2W+100, H-80)      │
└──────────┴──────────────────────────┘
```

**绝对坐标计算**：
```python
# 搜索框
search_x = w.left + 200
search_y = w.top + 35

# 聊天区域（用于复制消息）
chat_x = w.left + w.width * 2 // 3
chat_y = w.top + w.height // 2

# 输入框
input_x = w.left + w.width // 2 + 100
input_y = w.top + w.height - 80
```

### 3. 消息检测方案

#### 方案 A：复制检测法

```python
def copy_last_message(w):
    """复制当前聊天最后一条消息"""
    w.activate()
    pyautogui.click(w.left + w.width * 2 // 3, w.top + w.height // 2)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'end')  # 跳到最后
    pyautogui.press('up')            # 选择最后一条
    pyautogui.hotkey('ctrl', 'c')    # 复制
    return get_clipboard()
```

**优点**：简单可靠
**缺点**：只能获取文本消息

#### 方案 B：图像对比法

```python
def check_new_message(prev_screenshot):
    """截图对比检测新消息"""
    current = pyautogui.screenshot(region=(x, y, w, h))
    diff = pixelmatch(prev, current)
    return diff > THRESHOLD
```

**优点**：可以检测所有类型消息
**缺点**：需要计算差异阈值

### 4. 群聊特殊处理

群聊搜索结果不能用键盘选择，必须用鼠标点击：

```python
# ❌ 错误：用 Tab/Enter 选择搜索结果
pyautogui.press('tab')
pyautogui.press('enter')

# ✅ 正确：用鼠标点击搜索结果
search_result_y = search_y + 55  # 搜索结果位置
pyautogui.click(search_x, search_result_y)
time.sleep(3)  # 等待滑动动画
```

### 5. OpenClaw iLink 集成

**架构**：
```
微信用户 → iLink Bot API → OpenClaw Gateway → 贾维斯(AI)
                                              ↓
                                         自动回复
```

**配置**：
```json
{
  "channels": {
    "openclaw-weixin": {
      "enabled": true,
      "provider": "openclaw-weixin",
      "config": {
        "appId": "wx...",
        "appSecret": "..."
      }
    }
  }
}
```

**限制**：
- Bot 账号无法被普通用户搜索
- 只能回复已建立对话的人
- 需要用户先给 Bot 发消息

## 三、常见问题

### Q1: pyautogui 操作无反应

**原因**：窗口未激活或失去焦点

**解决**：
```python
w.activate()
time.sleep(0.5)  # 等待窗口激活
```

### Q2: 中文输入乱码

**原因**：编码问题

**解决**：确保文件用 UTF-8 编码写入

### Q3: 搜索结果点错

**原因**：搜索结果位置不固定

**解决**：用鼠标点击而非键盘选择

### Q4: 消息发送失败

**原因**：输入框未获得焦点

**解决**：
```python
# 先点击输入框
pyautogui.click(input_x, input_y)
time.sleep(0.3)
# 再粘贴发送
```

## 四、安全注意事项

1. **FAILSAFE**：必须开启，鼠标移到左上角可停止
```python
pyautogui.FAILSAFE = True
```

2. **操作间隔**：不要太快，模拟人类
```python
time.sleep(0.3 + random.random() * 0.5)
```

3. **不要调整窗口大小**：只用 activate()

4. **分步执行**：不要一次性运行整个脚本

## 五、最佳实践

### 脚本结构

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyautogui
import pygetwindow as gw
import time
import subprocess
import os

# 配置
pyautogui.FAILSAFE = True

def set_clipboard(text):
    """设置剪贴板"""
    # ...

def find_wechat():
    """找到微信窗口"""
    # ...

def main():
    """主函数"""
    w = find_wechat()
    if not w:
        print("未找到微信窗口")
        return
    
    # 分步骤执行
    step1_activate(w)
    step2_search(w, "联系人")
    step3_send(w, "消息内容")

if __name__ == "__main__":
    main()
```

### 错误处理

```python
try:
    w.activate()
except Exception as e:
    print(f"激活窗口失败: {e}")
    # 尝试重新查找窗口
    w = find_wechat()
```

### 日志记录

```python
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
```
