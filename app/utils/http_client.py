import aiohttp

class HttpClient:
    async def get(self, url, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response

    async def post(self, url, json=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json) as response:
                return await response

    async def put(self, url, json=None):
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=json) as response:
                return await response

http_client = HttpClient()
