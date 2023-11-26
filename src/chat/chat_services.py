from src.exceptions import DoesNotExist


class ChatSelector:
    def get_all_chats(self, db):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM Chat")
            result = cursor.fetchall()
        return result

    def get_all_chats_verbose(self, db):
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT Chat.id, c.username AS customer, a.username AS admin "
                "FROM Chat "
                "LEFT JOIN User c ON Chat.customer_id=c.id "
                "LEFT JOIN User a ON Chat.admin_id=a.id; "
            )
            result = cursor.fetchall()
        return result

    def get_chat_by_id(self, db, chat_id):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM Chat WHERE Chat.id=%s", chat_id)
            result = cursor.fetchone()
        return result

    def get_chat_by_customer_id(self, db, customer_id):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM Chat WHERE Chat.customer_id=%s",
                           customer_id)
            result = cursor.fetchone()
        return result

    def get_chat_history_by_id(self, db, chat_id):
        with db.cursor() as cursor:
            cursor.execute("SELECT text, User.username as from_user, datetime "
                           "FROM Message "
                           "LEFT JOIN User ON User.id = Message.from_user_id "
                           "WHERE Message.chat_id=%s;",
                           chat_id)
            result = cursor.fetchall()
        return result

    def get_chat_users(self, db, chat_id):
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM User WHERE id IN "
                "(SELECT admin_id FROM Chat WHERE id=%s "
                "UNION SELECT customer_id FROM Chat WHERE id=%s);",
                (chat_id, chat_id))
            result = cursor.fetchall()
        return result

    def get_chat_opponent(self, db, chat_id, first_user_id):
        users = self.get_chat_users(db, chat_id)
        for user in users:
            if user["id"] != first_user_id:
                return user


class ChatService:
    def create_chat(self, db, customer_id, admin_id=None):
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Chat(customer_id, admin_id) "
                "VALUES (%s, %s); ",
                (customer_id, admin_id),
            )
        db.commit()
        with db.cursor() as cursor:
            cursor.execute("SELECT LAST_INSERT_ID() id;")
            chat_id = cursor.fetchone()
        return chat_id

    def get_or_create_chat_by_customer_id(self, db, customer_id):
        chat = ChatSelector().get_chat_by_customer_id(db, customer_id)
        if chat is None:
            chat_id = self.create_chat(db, customer_id)
        else:
            chat_id = chat
        return chat_id

    def insert_message(self, db, chat_id, from_user_id, datetime, text):
        chat = ChatSelector().get_chat_by_id(db, chat_id)
        if chat:
            with db.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Message(chat_id, from_user_id, datetime, text) "
                    "VALUES (%s, %s, %s, %s)",
                    (chat_id, from_user_id, datetime, text),
                )
            db.commit()
        else:
            raise DoesNotExist("chat not found")

    def link_chat_to_admin(self, db, chat_id, admin_id):
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE Chat "
                "SET admin_id = %s "
                "WHERE id = %s; ",
                (admin_id, chat_id),
            )
        db.commit()
