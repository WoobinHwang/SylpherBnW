from flask import Flask, request
import pymysql
import datetime

app = Flask(__name__)

first_tile = "4333222211111000000"
current_time = datetime.datetime.now()

# db = pymysql.connect(
#     host='dnqls0326.mysql.pythonanywhere-services.com'
#     , user='dnqls0326'
#     , password='system123'
#     , db='dnqls0326$sgeni'
#     , charset='utf8')

# cur = db.cursor();


@app.route('/')
def hello_world():
    return 'welcome anywhere user'

@app.route('/api/hello', methods=['POST'])
def hello():
    # body = request.get_json() # 사용자가 입력한 데이터

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "시작하셔도 됩니다."
                    }
                }
            ]
        }
    }

    return responseBody

# 유저가 입력 한 값 반환
@app.route('/api/test', methods=['POST'])
def test():
    body = request.get_json() # 사용자가 입력한 데이터

    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    sql= """
    SELECT * FROM sylpherbnw
    """

    cur.execute(sql)
    all_rows = cur.fetchall()

    sql= """
    SELECT * FROM sylpherbnw where channel = 'sgenius'
    """

    cur.execute(sql)
    all_rows2 = cur.fetchall()

    print(all_rows);
    print(all_rows2);

    # 입력값 줄바꿈 제거
    body2 = str(body['userRequest']['utterance']).strip()
    userID = str(body['userRequest']['user']['id'])



    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": body2 + "입력완료!  \n" + userID
                    }
                }
            ]
        }
    }

    return responseBody


