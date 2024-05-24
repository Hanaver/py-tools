import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# 初始化Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 可选：无头模式
service = webdriver.ChromeService(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# 打开TikTok网站
driver.get("https://www.tiktok.com/")

# 等待页面加载
time.sleep(30)  # 根据实际情况调整等待时间
cookies = driver.get_cookies()
for item in cookies:
    driver.add_cookie(item)

# youke = driver.find_element(By.CLASS_NAME, 'css-1gtmaw0-DivBoxContainer')
# if youke is not None:
#     youke.clear()
#     time.sleep(10)

# 搜索关键字
search_box = driver.find_element(By.CLASS_NAME, 'css-1yf5w3n-InputElement')
search_box.send_keys("Stand")
time.sleep(5)
search_box.send_keys(Keys.RETURN)
# driver.find_element(By.CLASS_NAME, 'css-16dy42q-ButtonSearch').click()

# 
# # 等待搜索结果加载
time.sleep(20)

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
    driver.get(link)
    time.sleep(5)  # 等待页面加载
    profile_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 提取博主信息（例如：名称、关注数、邮箱等）
    name = profile_soup.find('h1', {'class': 'profile-username'}).text
    followers = profile_soup.find('strong', {'title': 'Followers'}).text
    email = None
    # 提取邮箱（假设在简介中）
    bio = profile_soup.find('h2', {'class': 'profile-bio'}).text
    if "@" in bio:
        email = bio.split(' ')[-1]  # 简单提取方法，可根据实际情况调整

    data.append({
        'name': name,
        'followers': followers,
        'email': email
    })

# 关闭浏览器
driver.quit()

# 保存数据到CSV文件
df = pd.DataFrame(data)
df.to_csv('tiktok_profiles.csv', index=False)

print("数据已保存到tiktok_profiles.csv")
