#-*- codeing: UTF-8 -*-
from marvel import Marvel
from enum import Enum
import json
import pymongo
import csv
import time
import configparser 

MONGODB_URL = 'mongodb://localhost:27017/'
MONGODB_DB_NAME = 'marvel'  # 数据库名


filepath = 'name.csv'


class CollectionName(Enum):
    CHARACTERS = 'characters'
    STORIES = 'stories'


def dic2json( dict ):
    return json.dumps(dict)


def connect_mongodb(col_name, db_name=MONGODB_DB_NAME, db_url=MONGODB_URL):
    """连接到mongodb数据库"""
    myclient = pymongo.MongoClient(db_url)
    mydb = myclient[db_name]
    mycol = mydb[col_name]
    return mycol


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
    ml = characters[0:99]
    for m in ml:
        with open(filepath, 'a+', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(m)
    print("创建节点成功，数据写入 " + filepath + " 文件")


def main():
    # 数据库连接
    character_col = connect_mongodb(db_name=CollectionName.CHARACTERS.value)

    # 创建marvel连接
    m = Marvel(public_key, private_key)

    # 下载所有角色信息,信息格式参见：https://developer.marvel.com/docs#!/public/getCreatorCollection_get_0
    # download_all_characters(m, character_col)

    # 生成节点数据
    # create_node(filepath, character_col)


def download_some_stories(marvel, mycol):
    ''' 将前一步生成的node里面的英雄的故事进行保存，所有故事有106788个，全部保存没有必要'''
    some_heros = []
    with open(filepath, 'r', encoding='utf-8') as f:
        # f_csv = csv.reader(f)
        for r in f:
            # print(r)
            some_heros.append(r.split(',')[0:3])
    some_heros = some_heros[1:]
    print(some_heros)
    print("hello")
    for hero in some_heros:
        for i in range(0, int(hero[2]), 30):
            batch_stories = marvel.stories.all(characters=hero[0], offset=i, limit=30)
            print(batch_stories)
            time.sleep(3)
            for story in batch_stories["data"]["results"]:
                mycol.insert_one({str(hero[0]):story})
                print(story)
        print("story about hero "+hero[1]+" has downloaded")

    print("success download all stories about some hero")

def userInfoConfig(configname):
    cp = configparser.ConfigParser()
    cp.read(configname)
    private_key = cp.get('key','private_key')
    public_key = cp.get('key','public_key')
    return public_key,private_key

if __name__ == '__main__':
    # main()
    public_key,private_key = userInfoConfig("userInfo.conf")
    # print(public_key+' '+private_key)

    # 数据库连接
    # character_col = connect_mongodb(col_name=CollectionName.CHARACTERS.value)

    # # 创建marvel连接
    # m = Marvel(public_key, private_key)

    # characters = m.characters

    # print(characters.get(1011334))


    # # 下载所有故事信息，信息格式参见
    # story_col = connect_mongodb(col_name=CollectionName.STORIES.value)
    # download_some_stories(m, story_col)






