import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ── 加载 .env 配置 ──────────────────────────────────────────
load_dotenv()

def check_website(url, timeout=5):
    """检查目标网址是否可访问"""
    try:
        # 校园网断网时 requests 可能超时，设短超时以便快速判断
        response = requests.get(url, timeout=timeout)
        return response.status_code < 400
    except Exception:
        return False

# ===== 配置（通过 .env 或环境变量覆盖） =====
TARGET_URL = os.getenv("TARGET_URL", "https://www.baidu.com")
FALLBACK_URL = os.getenv(
    "FALLBACK_URL",
    "http://YOUR_PORTAL_SERVER:8080/eportal/index.jsp",
)

USERNAME = os.getenv("PORTAL_USERNAME", "")
PASSWORD = os.getenv("PORTAL_PASSWORD", "")

if not USERNAME or not PASSWORD:
    print("[ERROR] 请设置环境变量 PORTAL_USERNAME 和 PORTAL_PASSWORD，或创建 .env 文件。")
    sys.exit(1)

# === 驱动路径（默认使用项目下的 chromedriver-win64） ===
BASE_DIR = Path(__file__).resolve().parent
DRIVER_PATH = str(BASE_DIR / "chromedriver-win64" / "chromedriver.exe")

if not Path(DRIVER_PATH).exists():
    print(f"[ERROR] 驱动文件不存在: {DRIVER_PATH}")
    print("请手动下载对应版本的 chromedriver.exe 并放入 ./chromedriver-win64/ 文件夹")
    sys.exit(1)

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless=new")  # 新版 Chrome 无头模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

if not check_website(TARGET_URL):
    print(f"[!] 目标网址 {TARGET_URL} 不可达，正在启动备用登录页面...")
    driver = None
    try:
        # 使用本地固定的驱动路径
        service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(FALLBACK_URL)

        # 等待页面加载并确保 username 元素存在
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))

        # 直接通过 JS 设置值
        driver.execute_script("document.getElementById('username').value = arguments[0];", USERNAME)
        driver.execute_script("""
            var p = document.getElementById('pwd');
            if (p) { p.style.display = 'block'; p.value = arguments[0]; }
        """, PASSWORD)

        # 保存当前页面源码以便调试
        page_html = driver.page_source
        with open("fallback_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_html)
        print("[i] 已保存页面源码到 fallback_page_source.html")

        # 等待并点击“连接”控件
        login_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "loginLink")))
        login_link.click()
        print("[✓] 已点击连接，等待跳转...")
        time.sleep(5)
        
        print("[✓] 登录操作完成。")
        
    except Exception as e:
        print(f"[ERROR] 登录过程中发生错误: {e}")
    finally:
        if driver is not None:
            driver.quit()
else:
    print("[i] 网络正常，无需登录。")

print("[✓] 程序结束。")