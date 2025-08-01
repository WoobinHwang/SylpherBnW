import pymysql
import datetime

host='dnqls0326.mysql.pythonanywhere-services.com'
user='dnqls0326'
password='system123'
db='dnqls0326$sgeni'
charset='utf8'
first_tile = "4333222211111000000"
current_time = datetime.datetime.now()

db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

cur = db.cursor();


# # # drop ##
# sql = """
#     DROP TABLE sylpherbnw
# """
# cur.execute(sql)
# db.commit() # DB 변경사항 반영


# # ## table information ##
# # # 테이블명 : sylpherbnw
# # # 컬럼 : 행 식별값, 사용자 식별값, 접속 채널명, 점수 , 진행턴수, 보유 타일, 사용 타일, 사용자순서 ,  제출시간
# # # 컬럼 :  row_id ,    user_id  ,  channel , score,  turn ,   have_tile  , use_tile ,   user_order, send_datetime
# # #                                                                                      next_order로 바꿀 필요가 있음
# # # create
# sql = """
#     CREATE TABLE sylpherbnw (
#         row_id INT AUTO_INCREMENT PRIMARY KEY
#         , user_id VARCHAR(100) NOT NULL
#         , channel VARCHAR(100)
#         , score INT
#         , turn INT
#         , have_tile VARCHAR(100)
#         , use_tile INT
#         , user_order VARCHAR(100)
#         , send_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
# """
# cur.execute(sql) # SQL 쿼리문 실행
# db.commit() # DB 변경사항 반영


# ## insert ##
# sql = """
#     INSERT INTO sylpherbnw (user_id, channel, score, turn, have_tile, user_order)
#     VALUES ('sugo', 'sgenius', 0, 0, %s, '')
# """
# cur.execute(sql, (first_tile)) # SQL 쿼리문 실행
# db.commit() # DB 변경사항 반영


## select ##
    # cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
    # user_last_rows = cur.fetchone()
    # print(user_last_rows)



sql= """
    SELECT * FROM sylpherbnw
"""
text = 'sgenius'
channel = "'%s'" %(text)
cur.execute(sql)
# cur.execute("SELECT * FROM sylpherbnw WHERE channel!=%s;" %(channel))
all_rows = cur.fetchall()
print(len(all_rows))
print(all_rows)

cur.close() # # cur 객체 연결 해제
db.close() # # db 인스턴스 연결 해제

# cur.execute(sql) # SQL 쿼리문 실행
# db.commit() # DB 변경사항 반영

print("connection good");