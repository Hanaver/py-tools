import time
import random
import re  # 正则表达式匹配库
import time  # 事件库，用于硬性等待
import urllib  # 网络访问
import cv2  # opencv库

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# 初始化Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 可选：无头模式
service = webdriver.ChromeService(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
webUrl = "https://www.tiktok.com"
# 打开TikTok网站
driver.get(webUrl)

# 封装的计算图片距离的算法
def get_pos(imageSrc):
    # 读取图像文件并返回一个image数组表示的图像对象
    image = cv2.imread(imageSrc)
    # GaussianBlur方法进行图像模糊化/降噪操作。
    # 它基于高斯函数（也称为正态分布）创建一个卷积核（或称为滤波器），该卷积核应用于图像上的每个像素点。
    blurred = cv2.GaussianBlur(image, (5, 5), 0, 0)
    # Canny方法进行图像边缘检测
    # image: 输入的单通道灰度图像。
    # threshold1: 第一个阈值，用于边缘链接。一般设置为较小的值。
    # threshold2: 第二个阈值，用于边缘链接和强边缘的筛选。一般设置为较大的值
    canny = cv2.Canny(blurred, 0, 100)  # 轮廓
    # findContours方法用于检测图像中的轮廓,并返回一个包含所有检测到轮廓的列表。
    # contours(可选): 输出的轮廓列表。每个轮廓都表示为一个点集。
    # hierarchy(可选): 输出的轮廓层次结构信息。它描述了轮廓之间的关系，例如父子关系等。
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 遍历检测到的所有轮廓的列表
    for contour in contours:
        # contourArea方法用于计算轮廓的面积
        area = cv2.contourArea(contour)
        # arcLength方法用于计算轮廓的周长或弧长
        length = cv2.arcLength(contour, True)
        print(area)
        print(length)
        print('-------')
        # 如果检测区域面积在5025-7225之间，周长在300-380之间，则是目标区域
        if 4000 < area < 7225 and 300 < length < 450:
            # 计算轮廓的边界矩形，得到坐标和宽高
            # x, y: 边界矩形左上角点的坐标。
            # w, h: 边界矩形的宽度和高度。
            x, y, w, h = cv2.boundingRect(contour)
            print("计算出目标区域的坐标及宽高：", x, y, w, h)
            # 在目标区域上画一个红框看看效果
            # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            # cv2.imwrite("111.jpg", image)
            return x
    return 0
# 
# dis = get_pos('bigImage.png')
# exit()

def goVerify():
    try:
        print(111111111)
        time.sleep(5)
        # yanzm = driver.find_element(By.XPATH, '//*[@id="tiktok-verify-ele"]')
        yanzt = driver.find_element(By.XPATH, '//*[@id="captcha-verify-image"]')
        print(33333)
        imgUrl = yanzt.get_attribute('src')
        urllib.request.urlretrieve(imgUrl, './bigImage.png')
        
        # 移动验证码
        dis = get_pos('bigImage.png')
        smallImage = driver.find_element(By.XPATH, '//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
        # print(smallImage.location['x'])
        # print(dis)
        # print(dis*340/552)
        newDis = int(dis*340/552)-6
        driver.implicitly_wait(5)
        
        # 按下小滑块按钮不动
        ActionChains(driver).click_and_hold(smallImage).perform()
        i = 0
        moved = 0
        while moved < newDis:
            x = random.randint(3, 10)  # 每次移动3到10像素
            moved += x
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
            print("第{}次移动后，位置为{}".format(i, smallImage.location['x']))
            i += 1
        # 移动完之后，松开鼠标
        ActionChains(driver).release().perform()
        time.sleep(5)
    except NoSuchElementException:
        print(22222)
        time.sleep(2)
    pass

# 等待页面加载
time.sleep(10)  # 根据实际情况调整等待时间
cookies = driver.get_cookies()
for item in cookies:
    driver.add_cookie(item)
    
try:
    youke = driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div/div[3]/div/div[2]')
    time.sleep(2)
    youke.click()
except NoSuchElementException:
    time.sleep(5)

# 搜索关键字
search_box = driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input')
time.sleep(1)
search_box.send_keys("Stand")
time.sleep(2)
search_box.send_keys(Keys.RETURN)
# driver.find_element(By.CLASS_NAME, 'css-16dy42q-ButtonSearch').click()

# 等待搜索结果加载
goVerify()

# time.sleep(1000)
account = driver.find_element(By.XPATH, '//*[@id="search-tabs"]/div[1]/div[1]/div[1]/div[2]')
account.click()

goVerify()

# driver.execute_script("window.scrollTo(0, 600);")

# time.sleep(10)

# 解析搜索结果页面
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 查找博主链接
profiles = soup.find_all('a', href=True)
profile_links = [profile['href'] for profile in profiles if '/@' in profile['href']]
profile_links = profile_links[1:]
# 去除重复
profile_links = list(set(profile_links))
print(profile_links)

# 准备存储数据
data = []
# 遍历每个博主页面，提取信息
for link in profile_links:
    print(webUrl + link)
    driver.get(webUrl + link)
    time.sleep(8)  # 等待页面加载
    
    title = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[1]/div[2]/h1')
    followers = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[2]/strong')
    detail = driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h2')
    
    data.append({
        'name': title.text,
        'followers': followers.text,
        'email': detail.text
    })

print(data)
# 关闭浏览器
driver.quit()

# 保存数据到CSV文件
df = pd.DataFrame(data)
df.to_csv('tiktok_profiles.csv', index=False)

print("数据已保存到tiktok_profiles.csv")

