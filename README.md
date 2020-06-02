### Usage

1) Build a docker-image for api: docker-compose build
2) Run Redis db: docker-compose up db
3) Run api: docker-compose up api
4) Requests to api:

        a) /visited_links - posts domains into database. 
        Request body format: 
        {
            "links": [
                "link1",
                "link2",
                ...
            ]
        }

        b) /visited_domains - gets domain names wisited in certain period.
        Agruments: "from", "to" - utc timestamps. Default: "-inf", "+inf".

5) Tests: python flask_test.py

        TestPost class- tests for saving visited domains,
        TestsGet class- tests for getting visited domains.


### Comments
У меня есть начальные навыки работы с docker-compose, поэтому я подумала, что было бы удобно иметь возможность запускать api на сервере без Python. 
Но до этого задания я не имела дела с юнит-тестами и не знаю, как их использовать с docker-compose, поэтому запуск тестов осуществляется просто строкой "python flask_test.py".
    
