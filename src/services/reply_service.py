class ReplyService:
    def __init__(self, database = None):
        if database is None:
            from db import db
            self._db = db
        else:
            self._db = database

    def _create_main_reply(self) -> int:
        reply_id = self._db.session.execute(
            """
            INSERT INTO replies (
                reply_id,
                user_id,
                content
            ) VALUES (
                :reply_id,
                :user_id,
                :content
            )
            RETURNING id
            """, {
                "reply_id": -1,
                "user_id": -1,
                "content": ""
            }

        ).fetchone()[0]
        self._db.session.commit()
        return reply_id

    def create_reply_section(self, post_id):
        main_reply_id = self._create_main_reply()
        self._db.session.execute(
            """
            INSERT INTO reply_section (
                post_id,
                reply_id
                ) VALUES (
                    :post_id,
                    :reply_id
                )
            """, {
                "post_id": post_id,
                "reply_id": main_reply_id
            }
        )
        self._db.session.commit()

    def create_reply(self, reply_id, user_id, content):
        self._db.session.execute(
            """
            INSERT INTO replies (
                reply_id,
                user_id,
                content
            )
            VALUES (
                :reply_id,
                :user_id,
                :content
            )
            """, {
                "user_id":user_id,
                "reply_id":reply_id,
                "content":content
            }
        )
        self._db.session.commit()

    def create_vote(self, reply_id, user_id, points):
        self._db.session.execute(
            """
            INSERT INTO votes (
                reply_id,
                user_id,
                points
            ) VALUES (
                :reply_id,
                :user_id,
                :points
            )
            ON CONFLICT (reply_id, user_id)
            DO NOTHING;
            """, {
                "reply_id":reply_id,
                "user_id":user_id,
                "points":points
            }
        )
        self.commit()

    def create_post_vote(self, post_id, user_id, points):
        self._db.session.execute(
            """
            INSERT INTO votes (
                reply_id,
                user_id,
                points
            )
            SELECT reply_id, :user_id, :points
            FROM reply_section
            WHERE post_id=:post_id
            ON CONFLICT (reply_id, user_id)
            DO UPDATE SET points = EXCLUDED.points;
            """, {
                "user_id":user_id,
                "points":points,
                "post_id":post_id
            }
        )
        self._db.session.commit()

    def create_post_reply(self, post_id, user_id, content):
        self._db.session.execute(
            """
            INSERT INTO replies (
                reply_id,
                user_id,
                content
            )
            SELECT reply_id, :user_id, :content
            FROM reply_section
            WHERE post_id=:post_id
            """, {
                "user_id":user_id,
                "content":content,
                "post_id":post_id
            }
        )
        self._db.session.commit()

    def get_post_replies(self, post_id):
        replies = self._db.session.execute(
            """
            SELECT replies.*, users.username
            FROM replies
            LEFT JOIN users
            ON replies.user_id = users.id
            WHERE reply_id=(SELECT reply_id FROM reply_section WHERE post_id=:post_id)
            """, {
                "post_id":post_id
            }
        ).fetchall()
        return replies
