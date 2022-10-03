import re
import io, sys, re, os
import time
import numpy as np
from PIL import Image
import time
import base64
import sys
import requests, json, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
import pickle
import requests
import subprocess, os, random
import undetected_chromedriver as uc

from dial import adsl, get_my_ip

# 代理，不用代理则定义为空字符串，proxy = ''
proxy = '127.0.0.1:7890'
# 信用卡号
card_num = ''
# 信用卡过期月
card_expiry_month = '05'
# 信用卡过期年
card_expiry_year = '2030'
# 信用卡CVV
card_cvn = ''
# 信用卡类型(各国登录页面不同，cn页面002为master card)
card_type = "card_type_002"
# 注册邮箱
email = ''
# 注册地
reg_location = '中国'
# 服务器所在地
server_location = 'South Korea North (Chuncheon)'
# 密码
acc_password = '123passwordX!'


class Oracle(object):
    def __init__(self):
        chrome_options = self.options()
        # self.browser = webdriver.Chrome(options=chrome_options)
        self.browser = uc.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        # self.url = "https://www.oracle.com/cn/cloud/free/"
        self.url = "https://signup.cloud.oracle.com/?language=cn&sourceType=:ow:o:p:feb:0916FreePageBannerButton&intcmp=:ow:o:p:feb:0916FreePageBannerButton"

    def __del__(self):
        self.browser.close()

    def options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        
        # 添加代理
        if proxy:
            chrome_options.add_argument('--proxy-server=socks5://' + proxy)
        
        return chrome_options

    def get_cn_identity(self):
        headers = {
            'authority': 'www.meiguodizhi.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4,my;q=0.3',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            'origin': 'https://www.meiguodizhi.com',
            'referer': 'https://www.meiguodizhi.com/cn-address',
            'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        }

        json_data = {
            'city': '',
            'path': '/cn-address',
            'method': 'refresh',
        }

        response = requests.post('https://www.meiguodizhi.com/api/v1/dz', headers=headers, json=json_data).json()['address']
        Address = response['Address']
        Telephone = response['Telephone'].split()[1]
        City = response['City']
        Zip_Code = response['Zip_Code']
        State = response['State']
        Full_Name = response['Full_Name']
        firstName = Full_Name[:1]
        lastName = Full_Name[1:]
        State = response['State']
        return firstName, lastName, email, Address, City, State, Zip_Code, Telephone
        
    def click(self, xpath):
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    
    def sign_up(self):        
        self.browser.get(self.url)
        self.click("//div[text()='国家/地区']")
        self.click(f"//div[text()={reg_location}]")
        firstName, lastName, email, Address, City, State, Zip_Code, Telephone = self.get_cn_identity()
        time.sleep(1)
        self.browser.find_element_by_name('firstName').send_keys(firstName)
        time.sleep(1)
        self.browser.find_element_by_name('lastName').send_keys(lastName)
        time.sleep(1)
        self.browser.find_element_by_name('email').send_keys(email)
        
        # 解决人机验证
        iframe = self.browser.find_element_by_xpath('//iframe[@title="widget containing checkbox for hCaptcha security challenge"]')
        self.browser.switch_to.frame(iframe)
        self.browser.find_element_by_id('checkbox').click()
        
        reg_url = input('输入reg_url:')
        self.browser.get(reg_url)
        time.sleep(20)
        
        # 填写个人信息
        time.sleep(1)
        self.browser.find_element_by_name('alternateName').send_keys(''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], 5)))
        time.sleep(1)
        self.browser.find_element_by_name('password').send_keys(acc_password)
        time.sleep(1)
        self.browser.find_element_by_name('matchPassword').send_keys(acc_password)
        time.sleep(1)
        self.click('//*[@id="individual-customer-radio"]')
        time.sleep(2)
        self.click("//div[text()='主区域']")
        time.sleep(2)
        self.click(f"//div[text()={server_location}]")
        time.sleep(2)
        self.click('//*[@id="main"]/div/div[2]/div/div/div[2]/button')
        time.sleep(2)
        
        # 填写地址
        time.sleep(1)
        self.browser.find_element_by_name('address1').send_keys(Address)
        time.sleep(1)
        self.browser.find_element_by_name('city').send_keys(City)
        time.sleep(1)
        self.browser.find_element_by_name('province').send_keys(State)
        time.sleep(1)
        self.browser.find_element_by_name('postalcode').send_keys(Zip_Code)
        time.sleep(1)
        self.browser.find_element_by_name('电话号码').send_keys(Telephone)
        time.sleep(1)
        self.click('//*[@id="main"]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/form/button')
        
        # 添加付款方式
        time.sleep(1)
        self.click('//*[@id="main"]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/button')
        time.sleep(10)
        
        self.browser.switch_to.default_content()
        iframe = self.browser.find_element_by_xpath('//iframe[@id="opayifrm"]')
        self.browser.switch_to.frame(iframe)
        self.browser.find_element_by_id('ps-cc-button').click()

        
        time.sleep(2)
        self.browser.switch_to.default_content()
        iframe = self.browser.find_element_by_xpath('//iframe[@id="opayifrm"]')
        self.browser.switch_to.frame(iframe)
        iframe = self.browser.find_element_by_xpath('//iframe[@data-testid="paymentGateway"]')
        self.browser.switch_to.frame(iframe)
        time.sleep(1)
        self.click(f'//*[@id={card_type}]')
        time.sleep(1)
        
        
        self.browser.find_element_by_name('card_number').send_keys(card_num)
        
        time.sleep(1)
        card_expiry_month_ = self.browser.find_element_by_id('card_expiry_month')
        for option in card_expiry_month_.find_elements_by_tag_name('option'):
            if option.text.strip() == card_expiry_month:
                option.click() # select() in earlier versions of webdriver
                break
            
        card_expiry_year_ = self.browser.find_element_by_id('card_expiry_year')
        for option in card_expiry_year_.find_elements_by_tag_name('option'):
            if option.text.strip() == card_expiry_year:
                option.click() # select() in earlier versions of webdriver
                break
        
        time.sleep(1)
        self.browser.find_element_by_name('card_cvn').send_keys(card_cvn)
        time.sleep(1)
        try:
            self.browser.find_element_by_name('commit').click()
        except:
            pass
        
        time.sleep(10)
        iframe = self.browser.find_element_by_xpath('//iframe[@id="opayifrm"]')
        self.browser.switch_to.frame(iframe)
        self.browser.find_element_by_id('ps-success-close-button').click()
        

        # 切换为原始iframe
        self.browser.switch_to.default_content()
        
        time.sleep(1)
        self.browser.find_element_by_class_name('checkmark').click()
        time.sleep(1)
        self.browser.find_element_by_id('startMyTrialBtn').click()
        
        time.sleep(30)
        print('done')
        
if __name__ == '__main__':
    # oracle = Oracle()
    # oracle.sign_up()
    
    while True:
        # adsl()
        ips = json.load(open('ips', encoding='utf-8'))
        try:
            current_ip = get_my_ip()
        except:
            print('无法获取公网ip')
            time.sleep(10)
            continue
        if current_ip not in ips:
            oracle = Oracle()
            oracle.sign_up()
            
            # 把已用过的ip加入ips
            ips.append(current_ip)
            json.dump(ips, open('ips', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        else:
            print('无用ip')
            time.sleep(10)