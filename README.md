# （华科）校园网自动重连脚本（Windows，2026.5.24更新）

一款用于校园网环境的自动网络重连工具。当检测到网络连接中断时，自动完成 Portal 认证页面的登录流程，无需人工干预。本项目仅适用于Windows，Linux的自动重连可参见 https://github.com/K-An23/Hust-Network-Reconnect-Linux-

建议还是使用Chrome，然后将该浏览器的自动更新全部停掉（[如何彻底禁用 Chrome 自动更新_chrome关闭自动更新-CSDN博客](https://blog.csdn.net/olixu/article/details/149290012)）。这样可以避免浏览器的自动更新使得本地驱动与浏览器的版本不适配导致的自动重连失败。

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

  > 从 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载对应版本的 ChromeDriver，将 `chromedriver.exe` 置于项目根目录下的 `chromedriver-win64/` 文件夹中。如果找不到适合的版本，那就直接打开如下链接：https://storage.googleapis.com/chrome-for-testing-public/{Chrome版本号}/win64/chromedriver-win64.zip 就可以下载了
  >

## Getting Started

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭据

复制环境变量模板并编辑：

```bash
copy .env.example .env
```

根据实际情况填写以下内容：

| 变量                | 说明                                             |
| ------------------- | ------------------------------------------------ |
| `PORTAL_USERNAME` | 校园网账号                                       |
| `PORTAL_PASSWORD` | 校园网密码                                       |
| `TARGET_URL`      | 连通性检测目标（默认 `https://www.baidu.com`） |
| `FALLBACK_URL`    | 认证页面入口地址                                 |

### 3. 运行

```bash
python reconnect.py
```

程序启动后自动检测网络连通性，必要时执行认证流程。自己可以断网与不断网来试一下。

## Scheduled Execution（计划任务配置）

为避免网络断开后长时间未重连，推荐通过 Windows 任务计划程序设置定时执行（例如每 5 分钟运行一次）。

### 步骤一：准备工作

确保以下两个文件位于项目目录中（它们已被 `.gitignore` 排除，需手动创建）：

- **`reconnect.bat`** — 批处理启动脚本，内容如下：
  ```batch
    @echo off
    <!-- 改为你的项目目录位置，下述是示例 -->
    cd /d "D:\Workspace\self_tools\network_reconnect"
    <!-- 改为你的 python 运行环境，下述是示例 -->
    "D:/Anaconda/envs/syn/python.exe" reconnect.py
  ```
- **`reconnect_hidden.vbs`** — 隐藏命令行窗口的 VBS 脚本，内容如下：
  ```vb
  <!-- 将后面的目录改为你的项目目录位置，下述是示例 -->
  CreateObject("Wscript.Shell").Run "D:\Workspace\self_tools\network_reconnect\reconnect.bat", 0, False
  ```

> **注意**：请将上述 `reconnect_hidden.vbs` 中的路径替换为你的实际项目路径。

### 步骤二：创建计划任务

1. 按 `Win + R`，输入 `taskschd.msc` 并回车，打开**任务计划程序**。
2. 点击右侧 **"创建基本任务…"**。
3. **名称**：输入 `HustNetworkReconnect`（或任意名称）。
4. **触发器**：选择 **"每天"** → 设置 **"每 5 分钟重复一次，持续 24 小时"**。
   - 若向导不支持此设置，可在创建完成后右键任务 → **属性** → **触发器** → **编辑** 中调整。
5. **操作**：选择 **"启动程序"** → **程序或脚本** 中填写：
   ```
   C:\Windows\System32\wscript.exe
   ```
   **添加参数** 中填写（请替换为你的实际路径）：
   ```
   D:\Path\To\network_reconnect\reconnect_hidden.vbs
   ```
6. 完成创建。

### 原理说明

- `reconnect_hidden.vbs` 调用 `Wscript.Shell.Run` 时使用了参数 `0`，使被调用的 `reconnect.bat` 在**后台静默运行**，不弹出命令行窗口。
- 任务计划程序定期触发 VBS 脚本 → VBS 静默启动 BAT → BAT 调用 Python 执行检测与重连逻辑。

## Project Structure

```
network_reconnect/
├── chromedriver-win64/    # ChromeDriver 运行时（已配置 gitignore，需自行下载）
├── .env                   # 用户配置文件（已配置 gitignore，不纳入版本控制）
├── .env.example           # 环境变量模板
├── .gitignore
├── LICENSE
├── reconnect.py           # 主程序入口
├── reconnect.bat          # 批处理启动脚本（本地创建，已配置 gitignore）
├── reconnect_hidden.vbs   # 隐藏窗口启动脚本（本地创建，已配置 gitignore）
├── requirements.txt       # Python 依赖清单
└── README.md
```

## License

本项目基于 MIT 许可证开源。详见 [LICENSE](./LICENSE) 文件。

## Disclaimer

本工具仅供学习与便利目的使用。使用者应确保其使用方式符合所在校园网的相关规定与服务条款。作者不对因使用本工具产生的任何后果承担责任。
