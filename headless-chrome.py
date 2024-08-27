from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from spotify_song import SpotifySongModel
import asyncio
import multiprocessing
import concurrent.futures
import time, datetime
import random
import os, sys, json

loginRetryTimes = 3         # 登录重试次数
musicPlayTime = 55          # 单位秒 + 默认缓冲5s
playRetryTimes = 3          # 播放重试次数
loopTime = 1                # 循环播放次数
currentDirectory = os.getcwd()
#json_data = sys.argv[1]

json_data = '''
{
	"users" : [
		{
			"email": "szipan3@gmail.com",
			"password": "Zaq!2wsxcde3"
		}
	],
	"urls" : [
		"https://open.spotify.com/track/302TLuYhjWgiAOSxyEpoMM?si=4186ea8605b34f50",
		"https://open.spotify.com/track/1jhMocH0Xw3NTVlA3K10Bf?si=0b4aa6b430eb4be8",
		"https://open.spotify.com/track/7LV81smt0r3AKGolcjlRDW?si=421ef89fbfa24cd1",
		"https://open.spotify.com/track/7BqBn9nzAq8spo5e7cZ0dJ?si=494a77ba46dd417b",
		"https://open.spotify.com/track/0KKkJNfGyhkQ5aFogxQAPU?si=d91ac294649b494e",
		"https://open.spotify.com/track/2R6s6LwSa4DtpsUUBlhPiH?si=e95460b982c942bc",
		"https://open.spotify.com/track/1QGq2WRldwDQESDKkJBYW2?si=63c8369f23814c86",
		"https://open.spotify.com/track/2aMN1ky0SzSEcV1QdBYbW9?si=c4512aa54fa24a05",
		"https://open.spotify.com/track/1YgXa1PM4TXwxKkRpTtccs?si=bdbdfef8f4df459a",
		"https://open.spotify.com/track/2ynEsP0aHj79tscatzkCbh?si=3e03299ebeb24be8",
		"https://open.spotify.com/track/716uhQk1kzI8532MYJ7aA7?si=84a9f5f5dc424ec1",
		"https://open.spotify.com/track/2Cel3W10xXpUU6fEq1qSRj?si=4787c9f6fdad4106",
		"https://open.spotify.com/track/6LLyiqMoNoex4Zu0ka4iF2?si=f44a9dca2d5644c8",
		"https://open.spotify.com/track/6CUgyhYhI4iNsL63z5Y28i?si=49ba56e53f574873",
		"https://open.spotify.com/track/0KKkJNfGyhkQ5aFogxQAPU?si=d91ac294649b494e",
		"https://open.spotify.com/track/6IzBszbsoMH6Abdx8qI5Is?si=0d39ee9e583b43ff",
		"https://open.spotify.com/track/6ZmYAh3IKPMupbPHlA7Sjo?si=ccb0f53cffd14a0b",
		"https://open.spotify.com/track/3syh856Vm0yXIbT0nwK7PN?si=a47f82e1089949d9",
		"https://open.spotify.com/track/740KtWw1r4f5Gd6UXzhYNp?si=a636e6903c754b47",
		"https://open.spotify.com/track/4BbKqJOcUu0dMAdzKswmXs?si=265550f27bf840ce",
		"https://open.spotify.com/track/3OXHwY8gI2QUh0QliXBwrI?si=f81547c4e4274bde",
		"https://open.spotify.com/track/2PYGSOOoteALibgx1ALIgH?si=df44e68e9f974b2e",
		"https://open.spotify.com/track/23dZfNKGEsPJvdsk5w5Ly2?si=5be4cdce8def43eb",
		"https://open.spotify.com/track/3x0nAQqT78NF9ePWpQkiMO?si=d728ed88cda940fe",
		"https://open.spotify.com/track/3OXHwY8gI2QUh0QliXBwrI?si=e7008ba5549e40f2",
		"https://open.spotify.com/track/4avggvXPPeBVFuxaH1T5aB?si=d830471797754159",
		"https://open.spotify.com/track/6hzmRh7vU6yWQWzhlB2t4P?si=83acee28b69047df",
		"https://open.spotify.com/track/3OXHwY8gI2QUh0QliXBwrI?si=34290d3424b54973",
		"https://open.spotify.com/track/57FcbS9KNbuMWa1FA30Lp6?si=a265bc3ef81a4d39",
		"https://open.spotify.com/track/3s7TGJ9jaG2JnVu3jYtYSS?si=be1b750a4d3b4153",
		"https://open.spotify.com/track/632VyMrvhsHIsO4zq9khts?si=3177597195fd4f42",
		"https://open.spotify.com/track/5eV5aLGogtSwDLKgHdkKRb?si=c648036d042c4aec",
		"https://open.spotify.com/track/4ymuPowtkCWZ6TzFA21qEl?si=db511a3ff72242b7",
		"https://open.spotify.com/track/5Eaw8UqiDIDYyFBqOquVXJ?si=6f0cd52214a34423",
		"https://open.spotify.com/track/4KBegMBVyHsfC7fPOztTzV?si=f6dd8087e10d4389",
		"https://open.spotify.com/track/4nF5p1V5VRgls1lSzzAZ88?si=aa22233282264085",
		"https://open.spotify.com/track/2aMN1ky0SzSEcV1QdBYbW9?si=c4512aa54fa24a05",
		"https://open.spotify.com/track/2VCl8jXHfealmpgfxVn0jn?si=4da513e47fc14f46",
		"https://open.spotify.com/track/73eCSQ1DxQbaOnzy8PhKx3?si=4217431ec398419e",
		"https://open.spotify.com/track/4sxGX1tCfmno7InnRohPxL?si=c9269995eb204830",
		"https://open.spotify.com/track/101iWa6yaODTI0RWewMK1B?si=ad397bd686404494",
		"https://open.spotify.com/track/5M1mL0Ya6pbp0VJGT2OSVT?si=386686087be745c1",
		"https://open.spotify.com/track/3HH9pAwNfQVXYVUbmHxWwn?si=ba6ec9ea65434462",
		"https://open.spotify.com/track/34ym6ChBJufR0mlMyUu1we?si=77a48500b552475b",
		"https://open.spotify.com/track/0pzyN7Uy0bmDSsTs0iHuSC?si=53a0e91a6c2b4101",
		"https://open.spotify.com/track/1kEbEoz2MJqapQSGXefXhc?si=647a43c5ed934b13",
		"https://open.spotify.com/track/5DvxSuBFIRQJtBeUQMuDXd?si=8c07395e99f64cd5",
		"https://open.spotify.com/track/5xbOj9XdtLTFAyb5Wtb63R?si=958bbe66bb19478d",
		"https://open.spotify.com/track/5R1bjCYaGpl6eZS2W2qfov?si=ccf80e5fb4a9426d",
		"https://open.spotify.com/track/5eyGVcR4S0NA9ZeyL5JnNO?si=1b7e4def8c0e44c4",
		"https://open.spotify.com/track/5071fuvHFQ8ZYOT0SMdn4N?si=713367aed8a54c3b",
		"https://open.spotify.com/track/6LLyiqMoNoex4Zu0ka4iF2?si=f44a9dca2d5644c8",
		"https://open.spotify.com/track/2W1V64GhT2gfCCRoot5aar?si=2eec4a70f0024381",
		"https://open.spotify.com/track/79XqEntClgg9RH2iWrmrqp?si=6ae1096a4ed242b8",
		"https://open.spotify.com/track/7ENyyu1bbuqaIG3V1Jr73X?si=e1c6cf9cf0cb4cfe",
		"https://open.spotify.com/track/36fmIljo8kkBcB0oYvXcLC?si=75282fc19aa94d80",
		"https://open.spotify.com/track/2Qq7GzCe94dOAOPMvK2AzE?si=7378a3de19db4529",
		"https://open.spotify.com/track/65vVLwADGFsIR9MlYdQH7K?si=7d2fb6cf9a9b40d8",
		"https://open.spotify.com/track/0c3JZG01M912iGPeoOwuhe?si=f446b93ae7c743f1",
		"https://open.spotify.com/track/3ulBp880DxkhYImcPxw2i5?si=06d120e2cbd14b60",
		"https://open.spotify.com/track/5eY1A4xxaeFeJlwNHygAN8?si=5f71af2b5435485a",
		"https://open.spotify.com/track/0GprXtBfKxJBkfqCKe6PQm?si=f7adb50dc1db4064",
		"https://open.spotify.com/track/3WozQKP0j1TvdvLXhj5lvU?si=b75609c6548945df",
		"https://open.spotify.com/track/3jp4CFFqUSo8dTJ9icCx4l?si=deed1761ea2140ba",
		"https://open.spotify.com/track/4lWruqkKSa28BHajiKzQFh?si=d8dad814c8914fda",
		"https://open.spotify.com/track/3OXHwY8gI2QUh0QliXBwrI?si=4b57cbb613f44711",
		"https://open.spotify.com/track/5YHYLmdhMjx5xzju52rvQD?si=bde0571e2a634149",
		"https://open.spotify.com/track/1b3mJ1pQl9s1zz9SXMmm3i?si=ef53071087f241e0",
		"https://open.spotify.com/track/7dZGFzoDI4QHMEOjuFiNOt?si=c932d58199b141f7",
		"https://open.spotify.com/track/5ZDWZKt8BCJRxTj5zQK9SE?si=d93ad4c93278457f",
		"https://open.spotify.com/track/0pzyN7Uy0bmDSsTs0iHuSC?si=53a0e91a6c2b4101",
		"https://open.spotify.com/track/3bv43QaoyJfuyTLuGEHyU1?si=6aa4603f1a5e4b4c",
		"https://open.spotify.com/track/0pzyN7Uy0bmDSsTs0iHuSC?si=305b923572ce4237",
		"https://open.spotify.com/track/0ag9VPDTOEsgD5j5Hm2WBm?si=e9abdfded6f54a07",
		"https://open.spotify.com/track/34rNonM7x3cyyooQ5QXYhl?si=1d374f934ffe4903",
		"https://open.spotify.com/track/126sFLTpIW0IlvuRPVNB95?si=72c426ac6eea476c",
		"https://open.spotify.com/track/4X3gYJeL8m1huVLZkIkLGV?si=2f2e8e899f24429d",
		"https://open.spotify.com/track/0K0iKULxAnPIKusAW3Siuj?si=30122a7e85dd40cd",
		"https://open.spotify.com/track/2XXjHBhHR8Epach2N3HBf4?si=960279e270c449d7",
		"https://open.spotify.com/track/0e0xH7S6AiHiZOSeYJTNqH?si=947a984e9e694746",
		"https://open.spotify.com/track/5SEOTzCsR3tkDHbCSl8OyE?si=15ff97b82a2340bb",
		"https://open.spotify.com/track/3OXHwY8gI2QUh0QliXBwrI?si=4b57cbb613f44711",
		"https://open.spotify.com/track/5gpww2Kr4SW1v6NhJ2CebD?si=58daa311e1b8474f",
		"https://open.spotify.com/track/7sfOrmYdSYpIZJBOK4IJF9?si=af015f2db5894761",
		"https://open.spotify.com/track/6DczfkAhikNrYryp5vyRnW?si=a7daa1c7e9cf43c5",
		"https://open.spotify.com/track/6M5l0l6egq8IiHITIwJtnF?si=ca25c088cabe4705",
		"https://open.spotify.com/track/0CUNKIlXEHFoQG3ePClG2n?si=7d33d24c51094431",
		"https://open.spotify.com/track/3G5A0gS6WxDD3qvhN6AmHu?si=28412e5fef074595",
		"https://open.spotify.com/track/6LLyiqMoNoex4Zu0ka4iF2?si=2d97fe1790794804",
		"https://open.spotify.com/track/3p0jSLMv7Wp2D0Exe6V5t6?si=d1e8f58935094173",
		"https://open.spotify.com/track/17oOACDbDuyVI1S8rjnnvZ?si=6408a3e2cb3e4afe",
		"https://open.spotify.com/track/34fFKAvFIdbI7HD90BQEqg?si=847e1fb1a53f4151",
		"https://open.spotify.com/track/16qsrWJsn9a5kbvs7OAgj3?si=8c2f8e66d7014d4c",
		"https://open.spotify.com/track/7DOacuTUvU8PoJyijGQ4MO?si=dadf4d1db47f42b7",
		"https://open.spotify.com/track/440LjB3Qs7P67RDQhRH8B7?si=e7149f0a799f4daa",
		"https://open.spotify.com/track/0HuETaYtsTF3nUPn3EVlBQ?si=a83f21179cef4ad0",
		"https://open.spotify.com/track/0pPlhZMdF6vRu4Wjxd5hcT?si=dc4cb0ff00b74730",
		"https://open.spotify.com/track/6A4wVKbcg0mRriCFjZzX0Z?si=e51ee0057a574613",
		"https://open.spotify.com/track/2l0lhEhOOM53BdNRlWgUmB?si=f1c45fa55cd54820",
		"https://open.spotify.com/track/3Tes0XUodHjwjoL4Z8kU8H?si=d09d984a2d054383",
		"https://open.spotify.com/track/7zGOVmhTrn1RzoujRFHv2e?si=cb63e123c8f64ec3",
		"https://open.spotify.com/track/5ZZwQy1wofQhj7LJDNLflT?si=946a849e0dc64dff",
		"https://open.spotify.com/track/5ZF8okz1tk5vLzYrK0AMgw?si=ce158ad3c2654343",
		"https://open.spotify.com/track/3nfzbH1p3oCEtZIohPkLdJ?si=a04c9d73287e4c71",
		"https://open.spotify.com/track/4ruGQ2XSvehHrfAMuyfvoS?si=f350d173b45e42c1",
		"https://open.spotify.com/track/7CTitzr4eVIDCPUJi5Dr4B?si=9849e752979d48ce",
		"https://open.spotify.com/track/3Shmm2SZQsZxRj8OkOtewe?si=82223898a35348a1",
		"https://open.spotify.com/track/5LCwPiEbQLBZRinLhnSJ4u?si=b49b5f8becab418a",
		"https://open.spotify.com/track/51Fno4GluxKhibrw1tR4Z0?si=5c74b56f6d814bdf",
		"https://open.spotify.com/track/440LjB3Qs7P67RDQhRH8B7?si=5b3cff0516784fbc",
		"https://open.spotify.com/track/3OXHwY8gI2QUh0QliXBwrI?si=1b3f1df9963b4480",
		"https://open.spotify.com/track/5SEOTzCsR3tkDHbCSl8OyE?si=705419ee7f1547eb",
		"https://open.spotify.com/track/4qijullhDLnh7GplpQgOGK?si=be6cf7b3e8f5470e",
		"https://open.spotify.com/track/0n0IaugHVlZgBDDpNx0fjh?si=a3303a828b8b4453",
		"https://open.spotify.com/track/5dySIJXOLi6sttkybVDSia?si=eb75f8bb1ecc4031",
		"https://open.spotify.com/track/7BxRGUJk9ArTRBZ70HGC0n?si=89558e3d37174da3",
		"https://open.spotify.com/track/5653mRfv5aBtXP6DSA8T1Q?si=3adb2255266f4ced",
		"https://open.spotify.com/track/1LE1T8bq6deSH1kpcjmnly?si=45ab80b2ac824a59",
		"https://open.spotify.com/track/6NMAc7Hz5rOW2IUw7dqEBO?si=7ba0303843e14925",
		"https://open.spotify.com/track/7CfJtcc9ubR436uztXuvym?si=fb7ae7b926494164"
	]
}
'''

parsed_json = json.loads(json_data)

userPwdList = [
    ( parsed_json["users"][0]["email"], parsed_json["users"][0]["password"]),
    #('szipan2@gmail.com', 'Zaq!2wsxcde3'),
]

#print(userPwdList)

processNum = len(userPwdList)              # 同时登录的账号数量

urlsList = parsed_json["urls"]
#print(urlsList)

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
    #chrome_options.set_headless()
    chrome_options.add_argument("--headless") 
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
                print('登录失败！ 放弃账号：%s  URL:%s' % (uEmail, urlStr))
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

    print('All tasks completed！')
    fo = open(currentDirectory + '/music_play_count.txt', 'w')
    for i in range(len(urlsList)):
        song = SpotifySongModel.get('url%d' % i)
        print('URL: %s  Count: %s' % (urlsList[i], song.playCount))
        fo.write('URL: %s  Count: %s\n' % (urlsList[i], song.playCount))

    fo.close()

if __name__ == "__main__":
    asyncio.run(main())
