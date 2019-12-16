#-*- codeing: UTF-8 -*-
from marvel import Marvel
from enum import Enum
import pymongo
import csv
import time
import configparser 

MONGODB_URL = 'mongodb://localhost:27017/'
MONGODB_DB_NAME = 'marvel'  # 数据库名

config_file_name = "userInfo.conf"
node_filepath = 'node.csv'
edge_filepath = 'edge.csv'


class CollectionName(Enum):
    CHARACTERS = 'characters'
    STORIES = 'story'


def connect_mongodb(col_name, db_name=MONGODB_DB_NAME, db_url=MONGODB_URL):
    """连接到mongodb数据库"""
    myclient = pymongo.MongoClient(db_url)
    mydb = myclient[db_name]
    mycol = mydb[col_name]
    return mycol


def userInfoConfig(configname):
    '''读取config中的公钥和私钥'''
    cp = configparser.ConfigParser()
    cp.read(configname)
    private_key = cp.get('key','private_key')
    public_key = cp.get('key','public_key')
    return public_key, private_key


def download_all_characters(marvel, mycol):
    ''' 将角色的数据都保存到mongodb数据库中： 英雄共计1493人 '''
    for i in range(0, 1500, 100):
        batch_characters = marvel.characters.all(limit=100, offset=i)
        for character in batch_characters["data"]["results"]:
            mycol.insert_one(character)
    print("success download all characters")


def create_node(filepath, mycol):
    ''' 通过下载的角色信息确定节点信息 '''
    characters = []
    headers = ['id', 'name', 'weight']  # 角色编号id，角色名name，角色故事数量weight: [1009610, 'Spider-Man', 5478]]
    with open(filepath, 'w', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

    for character in mycol.find():
        characters.append([character["id"], character["name"], character["stories"]["available"]])
    characters.sort(key=lambda x:x[2], reverse=True)
    # 仅仅下载了故事最多的前99个英雄
    ml = characters[0:99]
    for m in ml:
        with open(filepath, 'a+', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(m)
    print("创建节点成功，数据写入 " + filepath + " 文件")


def download_some_stories(marvel, mycol):
    ''' 将前一步生成的node里面的英雄的故事进行保存，所有故事有106788个，全部保存没有必要'''
    some_heros = []
    with open(node_filepath, 'r', encoding='utf-8') as f:
        for r in f:
            some_heros.append(r.split(',')[0:3])
    some_heros = some_heros[1:]
    # print(some_heros)
    for hero in some_heros:
        for i in range(0, int(hero[2]), 30):
            batch_stories = marvel.stories.all(characters=hero[0], offset=i, limit=30)
            print(batch_stories)
            time.sleep(3)
            for story in batch_stories["data"]["results"]:
                mycol.insert_one({"hreoid":str(hero[0]),"story":story})
                # print(story)
        print("story about hero "+hero[1]+" has downloaded")

    print("success download all stories about some hero")


def create_edges(edges_filepath,story_col):
    '''
    基于生成的英雄对应故事的信息创建英雄对应于英雄之间的关联指数[heroid1,heroid2,weight],并将数据存放在edges_filepath文件中。
    :param edges_filepath: 文件存放位置
    :param story_col: mongdb中story表的引用
    :return: none
    '''
    hero_story = {}
    for q in story_col.find():
        # print(q["heroid"])
        if q["heroid"] not in hero_story.keys():
            hero_story[q["heroid"]] = []
            # print("not exit")
        else:
            hero_story[q["heroid"]].append(q["story"]["id"])

    # 创建表头
    edge_headers = ['source', 'target', 'weight']
    with open(edges_filepath, 'w', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(edge_headers)

    '''两层循环用来对于遍历任意两个英雄之间关联的权重：
       具体方式：每个英雄都有自己经历的故事，两个英雄彼此故事的重合的数量就表示两者的交集的多少，
                每个英雄的故事存在在list中，两个list合并之后创建set，两个list长度的和与set长度的差值就是重合的数目
                为了保证数据不会重复，所以仅仅计算key1>key2的时候的情况。
                为了保证数据有效，仅仅记录重合数目>0的时候的情况。
    '''
    for key, value in hero_story.items():
        for innerkey, innervalue in hero_story.items():
            # print(type(int(key)))
            if int(key) > int(innerkey):
                key_len = len(value)
                innerkey_len = len(innervalue)
                # print(value)
                # print(type(value),type(innervalue)) #list list
                # print(value+innervalue) # 两个list实现合并
                set_len = len(set(value + innervalue))
                common_len = key_len + innerkey_len - set_len
                print(str(key) + " and " + str(innerkey) + " " + str(common_len))
                with open(edge_filepath, 'a+', encoding='utf-8') as f:
                    f_csv = csv.writer(f)
                    if common_len > 0:
                        f_csv.writerow([key, innerkey, common_len])
    print("edges生成完毕")


def main():

    public_key,private_key = userInfoConfig(config_file_name)
    # print(public_key+' '+private_key)

    # 创建marvel连接
    m = Marvel(public_key, private_key)

    # 数据库连接
    character_col = connect_mongodb(col_name=CollectionName.CHARACTERS.value)
    # 下载所有角色信息,信息格式参见：https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0
    download_all_characters(m, character_col)

    # 生成节点数据
    create_node(node_filepath, character_col)

    # 下载对应英雄的故事，
    story_col = connect_mongodb(col_name=CollectionName.STORIES.value)
    # download_some_stories(m, story_col)

    # 生成边数据
    create_edges(edge_filepath,story_col)


if __name__ == '__main__':
    main()












