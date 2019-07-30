class Message:
    __id = None
    from_id = None
    to_id = None
    context = None
    created_at = None

    def __init__(self):
        self.__id = -1
        from_id = -1
        to_id = -1
        context = ""
        created_at = "now()"

    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = """
                SELECT id, from_id, to_id, context, created_at 
                FROM messages
                WHERE id = %s
            """
        cursor.execute(sql, (message_id,))
        data = cursor.fetchone()

        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.context = data[3]
            loaded_message.created_at = data[4]
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = """
                SELECT id, from_id, to_id, context, created_at
                FROM messages
                WHERE to_id = %s
            """
        ret = []
        cursor.execute(sql, (user_id,))

        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.context = row[3]
            loaded_message.created_at = row[4]
            ret.append(loaded_message)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        pass

    def save_to_db(self, cursor):
        pass

    def delete(self, cursor):
        pass
