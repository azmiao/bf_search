import os
import shutil
from hoshino import Service, R
from .search import *

sv_help = '''=====功能=====
[战地1查询 角色昵称] 查询战地1信息
[战地4查询 角色昵称] 查询战地4信息
[战地5查询 角色昵称] 查询战地5信息'''.strip()

if os.path.exists(R.img('bf_search').path):
    shutil.rmtree(R.img('bf_search').path)  #删除目录，包括目录下的所有文件
    os.mkdir(R.img('bf_search').path)
else:
    os.mkdir(R.img('bf_search').path)

sv = Service('bf_search', help_=sv_help, enable_on_default=True, bundle='战地查询')
svcl = Service('bf_search_auto_clean', enable_on_default = True, help_='战地查询图片自动清理')

# 帮助界面
@sv.on_fullmatch("战地帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 图片自动清理
@svcl.scheduled_job('cron', hour='03', minute='00')
async def auto_clean():
    if os.path.exists(R.img('bf_search').path):
        shutil.rmtree(R.img('bf_search').path)
        os.mkdir(R.img('bf_search').path)
    else:
        os.mkdir(R.img('bf_search').path)

@sv.on_prefix('战地1查询')
async def search_info1(bot, ev):
    name = ev.message.extract_plain_text()
    msg_e = '正在从Gametool查询，预计5-10秒'
    await bot.send(ev, msg_e)
    msg = create_msg(name, 'bf1')
    if msg == 'gametool网站连接失败！':
        msg = msg + '\n由于API在国外所以有时可能链接不上，你可以尝试输入"战地帮助"采用用国内的K-ON的API查询'
    await bot.send(ev, msg)

@sv.on_prefix('战地4查询')
async def search_info4(bot, ev):
    name = ev.message.extract_plain_text()
    msg_e = '正在从Gametool查询，预计5-10秒'
    await bot.send(ev, msg_e)
    msg = create_bf4msg(name, 'bf4')
    if msg == 'gametool网站连接失败！':
        msg = msg + '\n由于API在国外所以有时可能链接不上，你可以尝试过会再查'
    await bot.send(ev, msg)

@sv.on_prefix('战地5查询')
async def search_info5(bot, ev):
    name = ev.message.extract_plain_text()
    msg_e = '正在从Gametool查询，预计5-10秒'
    await bot.send(ev, msg_e)
    msg = create_msg(name, 'bfv')
    if msg == 'gametool网站连接失败！':
        msg = msg + '\n由于API在国外所以有时可能链接不上，你可以尝试过会再查'
    await bot.send(ev, msg)