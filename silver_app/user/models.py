import datetime as dt


from silver_app.database import Model, Column, SurrogatePK
from silver_app.extensions import db



class User(SurrogatePK, Model):

    __tablename__ = "users"

    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.LargeBinary(128), nullable = True)
    created_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
    updated_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
    

