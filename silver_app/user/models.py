import datetime as dt


from silver_app.database import Model, Column, SurrogatePK
from silver_app.extensions import db
from silver_app.extensions import bcrypt


class User(SurrogatePK, Model):

    __tablename__ = "users"

    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.LargeBinary(128), nullable = True)
    created_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
    updated_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
    




    def __init__(self, username, email, password = None, **kwargs):

        Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """ Set password """
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):

        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)