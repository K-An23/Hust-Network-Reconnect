# 校园网自动重连工具

检测校园网连通性，断网时自动登录认证页面。

## 功能

- 定期检测指定 URL 的可达性
- 检测到网络断开时，自动打开校园网认证门户
- 填写账号密码并提交登录
- 支持 Chrome 无头模式，不干扰前台工作

## 前置条件

1. **Python 3.10+**
2. **Chrome 浏览器**（已安装）
3. **ChromeDriver** — 版本需与本地 Chrome 主版本号一致
   - 从 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载
   - 解压后将 `chromedriver.exe` 放入项目下的 `chromedriver-win64/` 目录

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制环境变量模板：
   ```bash
   cp .env.example .env
   ```
2. 编辑 `.env`，填入校园网账号、密码及认证页面地址。

## 使用

### 命令行运行

```bash
python reconnect.py
```

### 通过批处理脚本

双击 `reconnect.bat` 即可运行。

> **提示**：可将 `reconnect.bat` 添加到 Windows 任务计划程序，实现开机自动重连。

## 项目结构

```
network_reconnect/
├── chromedriver-win64/   # ChromeDriver（已 gitignore，需自行下载）
├── .env                  # 用户配置（已 gitignore）
├── .env.example          # 配置模板
├── .gitignore
├── reconnect.py          # 主程序
├── reconnect.bat         # 快捷启动脚本
├── requirements.txt      # Python 依赖
└── README.md
```

## 免责声明

本工具仅供个人学习与便利使用。使用前请确认符合所在校园网的使用条款。
