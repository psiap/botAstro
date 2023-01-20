import datetime
import pymysql

from utils.db_api.configdb import *

class BotDB:

    def __init__(self):
        self.conn = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def add_room_meet(self,userid,username,day,time,room):
        date_temp_h = datetime.datetime.strptime(time, "%H:%M:%S")
        n_d = f"{date_temp_h + datetime.timedelta(minutes=30)}".split(' ')[-1]
        self.cursor.execute(f"SELECT * FROM `roommeet`.`users` where (`day` = '{day}') and (`time` = '{time}') and (`room` = '{room}');")
        if self.cursor.fetchone():
            return False
        else:
            self.cursor.execute(
                f"SELECT * FROM `roommeet`.`users` where (`day` = '{day}') and (`time` = '{n_d}') and (`room` = '{room}');")
            if self.cursor.fetchone():
                return False
            else:
                self.cursor.execute(f"INSERT INTO `roommeet`.`users` (`userid`, `username`, `day`, `time`, `room`) "
                                    f"VALUES ('{userid}', '{username}', '{day}', '{n_d}', '{room}');")
                self.conn.commit()
                self.cursor.execute(f"INSERT INTO `roommeet`.`users` (`userid`, `username`, `day`, `time`, `room`) "
                                    f"VALUES ('{userid}', '{username}', '{day}', '{time}', '{room}');")
                self.conn.commit()
                return True


    def edit_pid_bot(self,apitoken,pid):
        self.cursor.execute(f"SELECT * FROM subsbotbd.bots_bd where (`apitoken` = '{apitoken}');")
        answer = self.cursor.fetchone()
        if answer:
            self.cursor.execute(f"UPDATE `subsbotbd`.`bots_bd` SET `pid` = '{pid}' WHERE (`apitoken` = '{apitoken}');")
            self.conn.commit()
