import re
import aiohttp
from config import api_hbtv


async def fetch_movies(query: str):
    try:
        kp_link_match = re.match(r'https?://www\.kinopoisk\.ru/(series|film)/(\d+)', query)
        if kp_link_match:
            kp_id = kp_link_match.group(2)
            url = f"https://apivb.info/api/videos.json?id_kp={kp_id}&token={api_hbtv}"
        else:
            kp_match = re.match(r'kp(\d+)', query)
            if kp_match:
                kp_id = kp_match.group(1)
                url = f"https://apivb.info/api/videos.json?id_kp={kp_id}&token={api_hbtv}"
            else:
                url = f"https://apivb.info/api/videos.json?title={query}&token={api_hbtv}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    movies = await response.json(content_type=None)
                    return movies
        return []
    except Exception as e:
        print(e)
        return []