import json

import openai
import requests
from config import API_KEY_GPT

def get_rewiew_recall(recall):



    prompt = f'''Сделай рерайт текста со 100% уникальностью
                Полностью перепиши текст
                Перепиши текст, используя синонимы:"\n{recall}"'''

    URL = "https://api.openai.com/v1/chat/completions"

    headers = {"Authorization": f"Bearer {API_KEY_GPT}"}

    data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
    proxy = {'http': 'http://VeG8yC:yv7buh3AH7ba@hproxy.site:12683',
             'https': 'http://VeG8yC:yv7buh3AH7ba@hproxy.site:12683'}
    result = requests.post(URL, headers=headers, json=data, proxies=proxy)
    response = result.json()
    result = response['choices'][0]['message']['content']
    return result


def get_rewiew_recall_1(recall):



    prompt = f'''Перепиши: "\n{recall}"'''

    URL = "https://api.openai.com/v1/chat/completions"

    headers = {"Authorization": f"Bearer {API_KEY_GPT}"}

    data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
    proxy = {'http': 'http://VeG8yC:yv7buh3AH7ba@hproxy.site:12683',
             'https': 'http://VeG8yC:yv7buh3AH7ba@hproxy.site:12683'}
    result = requests.post(URL, headers=headers, json=data, proxies=proxy)
    response = result.json()
    result = response['choices'][0]['message']['content']
    return result

# использую это
def get_rewiew_recall_4(recall,list_nice_proxy):


    for nice_proxy in list_nice_proxy:
        try:
            prompt = f'''Сделай полный рерайт текста, сохраняя стилистику\n"\n{recall}"'''

            URL = "https://api.openai.com/v1/chat/completions"

            headers = {"Authorization": f"Bearer {API_KEY_GPT}"}

            data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                }
            proxy = {'http': f'http://{nice_proxy}',
                     'https': f'http://{nice_proxy}'}
            result = requests.post(URL, headers=headers, json=data, proxies=proxy)
            response = result.json()
            result = response['choices'][0]['message']['content']
            return result
        except:
            continue
# использую это

def partly_rewrite(recall,list_nice_proxy):
    for nice_proxy in list_nice_proxy:
        try:
            prompt = f'''Сделай частичный рерайт текста, сохраняя стилистику\n"\n{recall}"'''

            URL = "https://api.openai.com/v1/chat/completions"

            headers = {"Authorization": f"Bearer {API_KEY_GPT}"}

            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
            proxy = {'http': f'http://{nice_proxy}',
                     'https': f'http://{nice_proxy}'}
            result = requests.post(URL, headers=headers, json=data, proxies=proxy)
            response = result.json()
            result = response['choices'][0]['message']['content']
            return result
        except:
            print(nice_proxy + 'Не рабочая')
            continue