import asyncio

import aiohttp

from warnings import warn


with open("vk_access_token.txt", mode="r") as file:
    vk_access_token = file.read()
vk_api_version = "5.154"
owner_id = "-160464793"
url = f"https://api.vk.ru/method/wall.get?v={vk_api_version}&owner_id={owner_id}&count=1&access_token={vk_access_token}"


async def get_last_text_message():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            a = await response.json()
            try:
                a = a["response"]["items"][0]["text"]
            except:
                a = None
            return a


async def ticker(delay):
    while True:
        yield await get_last_text_message()
        await asyncio.sleep(delay)


async def set_morning_trigger(trigger_function, delay=30):
    if delay < 28:
        warn("The delay is too small. Limit of wall.get usage per day may be exceeded.")
    generator = ticker(delay)
    async def get_last_text():
        return await generator.asend(None)
    text = ""
    while True:
        new_text = await get_last_text()
        if new_text != None and text != new_text:
            text = new_text
            asyncio.gather(trigger_function(text))


if __name__ == "__main__":
    async def function(string):
        print(string)
    asyncio.run(set_morning_trigger(function))
