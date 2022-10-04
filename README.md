# shortlink
docker container와 fastapi를 활용한 url 단축 서비스
***
## 환경
python 3.10 버전 사용  
사용 라이브러리 : requirements.txt 참고
***
## 디렉토리 구조
```
├── app                      shortlink Dockernize
└── docker-compose.yml       docker compose
```
***
docker compose env 파일을 생성하거나 docker-compose.yml에 직접 database password를 세팅해준다.  
```shell
MYSQL_ROOT_PASSWORD="yourpassword"
```
최초에 mysql container를 띄우고 shortlink database를 생성해준다.
```sql
create database shortlink;
```
***
### short link 요청
```http request
POST http://localhost:80/shortlink/short-links
Content-Type: application/json

{
  "url": "https://www.google.com"
}
```
### 생성된 short link로 redirect 요청
```http request
GET http://localhost:80/ab180/short-links/{short_link}
```
