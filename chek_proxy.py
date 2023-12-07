from bs4 import BeautifulSoup
import get_proxy_list
import requests
import aiohttp
import asyncio

nice_proxy = []
async def check_proxy(session, proxy2):
    global nice_proxy
    url = 'http://icanhazip.com/'
    # proxy_for_check = {'http': f'http://{proxy2}',
    #                    'https': f'http://{proxy2}'}
    proxy_for_check = f'http://{proxy2}'
    try:
        async with session.get(url, proxy=proxy_for_check) as response:
            if response.status == 200:
                nice_proxy.append(proxy2)
                print(nice_proxy)
                return True
    except:
        pass


#
async def create_tasks(list_proxy):
    async with aiohttp.ClientSession() as session:

        tasks = []
        for proxy in list_proxy:
            task = asyncio.create_task(check_proxy(session, proxy))
            tasks.append(task)
        print('Запускаю чекер')
        await asyncio.gather(*tasks)


def get_proxy():
    print('Получаю прокси')
    list_proxy = get_proxy_list.get_proxy_list()
    asyncio.run(create_tasks(list_proxy))
    print(f'Получил {len(nice_proxy)} рабочих прокси')
    print(nice_proxy)
    return nice_proxy
