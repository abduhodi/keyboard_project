from mysql.connector import connect, DatabaseError
from widgets.user import User


class Database:
    def __init__(self) -> None:
        self.__host = 'bjx8tyzoqumbaxwklyoe-mysql.services.clever-cloud.com'
        self.__user = 'uufv6yksi7xglkum'
        self.__passwd = '053bpesEBetThfyNE7Hm'
        self.__database = 'bjx8tyzoqumbaxwklyoe'
    
    
    def connect_db(self):
        DB = connect(
            host = self.__host,
            user = self.__user,
            passwd = self.__passwd,
            database = self.__database
        )
        return DB


    def write(self, user: User):
        query = """
        INSERT INTO Users (name, email, telegramId, password, easy, medium, hard, expert) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            user.name,
            user.email,
            user.telegramId,
            user.passwd,
            user.easy,
            user.medium,
            user.hard,
            user.expert
            )
        try:
            DB = self.connect_db()
            cur = DB.cursor()
            cur.execute(query, data)
            DB.commit()
            return True
        except DatabaseError as db_err:
            print(db_err)
            return False
        finally:
            DB.close()
    

    def read(self, email: str, passwd: str):
        try:
            DB = self.connect_db()
            cur = DB.cursor()
            cur.execute("SELECT * FROM Users WHERE email = %s and password = %s", (email, passwd))
            data = cur.fetchone()
            return data
        except DatabaseError as de:
            print(de)
            return None
        finally:
            DB.close()

    
    def update(self, user: User):
        try:
            DB = self.connect_db()
            cur = DB.cursor()
            cur.execute(
                "UPDATE Users SET easy = %s, medium = %s, hard = %s, expert = %s WHERE email = %s",
                (user.easy, user.medium, user.hard, user.expert, user.email)
                )
            DB.commit()
            return True
        except DatabaseError as de:
            print(de)
            return False
        finally:
            DB.close()

    
    def exist_email(self, email: str):
        try:
            DB = self.connect_db()
            cur = DB.cursor()
            cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
            data = cur.fetchone()
            if data:
                return True
            return False
        except DatabaseError as de:
            print(de)
            return False
        finally:
            DB.close()


    def exist_telegramId(self, telegramId: str):
        try:
            DB = self.connect_db()
            cur = DB.cursor()
            cur.execute("SELECT * FROM Users WHERE telegramId = %s", (telegramId,))
            data = cur.fetchone()
            if data:
                return True
            return False
        except DatabaseError as de:
            print(de)
            return False
        finally:
            DB.close()
        


# db = Database().connect_db()
# cur = db.cursor()
# cur.execute("desc Users")
# # print(cur)
# # db.commit()
# data = cur.fetchall()
# for i in data:
#     print(i)