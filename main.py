from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import db
import gpt
import random
import chek_proxy
def check_review(dict_for_check):
    driver = webdriver.Chrome()
    for count in dict_for_check:
        url = dict_for_check[count]['url']
        recall = dict_for_check[count]['recall']
        driver.get(url=url)
        time.sleep(5)
        try:
            driver.find_element(By.XPATH, '//div[text()="Отзывы"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//button[@aria-expanded="false"]').click()
            time.sleep(2)
            try:
                driver.find_element(By.XPATH,"//div[text()='Сначала новые']/../..").click()
                time.sleep(2)
            except:
                driver.find_element(By.XPATH, '//div[text()="Самые релевантные"]').click()
                time.sleep(2)
                driver.find_element(By.XPATH,"//div[text()='Сначала новые']/../..").click()
                time.sleep(2)
        except Exception as ex:
            print(ex, url, recall)
        len_recall_2 = len(recall)/2
        src = driver.page_source
        if any([recall in src,
                recall[:int(len_recall_2)] in src]):
            db.set_status_proverka(dict_for_check[count])
            print(f'!Отзыв: {recall}! найден')
        else:
            db.set_new_date(dict_for_check[count])
            print(f'Отзыва {recall} не найден')
    driver.close()
    driver.quit()


def re_check_review(dict_for_check):
    driver = webdriver.Chrome()
    for count in dict_for_check:
        url = dict_for_check[count]['url']
        recall = dict_for_check[count]['recall']
        driver.get(url=url)
        time.sleep(5)
        try:
            driver.find_element(By.XPATH, '//div[text()="Отзывы"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//button[@aria-expanded="false"]').click()
            time.sleep(2)
            try:
                driver.find_element(By.XPATH,"//div[text()='Сначала новые']/../..").click()
                time.sleep(2)
            except:
                driver.find_element(By.XPATH, '//div[text()="Самые релевантные"]').click()
                time.sleep(2)
                driver.find_element(By.XPATH,"//div[text()='Сначала новые']/../..").click()
                time.sleep(2)
        except Exception as ex:
            print(ex, url, recall)
        len_recall_2 = len(recall)/2
        src = driver.page_source
        if any([recall in src,
                recall[:int(len_recall_2)] in src]):
            db.set_status_gotovo(dict_for_check[count])
            print(f'!Отзыв: {recall}! на месте')
        else:
            db.set_new_slet(dict_for_check[count])
            print(f'Отзыва {recall} слетел')
    driver.close()
    driver.quit()

def rewrite_recall(dict_for_rewrite):
    # list_nice_proxy = chek_proxy.get_proxy()
    list_nice_proxy = ['VeG8yC:yv7buh3AH7ba@hproxy.site:12683']
    for _ in dict_for_rewrite:
        random_int = random.randint(0, 1)
        if random_int == 0:
            recall = dict_for_rewrite[_]['recall']
            new_recall = gpt.get_rewiew_recall_4(recall, list_nice_proxy)
            db.set_new_recall(new_recall, dict_for_rewrite[_]['id_review'], '100%')
            print(f"Отзыв №{dict_for_rewrite[_]['id_review']} переписан полностью")
        if random_int == 1:
            recall = dict_for_rewrite[_]['recall']
            new_recall = gpt.partly_rewrite(recall, list_nice_proxy)
            db.set_new_recall(new_recall, dict_for_rewrite[_]['id_review'], '50%')
            print(f"Отзыв №{dict_for_rewrite[_]['id_review']} переписан частично")


if __name__ == '__main__':

    dict_for_check = db.get_rewiews_for_check()
    print('Начинаю проверять отзывы')
    check_review(dict_for_check)
    print('Начинаю перепроверять прошлые отзывы')
    dict_for_re_check = db.recheck()
    re_check_review(dict_for_re_check)

    dict_for_rewrite = db.get_recalls_for_rewrite()
    print('Начинаю переписывать отзывы')
    rewrite_recall(dict_for_rewrite)
