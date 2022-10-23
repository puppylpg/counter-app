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
# 话题下用户的post list，包含comment
url_post_list = 'https://yapi.haohaozhu.cn/topic/GetAnswerList460'


def write(dictionary, path):
    path = 'haohaozhu/' + path
    print(path)
    # Writing to sample.json
    with open(path, "w", encoding='utf-8') as outfile:
        json.dump(dictionary, outfile, indent=2, ensure_ascii=False)


def get(url, headers, cookies, params, times = 1):
    max = 5
    if times > max:
        print('Timeout for {} beyond the maximum({}) retry times. SKIP!'.format(url, max))
        return None

    # 加入停顿防止被反爬
    retry_wait = random.randint(0, 3)
    print("sleep: {}s".format(retry_wait))
    time.sleep(retry_wait)
    try:
        return requests.post(url, headers=headers, cookies=cookies, params=params)
    except Exception as e:
        print("Unknown error for {}. Try again(Times={}). Error string: {}".format(url, times, e))

    hhz_data = get(url, headers, cookies, params, times + 1)
    return hhz_data


remark_list = []
if __name__ == "__main__":
    topic_ids_hot = [499, 193, 660, 698, 519, 263, 414, 261, 663, 354, 670, 586, 516, 528, 661, 507, 366, 683, 743, 345]
    # 手写
    topic_ids = [1594, 1362, 1433, 1573, 1417, 1302, 1411, 1572, 1312, 1280, 1447, 1410, 1196, 1523, 1318, 1481, 1347, 1129, 1374, 1442, 1180, 1331, 1160, 1300, 1033, 1250, 1122, 1314, 1560, 397, 1511, 1301, 1372, 1329, 1320, 1424, 1546, 537, 86, 1217, 1622, 1545, 364, 1518, 645, 1605, 483, 1003, 626, 585, 1306, 1186, 1606, 459, 508, 1117, 566, 607, 495, 369, 1094, 589, 598, 451, 1152, 1028, 1323, 363, 1542, 1526, 471, 250, 505, 1458, 1270, 641, 101, 1155, 1513, 748, 1382, 1219, 1340, 440, 1429, 1113, 1474, 1004, 527, 517, 922, 510, 450, 604, 404, 568, 166, 170, 520, 481, 552, 997, 549, 685, 194, 558, 412, 427, 452, 278, 400, 535, 361, 382, 485, 306, 573, 561, 682, 359, 402, 386, 455, 394, 395, 475, 390, 902, 719, 447, 458, 429, 387, 628, 366, 650, 840, 596, 518, 720, 491, 663, 506, 507, 743, 261, 480, 580, 516, 586, 565, 354, 512, 528, 519, 499, 193, 660, 698, 263, 414, 670, 661, 683, 345]
    # topic_ids = [1433, 1362, 1594]

    cur_topic_num = 0

    # last time，用于中断恢复
    continue_from_break = True
    topic_from = 682
    page_from = 107

    for topic_id in topic_ids:
        cur_topic_num = cur_topic_num + 1
        # 起始页
        page = 1
        print("=====>")
        print("topic={}, {}/{}".format(topic_id, cur_topic_num, len(topic_ids)))
        topic_continue = True

        # 用于中断恢复
        if continue_from_break is True and topic_from is not None:
            if topic_id != topic_from:
                continue

        while topic_continue:
            # continue
            if continue_from_break:
                page = page_from
                continue_from_break = False

            params = 'topic_id=' + str(topic_id) + '&sort_type=1&current_time=1589453251&page={}&basic_info=%7B%22%24app_version%22%3A%226.4.2%22%2C%22%24lib%22%3A%22Android%22%2C%22%24lib_version%22%3A%221.6.19%22%2C%22%24manufacturer%22%3A%22Xiaomi%22%2C%22%24os%22%3A%22Android%22%2C%22%24os_version%22%3A%229%22%2C%22%24screen_height%22%3A1920%2C%22%24screen_width%22%3A1080%2C%22distinct_id%22%3A%22f8ac704efdb0727cd4cf6b60dbf01b0c%22%2C%22isProxy%22%3A1%7D'.format(page)
            post_res = get(url_post_list, headers=headers, cookies=cookies, params=params)
            post_json = post_res.json()
            data = post_json['data']
            # 干脆用pandas写到excel里得了，然后再存个原始json, and catch exception、add retry
            # title = data['list']['photo']['photo_info']['topic']['title']

            topic_continue = False if data['is_over'] == 1 else True
            if topic_continue is False:
                print("over for topic={}, page={}".format(topic_id, page))

            write(data,  str(topic_id) + "_" + str(page) + ".json")
            page = page + 1

