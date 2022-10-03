import os
import random
import time, json, requests
from bs4 import BeautifulSoup

def get_my_ip():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4,my;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://www.ip138.com/',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get('https://2022.ip138.com/', headers=headers)
    soup = BeautifulSoup(response.text)
    ip = soup.title.text.split('：')[1]
    return ip

def connect_ADSL(name,username,password):
    cmd_string = f'rasdial {name} {username} {password}'
    flag = os.system(cmd_string)
    print('flag:', flag)
    # if flag == 0:
    #     time_sum = random.randint(3, 16)
    #     m = time_sum
    #     while m > 0:
    #         print("time_sum", m)
    #         m -= 1
    #         os.system('ping www.baidu.com')
    #         time.sleep(1)


def disconnect_ADSL(name):
    cmd_string = f'rasdial {name} /disconnect'
    os.system(cmd_string)


def adsl(account, password):
    disconnect_ADSL('宽带连接')
    time.sleep(5)
    connect_ADSL('宽带连接', account, password)
    time.sleep(10)
    

if __name__ == '__main__':
    account = '134xxxxxxxx'
    password = 'xxxxxx'
    adsl(account, password)
    ips = json.load(open('ips', encoding='utf-8'))
    try:
        current_ip = get_my_ip()
    except:
        print('无法获取公网ip')
        time.sleep(10)
    if current_ip not in ips:
        ips.append(current_ip)
        json.dump(ips, open('ips', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    else:
        print('无用ip')
        time.sleep(10)