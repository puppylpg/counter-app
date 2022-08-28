import time
from datetime import datetime
import redis
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)


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


@app.route("/a", methods=["GET"])
def a():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    detail("a", ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    count = record("a", ip)
    return "{} {}".format(ip, count)


@app.route("/b", methods=["GET"])
def b():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    detail("b", ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    count = record("b", ip)
    return "{} {}".format(ip, count)


@app.route("/show_a", methods=["GET"])
def show_a():
    return str(cache.scard("a"))


@app.route("/show_b", methods=["GET"])
def show_b():
    return str(cache.scard("b"))


@app.route("/show_a_detail", methods=["GET"])
def show_a_detail():
    return '\n'.join([x.decode('utf-8') for x in show_detail("a")])


@app.route("/show_b_detail", methods=["GET"])
def show_b_detail():
    return '\n'.join([x.decode('utf-8') for x in show_detail("b")])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
