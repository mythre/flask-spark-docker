Forked from  mjhea0/flask-spark-docker for the basic environment docker(flask+spark+redis)

### Quick Start

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Application runs at http://localhost:5009

To post the request:
once the containers up,
run form_request in web container:
```sh
$docker exec -it web bash
python client/form_request.py
 ```


