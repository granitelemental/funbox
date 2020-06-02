### Usage

1) docker-compose build
2) docker-compose up
3) Requests to api:

- `POST /visited_links` - posts domains into database. Request body format: 
```
    {
        "links": [
            "link1",
            "link2",
            ...
        ]
    }
```

- `GET /visited_domains` - gets domain names wisited in certain period.
Agruments: `from`, `to` - utc timestamps. Default: `"-inf"`, `"+inf"`.

4) Tests: 

```
python flask_test.py
TestPost class- tests for saving visited domains,
TestsGet class- tests for getting visited domains.
```

### Comments
У меня есть начальные навыки работы с docker-compose, поэтому я подумала, что было бы удобно иметь возможность запускать api на сервере без Python. 
Но до этого задания я не имела дела с юнит-тестами и не знаю, как их использовать с docker-compose, поэтому запуск тестов осуществляется просто командой "python flask_test.py".