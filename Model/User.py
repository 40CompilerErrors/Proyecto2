import hashlib

from Utilities import DB_Driver as DB


class User:

    def validate(self, username, password):

        db = DB.DB_Driver()
        db_hash, db_role = self.getUser(username)

        if db_hash == 0 and db_role == 0:
            return False, 0

        hashed_password = hashlib.sha512(password.encode('utf8')).hexdigest()

        if not hashed_password == db_hash:
            return False, 1
        else:
            return True, db_role

        db.closeConnection()

    def getUser(self, username):

        db = DB.DB_Driver()

        query = """SELECT password_hash, isAdmin FROM users WHERE username = ?"""
        clean_user = db.sanitizeInput(username)
        db.cursor.execute(query, (clean_user,))
        result = db.cursor.fetchone()
        if result is not None:
            return result[0], result[1]
        else:
            print("No users with a matching username found")
            return 0, 0

        db.closeConnection()

    def registerUser(self, username, password):

        db = DB.DB_Driver()

        query = """INSERT INTO users (username, password_hash, isAdmin) VALUES (?, ?, 0)"""
        username = db.sanitizeInput(username)
        hashed_password = hashlib.sha512(password.encode('utf8')).hexdigest()
        try:
            db.cursor.execute(query, (username, hashed_password))
            db.connection.commit()
        except:
            print("ERROR: Query unsuccessful: register user")


        db.closeConnection()

    def deleteUser(self, username):
        db = DB.DB_Driver()

        query = """DELETE FROM users WHERE username = %s"""
        username = db.sanitizeInput(username)
        try:
            db.cursor.execute(query, (username,))
            db.connection.commit()
        except:
            print("ERROR: Query unsuccessful: register user")

        db.closeConnection()

    def getUserList(self):
        db = DB.DB_Driver()

        query = """SELECT username FROM users WHERE isAdmin = 0"""
        db.cursor.execute(query)
        # result = self.cursor.fetchall()
        result = list(db.cursor)
        # print(result)
        return result

        db.closeConnection()
