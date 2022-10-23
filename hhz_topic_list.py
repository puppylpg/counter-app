import requests
import time
import random
import json

# 复制请求头，cookies等参数
headers = {
    'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/9.9.3)hhz6.4.2-didf8ac704efdb0727cd4cf6b60dbf01b0c-h1bdf4d04986920fef3e8813-uid15177092-vid_a1e4012ec41322082963b3abc723afb2-proxy-k3vo9-emu0',
    'accept-encoding': 'gzip',
    'content-type': 'application/x-www-form-urlencoded',
}

cookies = {
    'visitor_token': 'vid_a1e4012ec41322082963b3abc723afb2',
    'hhz_token': '86585d75f4ca65bdb5f8a7e551b9b9d5',
    'Token': '86585d75f4ca65bdb5f8a7e551b9b9d5'
}
# tab，每个是一个话题
url_tab_topic = 'https://yapi.haohaozhu.cn/Topic/listing'
# 话题下用户的post list，包含comment
url_post_list = 'https://yapi.haohaozhu.cn/topic/GetAnswerList460'

remark_list = []
if __name__ == "__main__":
    tab_topic_continue = True
    while tab_topic_continue:
        shawshank='qEpcsu2CCkruqxB6h.itrY2p2txEp-tBp5hq7hIMHJ6cEwizpzX5C5gsOZLBZCEC9Z0P-28jNolH6JmzUFGdo_FmxJ0YNgGc6bR3tZRWDkjFEsUuAUgNys%3D'
        params1 = 'shawshank=' + shawshank + '&basic_info=basic_info=%7B%22%24app_version%22%3A%226.4.2%22%2C%22%24lib%22%3A%22Android%22%2C%22%24lib_version%22%3A%221.6.19%22%2C%22%24manufacturer%22%3A%22Xiaomi%22%2C%22%24os%22%3A%22Android%22%2C%22%24os_version%22%3A%229%22%2C%22%24screen_height%22%3A1920%2C%22%24screen_width%22%3A1080%2C%22distinct_id%22%3A%22f8ac704efdb0727cd4cf6b60dbf01b0c%22%2C%22isProxy%22%3A1%7D'

        topics_res = requests.post(url_tab_topic, headers=headers, cookies=cookies, params=params1)
        topics_json = topics_res.json()
        topics_data = topics_json['data']
        topics = topics_data['list']

        # 没办法，topic list不是按照page翻页的，我也不知道是啥参数……
        tab_topic_continue = False
        write(topics_data, topic_id + ".json")

        for topic in topics:
            topic_continue = True
            topic_id = topic['topic_info']['id']
            # 起始页
            page = 1

            while topic_continue:
                params2 = 'topic_id=' + topic_id + '&sort_type=1&current_time=1589453251&page={}&basic_info=%7B%22%24app_version%22%3A%226.4.2%22%2C%22%24lib%22%3A%22Android%22%2C%22%24lib_version%22%3A%221.6.19%22%2C%22%24manufacturer%22%3A%22Xiaomi%22%2C%22%24os%22%3A%22Android%22%2C%22%24os_version%22%3A%229%22%2C%22%24screen_height%22%3A1920%2C%22%24screen_width%22%3A1080%2C%22distinct_id%22%3A%22f8ac704efdb0727cd4cf6b60dbf01b0c%22%2C%22isProxy%22%3A1%7D'.format(page)

                post_res = requests.post(url_post_list, headers=headers, cookies=cookies, params=params2)
                post_json = res.json()
                data = post_json['data']

                topic_continue = False if data['is_over'] == 1 else True
                page = page + 1

                write(data, topic_id + "_" + page + ".json")

                # 加入停顿防止被反爬
                time.sleep(random.random())


def write(dictionary, path):
    # Serializing json
    json_object = json.dumps(dictionary, indent=2)

    # Writing to sample.json
    with open('haohaozhu/' + path, "w") as outfile:
        outfile.write(json_object)
