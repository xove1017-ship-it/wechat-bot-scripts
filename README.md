# 微信自动化工具集

基于 Python + pyautogui 的微信桌面自动化方案，支持自动回复、消息发送、中文输入等功能。

> 配合 [OpenClaw](https://github.com/openclaw/openclaw) + iLink Bot API 可实现 AI 自动回复

## 📁 项目结构

```
wechat-automation/
├── scripts/
│   ├── auto_reply/          # 自动回复脚本
│   │   ├── simple.py        # 简化版自动回复
│   │   ├── stable.py        # 稳定版监控
│   │   └── monitor.py       # 消息监控
│   ├── messaging/           # 消息发送
│   │   ├── send_message.py  # 发送消息
│   │   └── clipboard.py     # 剪贴板工具
│   ├── moments/             # 朋友圈相关
│   │   └── post_moments.py  # 发布朋友圈
│   └── utils/               # 工具函数
│       ├── window.py        # 窗口管理
│       └── clipboard.py     # 剪贴板操作
├── docs/
│   └── TECH_NOTES.md        # 技术要领
└── README.md
```

## 🚀 快速开始

### 环境要求

```bash
pip install pyautogui pygetwindow pyperclip pillow
```

### 基本用法

#### 1. 发送消息

```python
from scripts.utils.window import find_wechat_window, activate_wechat
from scripts.utils.clipboard import set_clipboard
import pyautogui
import time

# 找到并激活微信窗口
w = find_wechat_window()
activate_wechat(w)

# 搜索联系人
pyautogui.click(w.left + 200, w.top + 35)  # 点击搜索框
set_clipboard("联系人名称")
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)

# 发送消息
pyautogui.click(w.left + w.width // 2 + 100, w.top + w.height - 80)
set_clipboard("你好！")
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
```

#### 2. 自动回复

```python
from scripts.auto_reply.simple import WeChatAutoReply

# 创建自动回复实例
auto_reply = WeChatAutoReply()

# 启动监控
auto_reply.monitor_and_reply()
```

## 🔧 技术要领

### 1. 中文输入方案

由于 pyautogui 不支持直接输入中文，使用剪贴板方案：

```python
def set_clipboard(text):
    """通过 PowerShell 设置剪贴板"""
    temp = r'C:\temp\clip.txt'
    with open(temp, 'w', encoding='utf-8') as f:
        f.write(text)
    cmd = f'Get-Content "{temp}" -Encoding UTF8 | Set-Clipboard'
    subprocess.run(['powershell', '-command', cmd], capture_output=True)
    os.remove(temp)
```

### 2. 窗口定位策略

微信窗口坐标计算：

```python
# 搜索框位置：左上角偏移
search_x = w.left + 200
search_y = w.top + 35

# 输入框位置：窗口底部中间
input_x = w.left + w.width // 2 + 100
input_y = w.top + w.height - 80

# 聊天区域：窗口中间偏右
chat_x = w.left + w.width * 2 // 3
chat_y = w.top + w.height // 2
```

### 3. 消息检测机制

**方案一：复制检测**
- 点击聊天区域 → Ctrl+End 跳到最后 → Up 选择最后一条 → Ctrl+C 复制
- 对比剪贴板内容判断是否有新消息

**方案二：图像对比**
- 定时截图聊天区域
- 使用 pixelmatch 对比像素变化
- 变化超过阈值判定有新消息

### 4. 防检测措施

```python
# 随机延迟，模拟人类操作
time.sleep(0.3 + random.random() * 0.5)

# 操作间隔不要太规律
CHECK_INTERVAL = 15 + random.randint(-3, 3)
```

### 5. 群聊注意事项

- 群聊搜索结果需要用鼠标点击，不能用 Tab/Enter
- 点击后等待 3 秒（滑动动画）
- 搜索结果 Y 坐标 = 搜索框 Y + 55

## ⚠️ 注意事项

1. **窗口尺寸**：不要调整微信窗口大小，只用 activate()
2. **操作顺序**：必须分步骤执行，不能一次性运行整个脚本
3. **等待时间**：每步操作后需要适当的 sleep 等待
4. **剪贴板清理**：使用完后删除临时文件
5. **安全退出**：设置 pyautogui.FAILSAFE = True，鼠标移到左上角可紧急停止

## 📝 OpenClaw 集成

通过 OpenClaw 的 message 工具可以实现微信消息收发：

```python
# OpenClaw 配置
{
  "channels": {
    "openclaw-weixin": {
      "enabled": true,
      "provider": "openclaw-weixin",
      "config": {
        "appId": "your-app-id",
        "appSecret": "your-app-secret"
      }
    }
  }
}
```

### 限制说明

- iLink Bot 协议：普通微信用户搜索不到 Bot 账号
- 只能回复已建立对话的用户
- 无法主动联系未建立对话的人

## 📬 联系方式

想联系作者？在 GitHub 页面按 F12 打开控制台：

1. 先在控制台输入 `allow pasting` 回车（解除粘贴限制）
2. 然后粘贴执行以下代码：

```javascript
console.log('微信: ' + atob('OTc5NDQ3MDI5'))
```

## 🔗 相关项目

- [sightflow-mimo](https://github.com/xove1017-ship-it/sightflow-mimo) - 本项目的 SightFlow 修改版，支持小米 Mimo 模型
- [wechat-bot-scripts](https://github.com/xove1017-ship-it/wechat-bot-scripts) - 微信自动化脚本工具集

## 📄 License

MIT
