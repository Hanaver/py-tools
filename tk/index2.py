import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# 初始化Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 可选：无头模式
driver = webdriver.Chrome(options=options)

# 打开TikTok网站
driver.get("https://www.tiktok.com")

# 等待页面加载
time.sleep(5)  # 根据实际情况调整等待时间

# 搜索关键字
search_keyword = "fashion"  # 替换为您的关键字
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
time.sleep(5)

# 解析搜索结果页面
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 查找博主链接
profiles = soup.find_all('a', href=True)
profile_links = [profile['href'] for profile in profiles if '/@' in profile['href']]
print(profile_links)
exit()

# 准备存储数据
data = []

# 遍历每个博主页面，提取信息
for link in profile_links:
    driver.get("https://www.tiktok.com" + link)
    time.sleep(5)  # 等待页面加载
    profile_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 提取博主信息（例如：名称、关注数、邮箱等）
    try:
        name = profile_soup.find('h1', {'data-e2e': 'user-title'}).text.strip()
    except AttributeError:
        name = None

    try:
        followers = profile_soup.find('strong', {'title': 'Followers'}).text.strip()
    except AttributeError:
        followers = None

    try:
        bio = profile_soup.find('h2', {'data-e2e': 'user-bio'}).text.strip()
    except AttributeError:
        bio = None

    data.append({
        'name': name,
        'followers': followers,
        'bio': bio
    })

# 关闭浏览器
driver.quit()

# 保存数据到CSV文件
df = pd.DataFrame(data)
df.to_csv('tiktok_profiles.csv', index=False)

print("数据已保存到tiktok_profiles.csv")
