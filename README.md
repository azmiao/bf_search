## 注意

gametools的数据源，由于cloudflare的cdn加速要看地区，有些地方可能打不开。

k-0n的数据源，是国内的，速度较快，由K-ON服服主 SuzuBucket 提供key

## 更新日志

21-09-13    v2.0    新增k-0n数据源查询（需要申请key）

21-09-02    v1.2    增加查无此人的回复

21-09-01    v1.1    修复战地4查询的问题

21-08-10    v1.0    首次测试

## bf_search

一个适用hoshinobot的 战地1 / 战地4 / 战地5 战绩信息查询插件

## 项目地址：
https://github.com/azmiao/bf_search/

## 功能

```
正式功能：

=====Gametool数据源=====
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

[bf1查服务器 服务器名] 根据服务器名查询该服务器ID
```

## 简单食用教程：

可看下方链接（~~不写了~~）：

~~https://www.594594.xyz/2021/08/11/bf_search/~~

或本页面：

1. 需要k-0n数据源的请去申请key，发邮件到邮箱root@k-0n.org，让桶唯（~~大桶蹄子~~）给你个key

    BTW：别人都封装好了api，干嘛不用（）

    若只用Gametool就不用key了，不用k-0n请忽略这条

2. 下载或git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/bf_search
    ```

3. 去`search.py`下的第`7`行填写你的key

    注：不用k-0n请忽略这条

4. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'bf_search'

    然后重启 HoshinoBot 即可