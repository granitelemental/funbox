### Usage

1) DB: docker-compose up db
2) Requirements: pip install -r requirements.txt
3) API: python api.py
4) Requests:

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

4) Tests: pytest

        TestPost class- tests for saving visited domains,
        TestsGet class- tests for getting visited domains.


### Comments
До этого задания я не имела дела с юнит-тестами, так что код может выглядеть странно.
    
