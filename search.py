import requests
import os,base64
from io import BytesIO
from hoshino import R


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