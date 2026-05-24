# Campus Network Auto-Reconnect

一款用于校园网环境的自动网络重连工具。当检测到网络连接中断时，自动完成 Portal 认证页面的登录流程，无需人工干预。

## Overview

本工具持续监测目标 URL 的可达性以判断网络连通状态。一旦检测到网络不可达，即自动启动浏览器驱动，导航至校园网认证门户，填写凭据并提交登录，从而实现断线自动重连。

## Features

- **连通性检测**：通过 HTTP 请求定期探测指定目标地址，快速判断网络状态
- **自动认证**：断网时自动打开校园网 Portal 认证页面并完成登录
- **无头运行**：采用 Chrome Headless 模式，运行时无界面干扰
- **配置外置**：敏感信息（账号、密码、认证页地址）通过环境变量或 `.env` 文件管理，避免硬编码

## Prerequisites

- **Python** >= 3.10
- **Google Chrome** 浏览器（已安装）
- **ChromeDriver** — 版本须与本地 Chrome 主版本号一致

  > 从 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载对应版本的 ChromeDriver，将 `chromedriver.exe` 置于项目根目录下的 `chromedriver-win64/` 文件夹中。

## Getting Started

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭据

复制环境变量模板并编辑：

```bash
cp .env.example .env
```

根据实际情况填写以下内容：

| 变量 | 说明 |
|---|---|
| `PORTAL_USERNAME` | 校园网账号 |
| `PORTAL_PASSWORD` | 校园网密码 |
| `TARGET_URL` | 连通性检测目标（默认 `https://www.baidu.com`） |
| `FALLBACK_URL` | 认证页面入口地址 |

### 3. 运行

```bash
python reconnect.py
```

程序启动后自动检测网络连通性，必要时执行认证流程。

> **提示**：可通过 Windows 任务计划程序配置定时执行，实现开机自启或周期性重连。

## Project Structure

```
network_reconnect/
├── chromedriver-win64/   # ChromeDriver 运行时（已配置 gitignore，需自行下载）
├── .env                  # 用户配置文件（已配置 gitignore，不纳入版本控制）
├── .env.example          # 环境变量模板
├── .gitignore
├── LICENSE
├── reconnect.py          # 主程序入口
├── requirements.txt      # Python 依赖清单
└── README.md
```

## License

本项目基于 MIT 许可证开源。详见 [LICENSE](./LICENSE) 文件。

## Disclaimer

本工具仅供学习与便利目的使用。使用者应确保其使用方式符合所在校园网的相关规定与服务条款。作者不对因使用本工具产生的任何后果承担责任。
