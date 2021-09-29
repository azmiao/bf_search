import requests
import os,base64
import yaml
from io import BytesIO
from hoshino import R

def get_key():
    key = ''
    return key

def get_displayName(user_id):
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    displayName = None
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    for user in config['bf_info']:
        if user['user_id'] == user_id:
            displayName = user['displayName']
    if displayName == None:
        displayName = f'你当前QQ暂未绑定战地'
    return displayName

def get_info(name, bf):
    url = f'https://api.gametools.network/{bf}/stats/'
    params = {
        'name': name,
        'lang': 'en-us'
    }
    try:
        per_info = requests.get(url, params, timeout=(5,10)).json()
    except:
        msg = 'gametool网站连接失败！'
        return msg
    return per_info

def create_img(img_url, name, bf):
    response = requests.get(img_url)
    ls_f = base64.b64encode(BytesIO(response.content).read())
    imgdata = base64.b64decode(ls_f)
    save_dir = R.img('bf_search').path
    path_dir = os.path.join(save_dir,f'{bf}_{name}.jpg')
    file = open(path_dir,'wb')
    file.write(imgdata)
    file.close()

def create_msg(name, bf):
    per_info = get_info(name, bf)
    if per_info == 'gametool网站连接失败！':
        return per_info
    nodata = {"detail": "playername not found"}
    if per_info == nodata:
        return '未找到此人'
    avatar = per_info['avatar']
    userName = per_info['userName']
    rank = per_info['rank']
    killDeath = per_info['killDeath']
    killsPerMinute = per_info['killsPerMinute']
    scorePerMinute = per_info['scorePerMinute']
    infantryKillDeath = per_info['infantryKillDeath']
    infantryKillsPerMinute = per_info['infantryKillsPerMinute']
    winPercent = per_info['winPercent']
    accuracy = per_info['accuracy']
    headshots = per_info['headshots']
    kills = per_info['kills']
    roundsPlayed = per_info['roundsPlayed']
    Killsperround = round(kills/roundsPlayed, 2)
    timePlayed = per_info['timePlayed']

    create_img(avatar, name, bf)
    avatar_img = ' '.join(map(str, [
        R.img(f'bf_search/{bf}_{name}.jpg').cqcode,
    ]))
    msg = f'{avatar_img}\n昵称：' + userName + f'\n等级：' + str(rank) + f'\nKD：' + str(killDeath) + f'\nKPM：' + str(killsPerMinute) + f'\nSPM：' 
    msg = msg + str(scorePerMinute) + f'\n步战KD：'  + str(infantryKillDeath) + f'\n步战KPM：' + str(infantryKillsPerMinute) + f'\n总胜率：' 
    msg = msg + winPercent + f'\n精准度：'  + accuracy + f'\n爆头率：'  + headshots + f'\n总击杀：'  + str(kills) + f'\n游戏局数：' 
    msg = msg + str(roundsPlayed) + f'\n场均击杀：'  + str(Killsperround) + f'\n游戏时间：'  + timePlayed
    return msg

# 战地4专用
def get_bf4info(name, bf):
    url = f'https://api.gametools.network/{bf}/stats/'
    params = {
        'name': name,
        'platform': 'pc'
    }
    try:
        per_info = requests.get(url, params, timeout=(5,10)).json()
    except:
        msg = 'gametool网站连接失败！'
        return msg
    return per_info

# 战地4专用
def create_bf4msg(name, bf):
    per_info = get_bf4info(name, bf)
    if per_info == 'gametool网站连接失败！':
        return per_info
    nodata = {"detail": "playername not found"}
    if per_info == nodata:
        return '未找到此人'
    avatar = per_info['avatar']
    userName = per_info['userName']
    rank = per_info['rank']
    killDeath = per_info['killDeath']
    killsPerMinute = per_info['killsPerMinute']
    scorePerMinute = per_info['scorePerMinute']
    winPercent = per_info['winPercent']
    accuracy = per_info['accuracy']
    headshots = per_info['headshots']
    kills = int(per_info['kills'])
    roundsPlayed = int(per_info['wins']) + int(per_info['loses'])
    Killsperround = round(kills/roundsPlayed, 2)
    timePlayed = per_info['timePlayed']

    create_img(avatar, name, bf)
    avatar_img = ' '.join(map(str, [
        R.img(f'bf_search/{bf}_{name}.jpg').cqcode,
    ]))
    msg = f'{avatar_img}\n昵称：' + userName + f'\n等级：' + str(rank) + f'\nKD：' + str(killDeath) + f'\nKPM：' + str(killsPerMinute) + f'\nSPM：' 
    msg = msg + str(scorePerMinute) + f'\n总胜率：' + winPercent + f'\n精准度：'  + accuracy + f'\n爆头率：'  + headshots + f'\n总击杀：'
    msg = msg  + str(kills) + f'\n游戏局数：' + str(roundsPlayed) + f'\n场均击杀：'  + str(Killsperround) + f'\n游戏时间：'  + timePlayed
    return msg
    
