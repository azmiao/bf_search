import os
import shutil
from hoshino import Service, R
from .search import *

sv_help = '''=====Gametool数据源=====
(Gametool国内经常打不开)
[战地1查询 角色昵称] 查询战地1信息

[战地4查询 角色昵称] 查询战地4信息

[战地5查询 角色昵称] 查询战地5信息

=====K-ON数据=====
(稳定，但只有战地1/5的数据)
[bf1查询 角色昵称] 查询战地1信息

[bfv查询 角色昵称] 查询战地5信息

[bf1查id 角色昵称] 查询战地1的个人ID

[bf1查ban 角色昵称] 查询战地1的ban状态

[bf1正在游玩 角色昵称] 查询战地1的正在游玩的服务器

[bf1最近游玩 角色昵称] 查询战地1的最近游玩过的服务器

[bf1查服务器 服务器名] 根据服务器名查询该服务器ID'''.strip()

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

@sv.on_prefix('bf1查询')
async def search_info(bot, ev):
    displayName = ev.message.extract_plain_text()
    msg = get_pinfo(displayName)
    await bot.send(ev, msg)

@sv.on_prefix('bf1查id')
async def search_pid(bot, ev):
    displayName = ev.message.extract_plain_text()
    msg = f'{displayName}的ID为：' + str(get_pid(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1查ban')
async def check_pid(bot, ev):
    displayName = ev.message.extract_plain_text()
    msg = f'{displayName}的联ban状态为：' + str(check_ban(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1正在游玩')
async def get_playing(bot, ev):
    displayName = ev.message.extract_plain_text()
    msg = str(get_playing_server(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1最近游玩')
async def get_his_playing(bot, ev):
    displayName = ev.message.extract_plain_text()
    msg = str(get_history(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1查服务器')
async def search_server(bot, ev):
    name = ev.message.extract_plain_text()
    msg = str(get_serverid(name))
    await bot.send(ev, msg)

@sv.on_prefix('bfv查询')
async def search_info(bot, ev):
    displayName = ev.message.extract_plain_text()
    msg = get_bfvpinfo(displayName)
    await bot.send(ev, msg)