#导入相关模块
import requests
import time
import random
#复制请求头，cookies等参数
headers={
    'user-agent':'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/9.9.3)hhz6.4.2-didf8ac704efdb0727cd4cf6b60dbf01b0c-h1bdf4d04986920fef3e8813-uid15177092-vid_a1e4012ec41322082963b3abc723afb2-proxy-k3vo9-emu0',
    'accept-encoding':'gzip',
    'content-type': 'application/x-www-form-urlencoded',
}

cookies={
    'visitor_token':'vid_a1e4012ec41322082963b3abc723afb2',
    'hhz_token':'86585d75f4ca65bdb5f8a7e551b9b9d5',
    'Token':'86585d75f4ca65bdb5f8a7e551b9b9d5'
}
url='https://yapi.haohaozhu.cn/Topic/listing'

# 换成谁都没用……默认就是那个“本周热门”的内容。。。
params = 'topic_id=519&sort_type=1&current_time=1589453251&p=2&page=2&basic_info=%7B%22%24app_version%22%3A%226.4.2%22%2C%22%24lib%22%3A%22Android%22%2C%22%24lib_version%22%3A%221.6.19%22%2C%22%24manufacturer%22%3A%22Xiaomi%22%2C%22%24os%22%3A%22Android%22%2C%22%24os_version%22%3A%229%22%2C%22%24screen_height%22%3A1920%2C%22%24screen_width%22%3A1080%2C%22distinct_id%22%3A%22f8ac704efdb0727cd4cf6b60dbf01b0c%22%2C%22isProxy%22%3A1%7D'

if __name__ == "__main__":
    # 注意请求方式是POST
    res = requests.post(url, headers=headers, cookies=cookies, params=params)
    json_obj = res.json()
    data = json_obj['data']
    list = data['list']
    for content in list:
        # 把评论文本提取出来
        comment_box = content['photo']['photo_info']
        comment = comment_box['remark']
        remark_list.append(comment)
        # 加入停顿防止被反爬
        time.sleep(random.random())

# remark_list=[]
# for i  in range(1,28):
#     #这个参数虽然又规律但是今天我看的时候已经发生变化了，大家如果要爬的话需要重新观察下。
#     params='topic_id=365&sort_type=1&current_time=1589453251&page={}&basic_info=%7B%22%24app_version%22%3A%224.7.0%22%2C%22%24carrier%22%3A%22%E5%85%B6%E4%BB%96%22%2C%22%24lib%22%3A%22Android%22%2C%22%24lib_version%22%3A%221.6.19%22%2C%22%24manufacturer%22%3A%22Xiaomi%22%2C%22%24os%22%3A%22Android%22%2C%22%24os_version%22%3A%228.0.0%22%2C%22%24screen_height%22%3A1920%2C%22%24screen_width%22%3A1080%2C%22distinct_id%22%3A%2244c043bb9672a88b4eafdfb3ce276c2c%22%7D'.format(i)
#
#     #注意请求方式是POST
#     res=requests.post(url,headers=headers,cookies=cookies,params=params)
#     json_obj=res.json()
#     data=json_obj['data']
#     list=data['list']
#     for content in list:
#         #把评论文本提取出来
#         comment_box=content['photo']['photo_info']
#         comment=comment_box['remark']
#         remark_list.append(comment)
#         #加入停顿防止被反爬
#         time.sleep(random.random())