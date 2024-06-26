import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1

def trim_title(title: str):
    title = title.replace("Go Go Loser Ranger S01E01 We Are Justice The Dragon Keepers 1080p DSNP WEB-DL AAC2.0 H 264-VARYG (Sentai Daishikkaku, Multi-Subs)", "Sentai Daishikkaku - 01")
    title = title.replace("Go Go Loser Ranger S01E02 Go Fighter D 1080p DSNP WEB-DL AAC2.0 H 264-VARYG (Sentai Daishikkaku, Multi-Subs)", "Sentai Daishikkaku - 02")
    title = title.replace("Go Go Loser Ranger S01E04 The Soldier With Love Hibiki 1080p DSNP WEB-DL AAC2.0 H 264-VARYG (Sentai Daishikkaku, Multi-Subs)", "Sentai Daishikkaku - 04")
    title = title.replace("Go Go Loser Ranger S01E03 Our Evil Will Bloom Someday 1080p DSNP WEB-DL AAC2.0 H 264-VARYG (Sentai Daishikkaku, Multi-Subs)", "Sentai Daishikkaku - 03")
    title = title.replace("Dead Mount Death Play 2nd Cour", "Dead Mount Death Play Part 2")
    title = title.replace(" (CA)", "")
    title = title.replace(" (JA)", "")
    title = title.replace("Tian Guan Ci Fu Di Er Ji", "Heaven Official's Blessing S2")
    title = title.replace("(AAC 2.0) ", "")
    ext = ".mkv"
    title = title + ext
    return title



def parse():
    a = feedparser.parse("https://nyaa.si/?page=rss&u=varyg1001&q=sentai")
    b = a["entries"]
    data = []    

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['size'] = i['nyaa_size']   
        item['link'] = "magnet:?xt=urn:btih:" + i['nyaa_infohash']
        data.append(item)
        data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                if ".mkv" in i["title"] or ".mp4" in i["title"]:
                    title = i["title"]
                    await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        await asyncio.sleep(60)
