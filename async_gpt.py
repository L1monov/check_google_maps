import db
from config import API_KEY_GPT
import requests
import aiohttp
import asyncio

async def partly_rewrite(session,list_nice_proxy, recall):
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
            proxy = f'http://{nice_proxy}'
            async with session.post(URL, headers=headers, json=data, proxy=proxy) as response:
                print('Получил ответ')
                response = await response.json()
                result = response['choices'][0]['message']['content']
                print(result)
                return result
        except:
            continue
    print(f'Отзыв не переписан')

async def create_tasks(list_proxy,date_recall):
    async with aiohttp.ClientSession() as session:

        tasks = []
        for _ in date_recall:
            recall = date_recall[_]['recall']
            task = asyncio.create_task(partly_rewrite(session, list_proxy,recall))
            tasks.append(task)
        print('Запускаю переписываение')
        print(len(tasks))
        await asyncio.gather(*tasks)

# if __name__ == '__main__':
#     date_recall = db.get_recalls_for_rewrite()
#     list_nice_proxy = ['191.101.80.162:80', '84.39.112.144:3128', '34.122.187.196:80', '155.94.241.133:3128',
#                        '75.89.101.62:80', '138.68.235.51:80', '204.188.255.67:4128', '47.88.62.42:80',
#                        '46.4.241.139:8888', '159.203.13.121:80', '70.38.0.96:4128', '204.188.255.68:4128',
#                        '70.38.0.98:4128', '162.223.94.163:80', '154.47.17.180:8080', '162.214.165.203:80',
#                        '108.170.12.14:80']
#
#     asyncio.run(create_tasks(list_nice_proxy,date_recall))
