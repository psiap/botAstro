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

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM astrabotbd.table_users;")
        return self.cursor.fetchall()

    def edit_location_from_user(self, user_id, location):
        self.cursor.execute(
            f"UPDATE `astrabotbd`.`table_users` SET `city_now` = '{location}' where `user_id` = '{user_id}';")
        return self.conn.commit()

    def get_users(self,user_id):
        self.cursor.execute(f"SELECT * FROM astrabotbd.table_users where `user_id` = '{user_id}';")
        return self.cursor.fetchone()




    def get_check_user_free_version(self, user_id):
        self.cursor.execute(f"SELECT * FROM astrabotbd.table_users where `user_id` = '{user_id}';")
        result = self.cursor.fetchone()
        if result['date_subs'] == None and result['treal'] == '0':
            data_save = datetime.datetime.now() + datetime.timedelta(days=3)
            self.cursor.execute(f"UPDATE `astrabotbd`.`table_users` SET `date_subs` = '{data_save}', `treal` = '1' where `user_id` = '{user_id}';")
            self.conn.commit()
            return data_save.strftime("%d.%m.%Y %H:%M")
        else:
            return

    def get_check_user_frends(self, user_id):
        self.cursor.execute(f"SELECT * FROM astrabotbd.table_frend_subs where `userid` = '{user_id}';")
        return self.cursor.fetchone()


    def get_check_user_frends_delete(self, keyid):
        self.cursor.execute(f"DELETE FROM `astrabotbd`.`table_frend_subs` WHERE (`keyid` = '{keyid}');")
        return self.conn.commit()


    def get_start_check_user(self, user_id, username, date_register):
        self.cursor.execute(f"SELECT * FROM astrabotbd.table_users where `user_id` = '{user_id}';")
        if self.cursor.fetchone():
            pass
        else:
            self.cursor.execute(f"INSERT INTO `astrabotbd`.`table_users` (`user_id`, `username`, `date_register`) "
                                f"VALUES ('{user_id}', '{username}', '{date_register}');")
            return self.conn.commit()

    def add_subs_users(self, user_id, date_subs):
        self.cursor.execute(f"UPDATE `astrabotbd`.`table_users` SET `date_subs` = '{date_subs}' WHERE (`user_id` = '{user_id}');")
        return self.conn.commit()

    def add_tranz_users(self,user_id, money, date_tranz):
        self.cursor.execute(f"INSERT INTO `astrabotbd`.`table_tranz` (`user_id`, `money`, `day`) "
                            f"VALUES ('{user_id}', '{money}', '{date_tranz}');")
        return self.conn.commit()



    def add_frend_subs(self,userid,daysubs):
        self.cursor.execute(f"INSERT INTO `astrabotbd`.`table_frend_subs` (`userid`, `daysubs`) VALUES ('{userid}', '{daysubs}');")
        return self.conn.commit()


    def edit_forecast_users(self,user_id, when_forecast):
        self.cursor.execute(f"UPDATE `astrabotbd`.`table_users` SET `when_forecast` = '{when_forecast}' WHERE (`user_id` = '{user_id}');")
        return self.conn.commit()

    def add_user_info_natal(self,user_id,name,floor,place_of_birth,date_of_birth,time_of_birth,city_now,when_forecast):
        self.cursor.execute(f"UPDATE `astrabotbd`.`table_users` SET `name` = '{name}', `floor` = '{floor}', "
                            f"`place_of_birth` = '{place_of_birth}', `date_of_birth` = '{date_of_birth}',"
                            f" `time_of_birth` = '{time_of_birth}',"
                            f" `city_now` = '{city_now}', `when_forecast` = '{when_forecast}' WHERE (`user_id` = '{user_id}');")
        return self.conn.commit()


    def edit_users_count_img(self,user_id,count_img):
        self.cursor.execute(f"UPDATE `astrabotbd`.`table_users` SET `count_img` = '{count_img}' WHERE (`user_id` = '{user_id}');")
        return self.conn.commit()