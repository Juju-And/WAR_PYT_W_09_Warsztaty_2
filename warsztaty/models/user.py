from clcrypto import password_hash, check_password


class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, raw_password, salt):
        self.__hashed_password = password_hash(raw_password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO Users(username, email, hashed_password)
                     VALUES(%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, email=%s, hashed_password=%s
                                              WHERE id=%s"""
            values = (self.username, self.email, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user

    @staticmethod
    def load_user_by_name_and_pass(cursor, user_name, user_pass):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (user_name,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data and check_password(user_pass, data[3]):
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        return True

    @staticmethod
    def delete_by_username(cursor, username):
        sql = "DELETE FROM users WHERE username=%s"
        cursor.execute(sql, (username,))

    @staticmethod
    def update_password(ctx, new_raw_password, username):
        sql = "UPDATE users SET hashed_password=%s WHERE username=%s"
        # new_pass = self.set_password(raw_password, None)
        cursor = ctx.cursor()
        cursor.execute(sql, (new_raw_password, username))
        ctx.commit()

    def __repr__(self):
        return '{}, {}, {}'.format(self.id, self.username, self.email)
