from datetime import datetime, timezone
import tldextract
import validators

from flask import Flask, jsonify, request, Response
import redis

app = Flask('API')
redis = redis.Redis()
is_db_connected = redis.ping()


def check_valid_domain(link):
    parsed = tldextract.extract(link)
    domain = ".".join([parsed.domain, parsed.suffix])
    if "://" in link:
        assert validators.url(link), "'links' contain an invalid link"
    else:
        assert validators.domain(domain), "'links' contain an invalid link"
    return domain


@app.route("/visited_links", methods=["POST"])
def add_domains():
    try:
        assert request.data, "there is no data"
        json = request.get_json()
        assert isinstance(json, dict), "Data is not a dict"
        assert "links" in json, "Trere is no field 'links' in data"
        assert isinstance(json["links"], list), "'links' is not a list"
        assert json["links"] != [], "'links' list is empty"
        assert all(list(map(lambda x: isinstance(x, str), json["links"]))), "'links' contain non-string values"
        domains = [check_valid_domain(link) for link in json["links"]]
    except Exception as e:
        return {"status": str(e)}, 400

    try:
        assert is_db_connected, "no connection to redis db"
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())
        domains = dict(zip(domains, [timestamp]*len(domains)))
        redis.zadd("visited_links", domains)
    except Exception as e:
        return {"status": str(e)}, 500
    return {"status": "ok"}
    

@app.route("/visited_domains", methods=["GET"])
def get_domains():
    try:
        start = request.args.get("from", "-inf")
        end = request.args.get("to", "+inf")
        assert not (start != "-inf" and end != "+inf") ^ (start.isdigit() and end.isdigit()), "start/end is not a digit"
        assert not (start != "-inf" and end != "+inf" and int(start) > int(end)), "'from' is greater than 'to'"
    except Exception as e:
        return {"status": str(e)}, 400

    try:
        assert is_db_connected, "no connection to redis db"
        assert redis.exists("visited_links"), "there is no such key in redis db"
        assert redis.zrangebyscore("visited_links", '-inf', '+inf'), "sorted set is empty"
        res = redis.zrangebyscore("visited_links", start, end)
        res = [str(x, "utf-8").split(":")[-1] for x in res]
        res = list(set(res))
    except Exception as e:
        return {"status": str(e)}, 500
    return {"domains": res, "status": "ok"}


app.run(host="localhost", port="8080", debug=True)