# # 채널 접속
@app.route('/api/enterchannel', methods=['POST'])
def enterchannel():

    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    try:
        body = request.get_json() # 사용자가 입력한 데이터


        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        try :
            text = body['userRequest']['utterance'].split(" ")[0]
        except :
            text = "korea"


        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        channel_data = '%s' %text
        channelchannel_data = "'%s'" %text
        sql = """
            SELECT * FROM sylpherbnw WHERE channel=%s;
        """
        cur.execute(sql, (channel_data))
        rows = cur.fetchall()
        print(rows)

        sql ="""
            SELECT * FROM sylpherbnw WHERE channel=%s AND user_id=%s;
        """
        cur.execute(sql, (channel_data, id_data))
        rows2 = cur.fetchall()
        print(rows2)


        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s;" ,(id_data))
        rows3 = cur.fetchall()
        print(rows3)


        if len(rows2) != 0:
            result = "해당 채널에 이미 접속중이십니다"
        elif len(rows3) != 0:
            result = "이미 다른 채널에 접속중이십니다"
        elif len(rows) < 2:
            # 정상적으로 접속한 경우
            sql = """
                INSERT INTO sylpherbnw (user_id, channel, score, turn, have_tile, user_order) VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (id_data, channel_data, 0, 0, first_tile, "") )
            db.commit()
            result = "채널에 참가하였습니다"
        else :
            result = "해당 채널에 이미 사람이 다 찼습니다."
    except:
        result = "문제 발생 관리자에게 문의해주세요"


    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody

# # 채널 초기화
@app.route('/api/initializing', methods=['POST'])
def initializing():

    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    try:
        body = request.get_json() # 사용자가 입력한 데이터


        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])


        cur.execute("DELETE FROM sylpherbnw WHERE user_id=%s;" %(idid_data))
        db.commit()
        result = "모든 채널에 있던 데이터들을 삭제하였습니다."
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제


    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 타일 제출하기
@app.route('/api/submittile', methods=['POST'])
def submitnumber():
    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();
    result = "무슨 결\n과가 나올까요"

    try:

        body = request.get_json() # 사용자가 입력한 데이터

        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        round_winner = '%s' %("first")
        round_loser = '%s' %("second")


        target_data = body['userRequest']['utterance']

        if (target_data == '발화 내용'):
            text = '0'
        else:
            text = target_data.split(" ")[0]


        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND turn=0;", (id_data))
        find_channel = cur.fetchall()
        userchannel = find_channel[0][2]
        channel_data = '%s' %(userchannel)
        channelchannel_data = "'%s'" %(userchannel)

        print("---------------------test else line 13----------------------")
        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s;", (id_data, channel_data))
        enemy_rows = cur.fetchall()
        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s;", (id_data, channel_data))
        user_rows = cur.fetchall()


        where_user_turn = len(user_rows)-1
        where_enemy_turn = len(enemy_rows)-1
        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s AND turn=%d;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()
        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s AND turn=%d;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()
        print("last rows")
        print(user_last_rows)
        print(enemy_last_rows)

        # # 이미 6점이면 바로 종료
        if(user_last_rows[3] >= 6 or enemy_last_rows[3] >= 6):
            result = "이미 게임이 끝나있습니다\n'나' %d : %d '상대'" % (user_last_rows[3], enemy_last_rows[3]);
        else:
            print("come else line")
            ### 유저가 갖고있는 타일 리스트 ###
            user_have_tile = list(user_last_rows[5])
            print(user_have_tile)
            user_use_tile = list(text)
            print(user_use_tile)
            use_success = True;

            try:
                for use_index in range(len(user_use_tile)):
                    for have_index in range(len(user_have_tile)-1, -1, -1):

                        if(user_use_tile[use_index] == user_have_tile[have_index]):
                            print("delete %d, %d" %(use_index, have_index))
                            del user_have_tile[have_index];
                            break;
                        ### 갖고있지 않는 타일을 발견 ###
                        elif have_index == 0 and use_index == len(user_use_tile)-1:
                            use_success = False;
            except:
                use_success = False;

            print("using check end")
            print(use_success)
            next_have_tile = ""
            if(use_success == True):
                next_have_tile = (''.join(user_have_tile))
            # # 보유 타일보다 더 많이 제출하려고 할 때
            if (use_success == False) :
                result = "타일이 부족합니다.\n다시 제출하세요."

            # # 상대가 없을 때
            elif (len(enemy_rows) == 0):
                    result = "상대방이 들어오지 않았습니다."

            else:
                # # 숫자로 정상적으로 제출
                # # 1라운드는 길이가 같을 때 입력한 사람이 제출
                if(len(user_rows) == len(enemy_rows)) :
                    if (user_last_rows[7] == 'second'):
                        result = "상대방의 차례입니다. 기다려주세요."

                    ### 보유한 타일만 제출했는지 확인
                    else:
                        print("do insert use tile")
                        cur.execute("INSERT INTO sylpherbnw (user_id, channel, score, turn, have_tile, use_tile, user_order) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[3], user_last_rows[4] + 1, int(next_have_tile), int(text), '' ) )
                        db.commit()
                        result = "%s라운드 제출 완료!" %(user_last_rows[4] + 1)
                elif(len(user_rows) > len(enemy_rows)):
                    result = "상대방이 제출 할 차례입니다."
                elif(len(user_rows) < len(enemy_rows)):

                    # # 양쪽 다 제출했으니 숫자를 비교 할 예정
                    enemy_num = enemy_last_rows[6]
                    user_num = int(text)

                    # # 제출 한 사람이 승리 할 경우
                    if (user_num > enemy_num):
                        # # 유저 승리로 입력
                        cur.execute("INSERT INTO sylpherbnw (user_id, channel, score, turn, have_tile, use_tile, user_order) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[3] + 1, user_last_rows[4] + 1, int(next_have_tile), int(text), round_winner ))
                        # # 상대 패배로 입력
                        print("enemy turn : ", where_enemy_turn)
                        cur.execute("UPDATE sylpherbnw SET user_order=%s WHERE user_id!=%s AND channel=%s AND turn=%s;"
                            , (round_loser, id_data, channel_data, where_enemy_turn))
                        db.commit()
                        result = "%s라운드 제출 완료\n당신이 승리하였습니다\n현재점수 본인 %s : %s 상대방"%(user_last_rows[4] + 1, user_last_rows[3] + 1, enemy_last_rows[3])
                        if (user_last_rows[3]+1 >= 6):
                            result = result + "\n'나'의 승리로 게임을 종료합니다."

                    # # 상대방이 승리 할 경우
                    elif (user_num < enemy_num):
                        # # 유저 패배로 입력
                        cur.execute("INSERT INTO sylpherbnw (user_id, channel, score, turn, have_tile, use_tile, user_order) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[3], user_last_rows[4] + 1, int(next_have_tile), int(text), round_loser ))
                        # # # 상대 승리로 입력
                        cur.execute("UPDATE sylpherbnw SET score=%s , user_order=%s WHERE user_id!=%s AND channel=%s AND turn=%s;"
                            , ( enemy_last_rows[3]+1, round_winner, id_data, channel_data, where_enemy_turn))
                        db.commit()
                        result = "%s라운드 제출 완료!\n상대방이 승리하였습니다...\n현재점수 본인 %s : %s 상대방" %(user_last_rows[4] + 1, user_last_rows[3], enemy_last_rows[3] + 1)

                        if (enemy_last_rows[3]+1 >= 6):
                            result = result + "\n상대방의 승리로 게임을 종료합니다."


                    # # 무승부인 상황
                    elif (user_num == enemy_num):
                        cur.execute("INSERT INTO sylpherbnw (user_id, channel, score, turn, have_tile, use_tile, user_order) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[3], user_last_rows[4] + 1, int(next_have_tile), int(text), user_last_rows[7]))
                        # # 상대 무승부 입력
                        enemy_order = '%s' %(enemy_last_rows[7])
                        cur.execute("UPDATE sylpherbnw SET user_order=%s WHERE user_id!=%s AND channel=%s AND turn=%s;"
                            , (enemy_order, id_data, channel_data, where_enemy_turn))
                        db.commit()
                        result = "무승부입니다!\n선 플레이어부터 다시 시작해주세요.\n현재점수 나 %s : %s 상대방"%(user_last_rows[3], enemy_last_rows[3])

    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제


    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 중간에 현재 상황 알림
@app.route('/api/infomation', methods=['POST'])
def infomation():
    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    try:
        body = request.get_json() # 사용자가 입력한 데이터


        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND turn=0;" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][2]
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()

        print("find last rows")

        # # 타일종류

        # # 상대 타일 개수 확인
        tile_light = len(enemy_last_rows[5])
        # # 서로 제출을 안 한 상태에서
        # # 가지고있는 포인트, 점수

        result = "현재 %s라운드\n점수\n'나' %s : %s '상대'\n내가 가진 타일: %s\n상대가 가진 타일수: %s개" %(user_last_rows[4], user_last_rows[3], enemy_last_rows[3], user_last_rows[5], tile_light)
        if (len(user_rows) > len(enemy_rows)):
            result = result + "\n'나'는 %s 타일을 제출하였습니다" %(user_last_rows[6])

        elif (len(user_rows) < len(enemy_rows)):
            result = "현재 %s라운드\n점수\n'나' %s : %s '상대'\n내가 가진 타일: %s\n상대가 가진 타일수: %s개" %(enemy_last_rows[4], user_last_rows[3], enemy_last_rows[3], user_last_rows[5], tile_light)
            result = result + "\n'상대'는 %s자리의 타일을 제출하였습니다" %(len(enemy_last_rows[6]))
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 지난 결과 호출
@app.route('/api/previous', methods=['POST'])
def previous():
    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    try:

        body = request.get_json() # 사용자가 입력한 데이터


        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND turn=0;" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][2]
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()

        # # 상대 타일 정의

        tile = "%s자리" %(len(enemy_last_rows[6]))


        if (len(user_rows) == 1) or (len(enemy_rows) == 1) :
            result = "이전 라운드가 없습니다."
        elif (len(user_rows) == len(enemy_rows)) :
            result = "현재 %s라운드 제출 전이며\n지난 라운드에 상대방이 %s 타일을 제출하여 " %(len(user_rows), tile)
            if (user_last_rows[6] > enemy_last_rows[6]):
                result = result + "내가 이겼습니다."
            elif (user_last_rows[6] == enemy_last_rows[6]):
                result = result + "비겼습니다."
            elif (user_last_rows[6] < enemy_last_rows[6]):
                result = result + "상대가 이겼습니다."

        # # 유저가 3 , 상대가 2의 상황
        elif (len(user_rows) > len(enemy_rows)) :

            where_user_prev_turn = "'%s'" %(len(user_rows)-2)

            cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_prev_turn))
            user_previous_rows = cur.fetchone()

            result = "현재 %s라운드 진행중이며\n지난 %s라운드에 상대방이 %s 타일을 제출하여 " %(len(user_rows)-1, len(enemy_rows)-1, tile)

            if (user_previous_rows[6] > enemy_last_rows[6]):
                result = result + "내가 이겼습니다."
            elif (user_previous_rows[6] == enemy_last_rows[6]):
                result = result + "비겼습니다."
            elif (user_previous_rows[6] < enemy_last_rows[6]):
                result = result + "상대가 이겼습니다."


            # # 유저가 2 , 상대가 3의 상황
        elif (len(user_rows) < len(enemy_rows)) :

            where_enemy_prev_turn = "'%s'" %(len(enemy_rows)-2)

            cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_prev_turn))
            enemy_previous_rows = cur.fetchone()

            # # 상대 타일 재정의
            tile = "%s자리" %(len(enemy_previous_rows[6]))

            result = "현재 %s라운드 진행중이며\n지난 %s라운드에 상대방이 %s 타일을 제출하여 " %(len(enemy_rows)-1, len(user_rows)-1, tile)

            if (user_last_rows[6] > enemy_previous_rows[6]):
                result = result + "내가 이겼습니다."
            elif (user_last_rows[6] == enemy_previous_rows[6]):
                result = result + "비겼습니다."
            elif (user_last_rows[6] < enemy_previous_rows[6]):
                result = result + "상대가 이겼습니다."

        # # 결과에 점수 추가하여 마무리
        result = result + "\n현재 점수\n'나' %s : %s '상대'" %(user_last_rows[3], enemy_last_rows[3])
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 다 끝난 후 로그 보여주기
@app.route('/api/checklog', methods=['POST'])
def checklog():
    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    try:
        body = request.get_json() # 사용자가 입력한 데이터

        idid_data = "'%s'" %str(body['userRequest']['user']['id'])

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND turn=0;" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][2]
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()
        result = ""

        ###
        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()

        # # 타겟지점
        if (user_last_rows[3] >= 6) or (enemy_last_rows[3] >= 6):
            result = result + "로그보기"
            for i in range(1, len(user_rows)):

                where_user_turn = "'%s'" %(i)
                where_enemy_turn = "'%s'" %(i)

                cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
                user_target_row = cur.fetchone()
                cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
                enemy_target_row = cur.fetchone()

                result = result + "\n%d라운드 나 %s : %s 상대" %(i, user_target_row[6], enemy_target_row[6])
                print(result)

        else:
            result = "아직 게임이 끝나지 않았습니다.\n게임이 끝난후에 이용하시기 바랍니다."

    except:
        result = result + "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# 기권하기
@app.route('/api/giveup', methods=['POST'])
def giveup():

    db = pymysql.connect(
    host='dnqls0326.mysql.pythonanywhere-services.com'
    , user='dnqls0326'
    , password='system123'
    , db='dnqls0326$sgeni'
    , charset='utf8')

    cur = db.cursor();

    try:
        body = request.get_json() # 사용자가 입력한 데이터
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])


        cur.execute("SELECT * FROM sylpherbnw WHERE user_id=%s AND turn=0;" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][2]
        channelchannel_data = "'%s'" %(userchannel)


        cur.execute("SELECT * FROM sylpherbnw WHERE user_id!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("UPDATE sylpherbnw SET score=%s WHERE user_id!=%s AND channel=%s AND turn=%s;" % ( 6, idid_data, channelchannel_data, where_enemy_turn))
        db.commit()
        result = "항복하였습니다"

    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


if __name__ == "__main__":
    app.run()