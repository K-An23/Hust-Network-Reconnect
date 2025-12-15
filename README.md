# （华科）校园网自动重连脚本

## 功能
- 检测目标网址是否可访问（默认百度）。
- 不可达时，自动打开校园网登录页，填入账号密码并点击“连接”。
- 保存登录页源码到 `fallback_page_source.html` 便于排查。
- 可设置定时任务进行定时自动检测与重连

## 目录结构
- `reconnect.py`：主脚本。
- `reconnect.bat`：Windows 一键运行批处理。
- `drivers/`：Edge WebDriver 及许可证文件。

## 环境要求
- Windows + Edge 浏览器（Linux 使用 selenium 参考https://blog.csdn.net/FujLiny/article/details/115387701）
- Python 3.8+
- 依赖：`requests`, `selenium`, `webdriver-manager`

安装依赖：
```powershell
pip install requests selenium webdriver-manager
```

## 使用方法
1) 编辑 `reconnect.py`，修改：
   - `TARGET_URL`：用来检测连通性的外网地址。
   - `FALLBACK_URL`：校园网登录页地址。
   - `username` / `password`：你的校园网账号密码。
2) 运行脚本：
   ```powershell
   python reconnect.py
   ```
3) 如果目标网址不可达，脚本会自动：
   - 打开 Edge，访问登录页。
   - 填入账号密码并点击登录。
   - 等待几秒后结束。

可选：双击 `reconnect.bat` 直接运行。

## EdgeDriver 说明
使用edge浏览器来自动化打开网页（Chrome浏览器也是可以的，需要稍微改一下脚本中webdriver的引用库即可。这里脚本主要使用edge浏览器）
- 脚本默认使用本地 `./drivers/msedgedriver.exe`。
- 如果不存在，将由 `webdriver-manager` 自动下载匹配版本。
- 如需固定驱动，放置在 `drivers/` 下并确保版本与本机 Edge 匹配。可见[安装 selenium 及配置 edge 浏览器驱动_edge浏览器驱动-CSDN博客](https://blog.csdn.net/m0_61552056/article/details/134956649)

## 调试
- 登录页解析失败时，检查生成的 `fallback_page_source.html`。
- 如元素 ID 不同，需在脚本中调整：
  - 用户名输入框 ID：`username`
  - 密码输入框 ID：`pwd`
  - 登录按钮 ID：`loginLink`
 
## 定时任务
直接设置一个定时任务去定时调用这个reconnect.bat脚本即可。Windows参考：https://zhuanlan.zhihu.com/p/430602325。
linux好像也有定时任务的设置。
