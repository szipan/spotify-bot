import random
import os
import datetime
import time
import multiprocessing
import asyncio
import concurrent.futures
import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
from spotify_song import SpotifySongModel

# options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=http://127.0.0.1:1080')
# PROXY = '127.0.0.1:1080'
# webdriver.DesiredCapabilities.CHROME['proxy'] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "proxyType": "MANUAL",
# }

loginRetryTimes = 3         # 登录重试次数
musicPlayTime = 55          # 单位秒 + 默认缓冲5s
playRetryTimes = 3          # 播放重试次数
loopTime = 3                # 循环播放次数

# 代理服务器
PROXY = ["127.0.0.1:7890"]

userPwdList = [
    ('adambandura.g@gmail.com', 'adam.bandura'),
]

processNum = len(userPwdList)              # 同时登录的账号数量

urlsList = [
    # 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',
    'https://open.spotify.com/track/302TLuYhjWgiAOSxyEpoMM?si=4186ea8605b34f50',
]

if not SpotifySongModel.exists():
    SpotifySongModel.create_table(
        read_capacity_units=100, write_capacity_units=100)

for uli in range(len(urlsList)):
    song = SpotifySongModel('url%d' % uli)
    song.save()


def worker(userInfo):
    """该函数将在子进程中执行"""
    uEmail = userInfo[0]
    uPwd = userInfo[1]
    loggedIn = False

    # 实例化1个谷歌浏览器对象
    time.sleep(1)
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.set_headless()
    # chrome_options.add_argument('--proxy-server=%s' % PROXY[random.randrange(len(PROXY))])
    # chrome_options.add_argument('--proxy-server=%s' % random.choice(PROXY))
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }}
    chrome_options.add_experimental_option('prefs', prefs)
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    browser = webdriver.Chrome(options=chrome_options)
    # for uli in range(len(urlsList)):
    for uli in range(len(urlsList)*loopTime):
        # print('当前URL的序列号111！ 序列号：%s' % uli)
        # 随机等待，防止被封
        time.sleep(random.randrange(30))
        # time.sleep(random.randrange(1))
        if uli >= len(urlsList):
            uli = uli % len(urlsList)
            # print('当前URL的序列号222！ 序列号：%s' % uli)
        urlStr = urlsList[uli]
        browser.get(urlStr)

        # 登录账号
        if not loggedIn:
            for i in range(int(loginRetryTimes)):
                try:
                    browser.get(urlStr)
                    browser.implicitly_wait(60)
                    browser.find_element(
                        by=By.CSS_SELECTOR, value='[data-testid="login-button"]').click()
                except Exception as e:
                    print('音乐网址打开失败！ 网址：%s' % urlStr)
                    continue
                try:
                    browser.find_element(
                        by=By.CSS_SELECTOR, value='[id="login-username"]').send_keys('%s' % uEmail)
                    browser.find_element(
                        by=By.CSS_SELECTOR, value='[id="login-password"]').send_keys('%s' % uPwd)
                    time.sleep(random.randrange(5))
                    browser.find_element(
                        by=By.CSS_SELECTOR, value='[id="login-button"]').click()
                    time.sleep(random.randrange(5))
                    loggedIn = True
                    break
                except Exception as e:
                    print('%s登录失败！ 重试第%d次  URL: %s' % (uEmail, i+1, urlStr), e)
                    continue
            if not loggedIn:
                print('登录失败！ 放弃账号：%s  URL:%s' % (uEmail, URLSTR))
                browser.quit()

        # 播放音乐
        for i in range(int(playRetryTimes)):
            try:
                time.sleep(random.randrange(5))
                startTime = datetime.datetime.now()
                # browser.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button').click()
                playButtons = browser.find_elements(
                    by=By.CSS_SELECTOR, value='[data-testid="play-button"]')
                playButtons[1].click()

                # 默认缓冲5s
                time.sleep(5)
                time.sleep(int(musicPlayTime))

                song = SpotifySongModel.get('url%d' % uli)
                song.playCount += 1
                song.save()
                print('Parent process：%d， Process：%d， Email：%s， URL：%s， Count：%s， Play Duration：%s' % (os.getppid(), os.getpid(
                ), uEmail, urlStr, song.playCount, datetime.datetime.now()-startTime))
                break
            except Exception as e:
                print('Play Failure: %s  %s, Retry %d times, URL：%s' %
                      (e, uEmail, i+1, urlStr))

    # browser.close() # Closes the current window
    browser.quit()  # Closes the browser and shuts down the ChromeDriver executable that is started when starting the ChromeDriver


async def main():
    # max_workers = 2  # Maximum parallel processes
    with multiprocessing.Manager() as manager, concurrent.futures.ProcessPoolExecutor(max_workers=int(processNum)) as executor:
        # gUrlsList = manager.list(urlsList)

        # Use submit() to submit tasks to the process pool
        futures = [executor.submit(worker, userInfo)
                   for userInfo in userPwdList]
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

    print("All tasks completed！")
    fo = open('music_play_count.txt', 'w')
    for i in range(len(urlsList)):
        song = SpotifySongModel.get('url%d' % i)
        print('URL: %s  Count: %s' % (urlsList[i], song.playCount))
        fo.write('URL: %s  Count: %s\n' % (urlsList[i], song.playCount))

    fo.close()


if __name__ == "__main__":
    asyncio.run(main())

# if __name__ == '__main__':
#     print(datetime.datetime.now())
#
#     # 创建进程池
#     print(len(urlsList), '#########')
#     manager = multiprocessing.Manager()
#     gUserPwdList = manager.list(userPwdList)
#     gUrlsList = manager.list(urlsList)
#
#
#     pool = multiprocessing.Pool(processes=processNum)
#     # 启动进程池中的进程
#     # pool.apply_async(process_task, (gUserPwdList, gUrlsList))
#     pool.apply_async(process_task, range(10))
#
#     # 关闭进程池
#     pool.close()
#     # 等待进程池中的进程结束
#     pool.join()

    # # 创建子进程
    # pList = []
    # for i in range(len(gUserPwdList)):
    #   p = multiprocessing.Process(target=worker, args=(gUserPwdList, gUrlsList))
    #   # 启动子进程
    #   p.start()
    #   pList.append(p)
    #
    # while p in pList:
    #   # 等待子进程结束
    #   p.join()

    # print(datetime.time().strftime('%H:%M:%S'))
    # print(datetime.datetime.now())
