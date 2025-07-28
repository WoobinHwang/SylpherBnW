import pymysql

host='dnqls0326.mysql.pythonanywhere-services.com'
user='dnqls0326'
password='system123'
db='dnqls0326$sgeni'
charset='utf8'

db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

cursor = db.cursor();

## table information ##
# 테이블명 : sylpherbnw
# 컬럼 : 행 식별값, 사용자 식별값, 접속 채널명, 점수 , 진행턴수, 보유 타일, 사용 타일,  순서 , 제출시간
# 컬럼 :  row_id ,    user_id  ,  channel , score,  turn ,   have_tile  , use_tile , order, datetime

sql = """
    CREATE TABLE products (
        row_id INT AUTO_INCREMENT PRIMARY KEY
        , user_id VARCHAR(100) NOT NULL
        , channel INT
        , score INT
        , turn INT
        , have_tile VARCHAR(20)
        , use_tile INT
        , order VARCHAR(100)
        , datetime DATETIME)
"""

cursor.execute(sql) # SQL 쿼리문 실행
db.commit() # DB 변경사항 반영

print("connection good!!");