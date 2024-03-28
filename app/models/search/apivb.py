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


async def find_popular_films():
    url = "https://api.kinopoisk.dev/v1.4/movie/random?lists=top250"

    headers = {
        "X-API-Key": "VBZ63SW-PFHMYEM-M3384F6-X6BXVSY",
        "accept": "application/json"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 200:

                    movies = await response.json(content_type=None)
                    movies['id'] = f"kp{movies['id']}"

                    trailers = movies.get('videos', {}).get('trailers', [])
                    trailer_url = trailers[0].get('url')
                    movies['trailer_url'] = trailer_url

                    return movies
        return []
    except Exception as e:
        print(e)
        return []


async def popular_films():
    url = "https://api.kinopoisk.dev/v1.4/movie?page=1&limit=25&lists=top250"
    headers = {
        "X-API-Key": "VBZ63SW-PFHMYEM-M3384F6-X6BXVSY",
        "accept": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    popular = await response.json(content_type=None)
                    return popular
        return []
    except Exception as e:
        print(e)
        return []