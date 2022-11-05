import os
from hoshino import aiorequests,logger
import json

server = "https://raw.githubusercontent.com/SonderXiaoming/pcr_strategy/main"

local_path = os.path.join(os.path.dirname(__file__), 'data')

def load_config(path) -> int:
    try:
        with open(path, encoding='utf8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        logger.exception(e)
        return {}

async def create_path(path):
    folder = os.path.exists(path)
    if not folder:                 
        os.makedirs(path)

async def download_json(url):
    resp = await aiorequests.get(url)
    if resp.status_code == 200:
        return await resp.json()

async def download_pic(url):
    logger.info(f"正在下载{url}")
    resp = await aiorequests.head(url)
    content_length = int(resp.headers["Content-Length"])
    #logger.info(f"块大小{str(content_length)}")
    #分割200kb下载
    block_size = 1024*200
    range_list = []
    current_start_bytes = 0
    while True:
        if current_start_bytes + block_size >= content_length:
            range_list.append(f"{str(current_start_bytes)}-{str(content_length)}")
            break
        range_list.append(f"{str(current_start_bytes)}-{str(current_start_bytes + block_size)}")
        current_start_bytes += block_size + 1
    pic_bytes_list = []
    for block in range_list:
        #logger.info(f"正在下载块{block}")
        headers = {"Range":f"bytes={block}"}
        resp = await aiorequests.get(url,headers = headers)
        res_content = await resp.content
        pic_bytes_list.append(res_content)
    return b"".join(pic_bytes_list)

async def update_data(type:str,force_update:bool):
    config_url = f"{server}/{type}/route.json"
    config = await download_json(config_url)
    if config:
        await create_path(local_path)
        save_path = os.path.join(local_path, type)
        await create_path(save_path)
        with open(os.path.join(save_path,'route.json'),"w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False)
        for strategy in config:
            images = strategy["image"]
            for image in images:
                if not force_update:
                    if os.path.exists(os.path.join(save_path,f'{image}')):
                        continue
                img_url = f"{server}/{type}/{image}"
                img_content = await download_pic(img_url)
                with open(os.path.join(save_path,f'{image}'),"ab") as fp:
                    fp.seek(0)
                    fp.truncate()
                    fp.write(img_content)


