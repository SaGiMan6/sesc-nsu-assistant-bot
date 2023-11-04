import asyncio

import aiohttp

from bs4 import BeautifulSoup


url = "https://vk.com/wall-160464793?offset=0&own=1"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}


async def get_last_text_message():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, features="lxml")
            soup = soup.select_one(".poster__text,.wall_post_text")
            if soup == None:
                return
            else:
                return soup.text


async def ticker(delay):
    while True:
        yield await get_last_text_message()
        await asyncio.sleep(delay)


async def set_morning_trigger(trigger_function, delay=10):
    generator = ticker(delay)
    async def get_last_text():
        return await generator.asend(None)
    text = ""
    while True:
        new_text = await get_last_text()
        if new_text != None and text != new_text:
            text = new_text
            asyncio.gather(trigger_function(text))


if __name__ == '__main__':
    async def function(string):
        print(string)
    asyncio.run(set_morning_trigger(function))
