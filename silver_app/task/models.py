import datetime as dt


from silver_app.database import Model, Column, SurrogatePK , reference_col
from silver_app.extensions import db



class Task(SurrogatePK, Model):

    __tablename__ = "tasks"
    title = Column(db.String(80), nullable =False)
    user_id = reference_col("users", nullable=False)
    description = Column(db.String(500), nullable=True)
    due_date = Column(db.Date, nullable = True, index = True)
    status = Column(db.String(20), nullable = False, default = "pending", index = True)
    created_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
    updated_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
    

    def __init__(self, title, user_id, description = None, due_date= None, **kwargs):

        Model.__init__(
            self, 
            title=title,
            user_id=user_id, 
            description=description,
            due_date=due_date,
            status="pending",  # Always default to pending
            **kwargs
        )