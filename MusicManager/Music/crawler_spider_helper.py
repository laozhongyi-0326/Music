# -*- coding: utf-8 -*-'

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import re
import redis
import time
import json
import requests
import urllib.parse

def get_music_list(key_word):
    music_list = []
    key_word_quote = urllib.parse.quote(key_word)
    for i in range(2):
        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}pn={}&rn=30&reqId=b5121fe1-9ef9-11e9-a351-f3767aabfeb3".format(key_word_quote, i)
        time.sleep(1)
        headers = {
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Referer': "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
            'Cookie': "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1562311168,1562313069; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1562313076",
            'Connection': "keep-alive",
            'Cache-Control': "no-cache",
            'Postman-Token': "9af8c3e7-0486-4b7c-8e1b-430576d62b86,3534fb6b-eab5-4250-a845-a895f95a15dc",
            'Host': "www.kuwo.cn",
            'cache-control': "no-cache"
            }

        response = requests.request("GET", url, headers=headers)
        json_dict= json.loads(response.content.decode('utf-8'))
        json_list = json_dict['data']['list']
        total = json_dict['data']['total']
        for json_info in json_list:
            item = {}
            item['song_name'] = json_info['name']
            item['songer_name'] = json_info['artist'].replace("&", ",")
            item['album_name'] = json_info['album']
            item['release_date'] = json_info['releaseDate']
            item['music_rid'] = json_info['musicrid']
            if 'albumpic' in json_info.keys():
                item['album_pic'] = json_info['albumpic']
            else:
                item['album_pic'] = None
            item['rid'] = json_info['rid']
            item['song_time_minutes'] = json_info['songTimeMinutes']
            url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1562307158018&reqId=e3578e21-9eeb-11e9-b21b-813062bf1964'.format(item['rid'])
            headers = {
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                'Accept': "application/json, text/plain, */*",
                'Cookie': "gtoken=nPVxX0ovEqy3; gid=39baace0-204f-4f6a-bf8e-204b9bbbf734; JSESSIONID=rp20f9u68uqh1oe0buja0qxnz; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1562293152,1562306059,1562307086; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1562307086",
                'Connection': "keep-alive",
                'Cache-Control': "no-cache",
                'Host': "www.kuwo.cn",
                'cache-control': "no-cache"
            }
            song_response = requests.request("GET", url, headers=headers)
            song_json_dict = json.loads(song_response.content.decode('utf-8'))
            song_msg = song_json_dict['msg']
            if song_msg == 'success':
                item['play_url'] = song_json_dict['url']
            else:
                item['play_url'] = None
            # music_list.append(json.dumps(item, ensure_ascii=False))
            music_list.append(item)
    return music_list


if __name__ == '__main__':
    key_word = '周杰伦'
    music_list = get_music_list(key_word)
    print(music_list)
