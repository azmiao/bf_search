import os
import shutil
import yaml
from hoshino import Service, R
from .search import *

sv_help = '''=====绑定昵称=====
(※注：绑定昵称后下列查询均可不带昵称)

[战地绑定 角色昵称] 绑定昵称

[战地解绑] 解绑昵称

[战地当前绑定] 查询当前绑定的战地昵称

=====Gametool数据源=====
(Gametool国内经常打不开)
[战地1查询 角色昵称] 查询战地1信息

[战地4查询 角色昵称] 查询战地4信息

[战地5查询 角色昵称] 查询战地5信息

=====K-ON数据=====
(稳定，但只有战地1和5的数据)
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

_current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
if not os.path.exists(_current_dir):
    data = {'bf_info': []}
    with open(_current_dir, "w", encoding="UTF-8") as f:
        yaml.dump(data, f,allow_unicode=True)

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
    user_id = ev.user_id
    name = ev.message.extract_plain_text()
    if name == '':
        name = get_displayName(user_id)
        if name == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg_e = '正在从Gametool查询，预计5-10秒'
    await bot.send(ev, msg_e)
    msg = create_msg(name, 'bf1')
    if msg == 'gametool网站连接失败！':
        msg = msg + '\n由于API在国外所以有时可能链接不上，你可以尝试输入"战地帮助"采用用国内的K-ON的API查询'
    await bot.send(ev, msg)

@sv.on_prefix('战地4查询')
async def search_info4(bot, ev):
    user_id = ev.user_id
    name = ev.message.extract_plain_text()
    if name == '':
        name = get_displayName(user_id)
        if name == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg_e = '正在从Gametool查询，预计5-10秒'
    await bot.send(ev, msg_e)
    msg = create_bf4msg(name, 'bf4')
    if msg == 'gametool网站连接失败！':
        msg = msg + '\n由于API在国外所以有时可能链接不上，你可以尝试过会再查'
    await bot.send(ev, msg)

@sv.on_prefix('战地5查询')
async def search_info5(bot, ev):
    user_id = ev.user_id
    name = ev.message.extract_plain_text()
    if name == '':
        name = get_displayName(user_id)
        if name == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg_e = '正在从Gametool查询，预计5-10秒'
    await bot.send(ev, msg_e)
    msg = create_msg(name, 'bfv')
    if msg == 'gametool网站连接失败！':
        msg = msg + '\n由于API在国外所以有时可能链接不上，你可以尝试过会再查'
    await bot.send(ev, msg)

@sv.on_prefix('bf1查询')
async def search_info(bot, ev):
    user_id = ev.user_id
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        displayName = get_displayName(user_id)
        if displayName == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg = get_pinfo(displayName)
    await bot.send(ev, msg)

@sv.on_prefix('bf1查id')
async def search_pid(bot, ev):
    user_id = ev.user_id
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        displayName = get_displayName(user_id)
        if displayName == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg = f'{displayName}的ID为：' + str(get_pid(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1查ban')
async def check_pid(bot, ev):
    user_id = ev.user_id
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        displayName = get_displayName(user_id)
        if displayName == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg = f'{displayName}的联ban状态为：' + str(check_ban(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1正在游玩')
async def get_playing(bot, ev):
    user_id = ev.user_id
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        displayName = get_displayName(user_id)
        if displayName == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg = str(get_playing_server(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1最近游玩')
async def get_his_playing(bot, ev):
    user_id = ev.user_id
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        displayName = get_displayName(user_id)
        if displayName == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg = str(get_history(displayName))
    await bot.send(ev, msg)

@sv.on_prefix('bf1查服务器')
async def search_server(bot, ev):
    name = ev.message.extract_plain_text()
    msg = str(get_serverid(name))
    await bot.send(ev, msg)

@sv.on_prefix('bfv查询')
async def search_info(bot, ev):
    user_id = ev.user_id
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        displayName = get_displayName(user_id)
        if displayName == '你当前QQ暂未绑定战地':
            msg = '你当前QQ暂未绑定战地!'
            await bot.send(ev, msg)
            return
    msg = get_bfvpinfo(displayName)
    await bot.send(ev, msg)

@sv.on_prefix('战地绑定')
async def bound_id(bot, ev):
    user_id = ev.user_id
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    flag = 0
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    for user in config['bf_info']:
        if user['user_id'] == user_id:
            flag = 1
    if flag == 1:
        msg = '您已经绑定过啦！请勿重新绑定！'
        await bot.send(ev, msg)
        return
    displayName = ev.message.extract_plain_text()
    if displayName == '':
        msg = '错误！战地昵称不能为空！'
        await bot.send(ev, msg)
        return
    try:
        data = {
            'user_id': user_id,
            'displayName': displayName
            }
        config['bf_info'].append(data)
        with open(current_dir, "w", encoding="UTF-8") as f:
            yaml.dump(config, f,allow_unicode=True)
        msg = f'战地昵称{displayName}绑定成功'
        await bot.send(ev, msg)
    except:
        # 正常来说不会遇到
        msg = f'未知原因！绑定失败！'
        await bot.send(ev, msg)

@sv.on_fullmatch('战地解绑')
async def unbound_id(bot, ev):
    user_id = ev.user_id
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    flag = 0
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    for user in config['bf_info']:
        if user['user_id'] == user_id:
            flag = 1
    if flag == 0:
        msg = '您还未绑定战地昵称！请先绑定！'
        await bot.send(ev, msg)
        return
    try:
        for user in config['bf_info']:
            if user['user_id'] == user_id:
                displayName = user['displayName']
        data = {
            'user_id': user_id,
            'displayName': displayName
            }
        config['bf_info'].remove(data)
        with open(current_dir, "w", encoding="UTF-8") as f:
            yaml.dump(config, f,allow_unicode=True)
        msg = f'战地昵称{displayName}解绑成功'
        await bot.send(ev, msg)
    except:
        # 正常不会遇到
        msg = f'未知原因！解绑失败！'
        await bot.send(ev, msg)

@sv.on_fullmatch('战地当前绑定')
async def search_bound(bot, ev):
    user_id = ev.user_id
    try:
        current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
        file = open(current_dir, 'r', encoding="UTF-8")
        file_data = file.read()
        file.close()
        displayName = None
        config = yaml.load(file_data, Loader=yaml.FullLoader)
        for user in config['bf_info']:
            if user['user_id'] == user_id:
                displayName = user['displayName']
        if displayName == '':
            msg = f'你当前QQ暂未绑定战地'
            await bot.send(ev, msg)
        else:
            msg = f'您当前绑定了战地昵称：{displayName}'
            await bot.send(ev, msg)
    except:
        # 正常不会遇到
        msg = f'未知原因！查询当前绑定昵称失败！'
        await bot.send(ev, msg)