def get_pinfo(displayName):
    url = f'https://api.k-0n.org/bf1/getCareer'
    headers = {
        'apikey': get_key()
    }
    params = {
        'displayName': displayName
    }
    per_info = requests.post(url, headers = headers, params = params).json()
    userName = displayName
    rank = per_info['Data']['rank']
    kd = per_info['Data']['kd']
    kpm = per_info['Data']['kpm']
    spm = per_info['Data']['spm']
    winPercent = round(per_info['Data']['wins']/(per_info['Data']['wins'] + per_info['Data']['losses']), 2)
    kills = per_info['Data']['kills']
    roundsPlayed = per_info['Data']['wins'] + per_info['Data']['losses']
    Killsperround = round(kills/roundsPlayed, 2)
    timePlayed = str(per_info['Data']['timePlayer_Readable']['day']) + '天' + str(per_info['Data']['timePlayer_Readable']['hours']) + '小时' + str(per_info['Data']['timePlayer_Readable']['minus']) + '分钟'
    msg = f'昵称：' + userName + f'\n等级：' + str(rank) + f'\nKD：' + str(kd) + f'\nKPM：' + str(kpm) + f'\nSPM：' 
    msg = msg + str(spm) + f'\n总胜率：' + str(winPercent) + f'\n总击杀：'  + str(kills) + f'\n游戏局数：' 
    msg = msg + str(roundsPlayed) + f'\n场均击杀：'  + str(Killsperround) + f'\n游戏时间：'  + timePlayed
    return msg

# 获取id
def get_pid(displayName):
    url = f'https://api.k-0n.org/origin/getPid/{displayName}'
    headers = {
        'apikey': get_key()
    }
    params = {
        'nocache': False,
        'details': False
    }
    pid_info = requests.get(url, headers = headers, params = params).json()
    return pid_info['Data']['UserId']

# 查询联ban
def check_ban(displayName):
    userId = get_pid(displayName)
    url = f'https://api.k-0n.org/bfban/check'
    headers = {
        'apikey': get_key()
    }
    params = {
        'userId': userId
    }
    ban_info = requests.post(url, headers = headers, params = params).json()
    if ban_info['Data'] == False:
        msg = '暂未被ban'
    else:
        msg = '已被ban'
    return msg

# 查询正在游玩的服务器
def get_playing_server(displayName):
    url = f'https://api.k-0n.org/bf1/getPlayingServer'
    headers = {
        'apikey': get_key()
    }
    params = {
        'displayName': displayName
    }
    play_info = requests.post(url, headers = headers, params = params).json()
    if play_info['Data'] == None:
        msg = f'{displayName}现在没在打战地1呢'
    else:
        msg = f'{displayName}正在游玩：\n服务器名' + play_info['Data']['gameName'] + '\n服务器ID：' + play_info['Data']['gameId']
        msg = msg + '\n游戏模式：' + play_info['Data']['modeName'] + '\n游戏地图：' + play_info['Data']['mapName']
    return msg

# 查询最近游玩的服务器
def get_history(displayName):
    url = f'https://api.k-0n.org/bf1/serverHistory'
    headers = {
        'apikey': get_key()
    }
    params = {
        'displayName': displayName
    }
    his_info = requests.post(url, headers = headers, params = params).json()
    if his_info['Data'] != None:
        msg = f'{displayName}最近游玩的服务器为：'
        for his_list in his_info['Data']:
            msg = msg + '\n\n服务器：' + his_list['name'] + '\n服务器ID：' + his_list['gameId']
    else:
        msg = f'{displayName}最近没有游玩呢'
    return msg

# 查服务器id
def get_serverid(name):
    url = f'https://api.k-0n.org/bf1/searchServer'
    headers = {
        'apikey': get_key()
    }
    params = {
        'name': name
    }
    his_info = requests.post(url, headers = headers, params = params).json()
    msg = f'查询到{name}相关的服务器为：'
    for ser_list in his_info['Data']:
        msg = msg + '\n\n服务器：' + ser_list['name'] + '\n服务器ID：' + ser_list['gameId'] 
    return msg

# 战地5
def get_bfvpinfo(displayName):
    url = f'https://api.k-0n.org/bfv/getCareer'
    headers = {
        'apikey': get_key()
    }
    params = {
        'displayName': displayName
    }
    per_info = requests.post(url, headers = headers, params = params).json()
    userName = displayName
    rank = per_info['Data']['rank']
    kd = per_info['Data']['kd']
    kpm = per_info['Data']['kpm']
    spm = per_info['Data']['spm']
    winPercent = round(per_info['Data']['wins']/(per_info['Data']['wins'] + per_info['Data']['losses']), 2)
    kills = per_info['Data']['kills']
    roundsPlayed = per_info['Data']['wins'] + per_info['Data']['losses']
    Killsperround = round(kills/roundsPlayed, 2)
    timePlayed = str(per_info['Data']['timePlayer_Readable']['day']) + '天' + str(per_info['Data']['timePlayer_Readable']['hours']) + '小时' + str(per_info['Data']['timePlayer_Readable']['minus']) + '分钟'
    msg = f'昵称：' + userName + f'\n等级：' + str(rank) + f'\nKD：' + str(kd) + f'\nKPM：' + str(kpm) + f'\nSPM：' 
    msg = msg + str(spm) + f'\n总胜率：' + str(winPercent) + f'\n总击杀：'  + str(kills) + f'\n游戏局数：' 
    msg = msg + str(roundsPlayed) + f'\n场均击杀：'  + str(Killsperround) + f'\n游戏时间：'  + timePlayed
    return msg