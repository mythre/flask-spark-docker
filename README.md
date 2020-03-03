Forked from  mjhea0/flask-spark-docker for the basic environment docker(flask+spark+redis)

### Quick Start

Spin up the containers:

```sh
$ docker-compose up -d --build
```
Download the resource from https://www.kaggle.com/datafiniti/womens-shoes-prices/

unzip and copy the csv named 7210_1.csv to the  path as  flask-spark-docker/services/web/project/Latest_women_shoes.csv




Application runs at http://localhost:5009

To post the request:
to up the dockers run the below command inside the checkout folder
 ```sh
$docker-compose up
 ```
Run form_request in web container:
```sh
$docker exec -it web bash
python client/form_request.py
 ```


