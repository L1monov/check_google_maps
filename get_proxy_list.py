
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_proxy_list():
    driver = webdriver.Chrome()
    url = 'http://free-proxy.cz/ru/'
    driver.get(url=url)
    page_source = driver.page_source
    with open('index.html','w', encoding='utf-8') as file:
        file.write(page_source)
    soup = BeautifulSoup(page_source, 'lxml')
    proxys = soup.find('table',{'id':'proxy_list'}).find('tbody').find_all('tr')
    list_proxy = []

    for proxy in proxys:
        try:
            ip_proxy = proxy.find('td').text.strip()
            port_proxy = proxy.find('span', {'class':'fport'}).text.strip()
            list_proxy.append(f'{ip_proxy}:{port_proxy}')
        except:
            continue

    driver.close()
    driver.quit()
    return list_proxy

