import time
from datetime import datetime
import redis
from flask import Flask
from flask import request
from flask import jsonify
import re

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)
busy = "<html><body><p> oops...当前访问人数较多，请稍后再试... </p></body></html>"
front_busy = "<html><body><p> OoOoops...当前访问人数较多，请稍后再试... </p></body></html>"
# regex
show_detail_path = re.compile('/?show_(\w+)_detail')
show_num_path = re.compile('/?show_(\w+)')
record_path = re.compile('/?(\w+)')


def record(url, ip):
    retries = 5
    while True:
        try:
            cache.sadd(url, ip)
            return cache.scard(url)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def detail(url, ip, time):
    cache.rpush(url + "_detail", ip + "_" + time)


def show_detail(url):
    return cache.lrange(url + "_detail", 0, -1)


def show_detail_html(url):
    return "<html><body><p>" + '</p><p>'.join([x.decode('utf-8') for x in show_detail(url)]) + "</p></body></html>"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    m = show_detail_path.match(path)
    if m:
        return show_detail_html(m.group(1))
    else:
        m = show_num_path.match(path)
        if m:
            return str(cache.scard(m.group(1)))
        else:
            m = record_path.match(path)
            if m:
                record(m.group(1), ip)
                detail(m.group(1), ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                return busy
            else:
                return front_busy


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
