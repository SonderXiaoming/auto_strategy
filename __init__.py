from hoshino import Service
from hoshino.priv import check_priv,SUPERUSER
from .download import update_data,load_config,local_path
from nonebot import scheduler
import os
from nonebot import MessageSegment

type_list = ['rank','activity','equipment','half_month','gocha','dragon','strength']

sv_help = '''
指令：
rank
活动攻略/sp/vh
刷图推荐
半月刊
千里眼
地下城
屯体
更新攻略缓存
'''.strip()

sv = Service("攻略", help_=sv_help, bundle="pcr查询")

def general_info(config,type_set):
    msg = ''
    for strategy in config:
        if strategy['text']:
            msg += strategy['text'] + '\n'
        for image in strategy['image']:
            image_path = os.path.join(local_path,f'{type_set}',image)
            msg += str(MessageSegment.image(f'file:///{image_path}')) + '\n'
    return msg

@sv.on_rex(r"^(陆|国|b)?((?i)rank|品级)表?$")
async def rank(bot, ev):
    type = 'rank'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_rex(r"^((活动(攻略|图)?)|(?i)sp|(?i)vh)$")
async def activity(bot, ev):
    type = 'activity'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_rex(r"^(刷图|装备)(推荐|攻略)?$")
async def equipment(bot, ev):
    type = 'equipment'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_rex(r"^半月刊|大记事|日历$")
async def half_month(bot, ev):
    type = 'half_month'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_rex(r"^(千|万)里眼$")
async def gocha(bot, ev):
    type = 'gocha'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_rex(r"^地下城|ex(\d{1})?$")
async def dragon(bot, ev):
    type = 'dragon'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_rex(r"^(屯|存|囤)体$")
async def save_strength(bot, ev):
    type = 'strength'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await bot.send(ev, msg)
    else:
        await bot.send(ev, "请先发送【更新攻略缓存】")

@sv.on_fullmatch("更新攻略缓存")
async def update_cache(bot, ev):
    if not check_priv(ev, SUPERUSER):
        await bot.send(ev, "仅有SUPERUSER可以使用本功能")
        return
    for type in type_list:
        try:
            await update_data(type,True)
        except:
            await bot.send(ev, f"{type}更新失败")
    await bot.send(ev, "更新完成")

@scheduler.scheduled_job('cron', hour='17', minute='06')
async def schedule_update_rank_cache():
    for type in type_list:
        try:
            await update_data(type,False)
        except:
            pass
