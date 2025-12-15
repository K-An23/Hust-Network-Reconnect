import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

def check_website(url, timeout=5):
    """检查目标网址是否可访问"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 400
    except Exception:
        return False

# ===== 配置 =====
TARGET_URL = "https://www.baidu.com"  # 替换为你想检测的目标网址
FALLBACK_URL = "http://172.18.18.60:8080/"  # 替换为你的校园网登录页真实地址

# 填写账号/密码（请替换下面的值）
username = "Mxxxxxxx"
password = "xxxxxxxx"

# 获取页面源码并保存到文件
# page_html = driver.page_source
# with open("fallback_page_source.html", "w", encoding="utf-8") as f:
#     f.write(page_html)

# ===== 主程序 =====
if not check_website(TARGET_URL):
    print(f"[!] 目标网址 {TARGET_URL} 不可达，正在启动备用登录页面...")

    driver = webdriver.Edge(service=EdgeService(executable_path="./drivers/msedgedriver.exe"))
    driver.get(FALLBACK_URL)

    # 等待页面加载并确保 username 元素存在
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))

    # 直接通过 JS 设置值（页面 JS 可能会隐藏/切换输入框）
    driver.execute_script("document.getElementById('username').value = arguments[0];", username)
    driver.execute_script("""
        var p = document.getElementById('pwd');
        if (p) { p.style.display = 'block'; p.value = arguments[0]; }
    """, password)

    # 保存当前页面源码以便调试
    page_html = driver.page_source
    with open("fallback_page_source.html", "w", encoding="utf-8") as f:
        f.write(page_html)
    print("[i] 已保存页面源码到 fallback_page_source.html")

    # 等待并点击“连接”控件（页面中为 <a id="loginLink">）
    login_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "loginLink")))
    login_link.click()
    print("[✓] 已点击连接，等待跳转...")
    time.sleep(5)
print("[✓] 操作完成，程序结束。")