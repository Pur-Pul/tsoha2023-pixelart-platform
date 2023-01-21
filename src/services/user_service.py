from werkzeug.security import check_password_hash

class UserService:
    def __init__(self, db):
        self._db = db
    
    def _fetch_user(self, username):
        user = self._db.session.execute(
            "SELECT id, password FROM users WHERE username=:username",
            {"username":username}
        ).fetchone()
        return user

    def validate_credentials(self, username, password):
        user = self._fetch_user(username)
        return user and check_password_hash(user.password, password)
    
    def register(self, username, hash_value):
        if self._fetch_user(username):
            return False
        else:
            self._db.session.execute(
                "INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username":username, "password":hash_value}
            )
            self._db.session.commit()