import config
import MySQLdb


class Db:
    def __init__(self, log=True):
        self.log = log
        self.connect()

    def connect(self):
        self.db = db = MySQLdb.connect(
            host=config.db_host,
            user=config.db_user,
            passwd=config.db_pass,
            db="tmoneydiscord",
        )
        if self.log == True:
            print(f"Successfully connected to {config.db_host} as {config.db_user}")

        self.cur = db.cursor()

    def add_user(self, authorID):
        try:
            self.cur.execute(
                f"""INSERT INTO TMDiscord (userID, messages) VALUES ({str(authorID)}, 0)"""
            )
            self.db.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.cur.execute(
                f"""INSERT INTO TMDiscord (userID, messages) VALUES ({str(authorID)}, 0)"""
            )
            self.db.commit()

    def increase_messages(self, userID):
        try:
            self.cur.execute(
                f"""UPDATE TMDiscord SET messages = messages + 1 where userID = '{str(userID)}'"""
            )
            self.db.commit()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.cur.execute(
                f"""UPDATE TMDiscord SET messages = messages + 1 where userID = '{str(userID)}'"""
            )
            self.db.commit()

    def get_messages(self, userID):
        try:
            self.cur.execute(
                f"""SELECT messages FROM TMDiscord WHERE userID = {str(userID)}"""
            )
            return self.cur.fetchone()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.cur.execute(
                f"""SELECT messages FROM TMDiscord WHERE userID = {str(userID)}"""
            )
            return self.cur.fetchone()

        
    def add_swear(self, userID, swear, no):
        try:
           self.cur.execute(
                f"""UPDATE TMDiscord SET {swear} = {swear} + {no} where userID = '{str(userID)}'"""
            )
            
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.cur.execute(
                f"""UPDATE TMDiscord SET {swear} = {swear} + 1 where userID = '{str(userID)}'"""
            )
        self.db.commit()

    def get_profile(self, userID):
        try:
            self.cur.execute(
                f"""SELECT * FROM TMDiscord WHERE userID = {str(userID)}"""
            )
            return self.cur.fetchone()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            self.cur.execute(
                f"""SELECT * FROM TMDiscord WHERE userID = {str(userID)}"""
            )
            return self.cur.fetchone()
            
        

if __name__ == "__main__":
    inp = input("Type Y to continue, this may override content: ")
    if inp == "Y":
        database = Db()
        database.cur.execute("""DROP TABLE TMDiscord""")
        database.cur.execute("""CREATE TABLE TMDiscord (
                                    userID VARCHAR(250) PRIMARY KEY,
                                    messages INT DEFAULT 0,
                                    fuck INT DEFAULT 0,
                                    shit INT DEFAULT 0,
                                    cunt INT DEFAULT 0,
                                    bitch INT DEFAULT 0,
                                    peenus INT DEFAULT 0,
                                    asshole INT DEFAULT 0,
                                    dick INT DEFAULT 0,
                                    peen INT DEFAULT 0,
                                    wanker INT DEFAULT 0,
                                    dickhead INT DEFAULT 0
        )""")
        database.db.commit()

        print("JOBS DONE!")

