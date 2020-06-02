import requests
import unittest


class TestPost(unittest.TestCase):
    url = "http://localhost:8080/visited_links"

    def test_post_ok(self):
        json = {"links": [
                "ya.ru",
                "https://ya.ru",
                "https://ya.ru?q=123",
                "https://stackoverflow.com/questions/10827160/undo-a-git-stash"
                ]}
        response = requests.post(url=self.url, json=json)
        self.assertTrue(response.json(), response.status_code) == ({"status": "ok"}, 200)
        
    def test_post_no_data(self):
        response = requests.post(url=self.url, json=None)
        self.assertTrue(response.json(), response.status_code) == ({"status": "there is no data"}, 400)

    def test_post_not_json_format(self):
        data = [1, [], "", (1,)]
        for d in data:
            response = requests.post(url=self.url, json=d)
            self.assertTrue(response.json(), response.status_code) == ({"status": "Data is not a dict"}, 400)
            
    def test_post_not_no_links(self):
        response = requests.post(url=self.url, json={})
        self.assertTrue(response.json(), response.status_code) == ({"status": "Trere is no field 'links' in data"}, 400)

    def test_post_links_not_list(self):
        data = [{"links": 1}, {"links": ""}, {"links": {}}, {"links": None}]
        for d in data:
            response = requests.post(url=self.url, json=d)
            self.assertTrue(response.json(), response.status_code) == ({"status": "'links' is not a list"}, 400)
        
    def test_post_links_empty(self):
        json = {"links": []}
        response = requests.post(url=self.url, json=json)
        self.assertTrue(response.json(), response.status_code) == ({"status": "'links' list is empty"}, 400)

    def test_post_links_non_string(self):
        data = [{"links": [1]}, {"links": [[]]}, {"links": [(1,)]}]
        for d in data:
            response = requests.post(url=self.url, json=d)
            self.assertTrue(response.json(), response.status_code) == ({"status": "'links' contain non-string values"}, 400)
        
    def test_post_invalid_domain(self):
        data = [
            {"links": ["..."]},
            {"links": ["1"]},
            {"links": ["ya.r"]},
            {"links": ["abc://ya.ru"]},
            {"links": ["https://yaru"]}]
        for d in data:
            response = requests.post(url=self.url, json=d)
            self.assertTrue(response.json(), response.status_code) == ({"status": "'links' contain an invalid link"}, 400)


class TestGet(unittest.TestCase):
    url = "http://localhost:8080/visited_domains"

    def test_valid_from_to(self):
        data = [{"start": "a", "end": 1}, {"start": 1, "end": "a"}]
        for d in data:
            response = requests.get(url=self.url + f"?from={d['start']}&to={d['end']}")
            self.assertTrue(response.json(), response.status_code) == ({"status": "start/end is not a digit"}, 400)

    def test_from_greater_than_to(self):
        start = 2
        end = 1
        response = requests.get(url=self.url + f"?from={start}&to={end}")
        self.assertTrue(response.json(), response.status_code) == ({"status": "'from' is greater than 'to'"}, 400)


if __name__ == '__main__':
    unittest.main()






  
