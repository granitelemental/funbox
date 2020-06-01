### Usage

1) docker-compose up db
2) pip install -r requirements.txt
3) API:
    a) /visited_links - posts domains into database. 
    Request body format: {
        links: [
            "link1",
            "link2",
            ...
        ]
    }
    
    b) /visited_domains - gets domain names wisited in certain period.
    Agruments: from, to - utc timestamps. Default: -inf, +inf

4) Tests:
    TestPost - tests for saving visited domains.
    TestsGet - tests for getting visited domains
    
