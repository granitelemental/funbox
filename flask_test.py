import requests


class TestPost:
    url = "http://localhost:8080/visited_links"

    def test_post_ok(self):
        json = {"links": [
                "ya.ru",
                "https://ya.ru",
                "https://ya.ru?q=123",
                "https://stackoverflow.com/questions/10827160/undo-a-git-stash"
                ]}
        response = requests.post(url=self.url, json=json)
        result = response.json(), response.status_code
        assert result == ({"status": "ok"}, 200)

    def test_post_no_data(self):
        response = requests.post(url=self.url, json=None)
        result = response.json(), response.status_code
        assert result == ({"status": "there is no data"}, 400)

    def test_post_not_json_format(self):
        data = [1, [], "", (1,)]
        for d in data:
            response = requests.post(url=self.url, json=d)
            result = response.json(), response.status_code
            assert result == ({"status": "Data is not a dict"}, 400)

    def test_post_not_no_links(self):
        response = requests.post(url=self.url, json={})
        result = response.json(), response.status_code
        assert result == ({"status": "Trere is no field 'links' in data"}, 400)

    def test_post_links_not_list(self):
        data = [{"links": 1}, {"links": ""}, {"links": {}}, {"links": None}]
        for d in data:
            response = requests.post(url=self.url, json=d)
            result = response.json(), response.status_code
            assert result == ({"status": "'links' is not a list"}, 400)

    def test_post_links_empty(self):
        json = {"links": []}
        response = requests.post(url=self.url, json=json)
        result = response.json(), response.status_code
        assert result == ({"status": "'links' list is empty"}, 400)

    def test_post_links_non_string(self):
        data = [{"links": [1]}, {"links": [[]]}, {"links": [(1,)]}]
        for d in data:
            response = requests.post(url=self.url, json=d)
            result = response.json(), response.status_code
            assert result == (
                {"status": "'links' contain non-string values"}, 400)

    def test_post_invalid_domain(self):
        data = [
            {"links": ["..."]},
            {"links": ["1"]},
            {"links": ["ya.r"]},
            {"links": ["abc://ya.ru"]},
            {"links": ["https://yaru"]}]
        for d in data:
            response = requests.post(url=self.url, json=d)
            result = response.json(), response.status_code
            assert result == (
                {"status": "'links' contain an invalid link"}, 400)


class TestGet:
    url = "http://localhost:8080/visited_domains"

    def test_valid_from_to(self):
        data = [{"start": "a", "end": 1}, {"start": 1, "end": "a"}]
        for d in data:
            url = self.url + f"?from={d['start']}&to={d['end']}"
            response = requests.get(url=url)
            result = (response.json(), response.status_code)
            assert result == ({"status": "start/end is not a digit"}, 400)

    def test_from_greater_than_to(self):
        start, end = 2, 1
        url = self.url + f"?from={start}&to={end}"
        response = requests.get(url=url)
        result = (response.json(), response.status_code)
        assert result == ({"status": "'from' is greater than 'to'"}, 400)
