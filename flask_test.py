import requests
import fakeredis

redis = fakeredis.FakeStrictRedis()


post_url = "http://localhost:8080/visited_links"
get_url = "http://localhost:8080/visited_domains"

def make_posttest(data, msg, status_code):

    def fn():
        for d in data:
            response = requests.post(url=post_url, json=d)
            assert (response.json(), response.status_code) == ({"status": msg}, status_code)
    return fn

def make_gettest(url, data, end, msg, status_code):
    def fn():
        response = requests.get(url=f"{url}?from={data[start]}&to={data[end]}")
        assert (response.json(), response.status_code) == ({"status": msg}, status_code)
    return fn

test_post_ok = make_posttest( 
    [{"links":[
            "ya.ru", 
            "https://ya.ru", 
            "https://ya.ru?q=123", 
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]}],
    "ok",
    200)
test_post_no_data = make_posttest([None], "there is no data", 400)
test_post_not_json_format = make_posttest([1, [], "", (1,)] , "Data is not a dict", 400)
test_post_not_no_links = make_posttest([{}] , "Trere is no field 'links' in data", 400)
test_post_links_not_list = make_posttest( 
    [{"links": 1}, {"links": ""}, {"links": {}}, {"links": None}],
    "'links' is not a list", 
    400)
test_post_links_empty = make_posttest([{"links": []}] , "'links' list is empty", 400)
test_post_links_non_string = make_posttest( 
    [{"links": [1]}, {"links": [[]]}, {"links": [(1,)]}], 
    "'links' contain non-string values", 
    400)
test_post_invalid_domain = make_posttest( 
    [
        {"links": ["..."]},
        {"links": ["1"]},
        {"links": ["ya.r"]},
        {"links": ["abc://ya.ru"]},
        {"links": ["https://yaru"]}
    ],
    "'links' contain an invalid link", 
    400)


  