from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from flask_migrate import Migrate





class CRUDMixin(Model):
    """ Allow convinience methods for CRUD (create, read, update, delete) """
 
    @classmethod
    def create(cls, **kwargs):

        instance = cls(**kwargs)
        return instance.save()
    

    def update(self, commit = True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self
    

    def save(self, commit= True):

        db.session.add(self)
        if commit :
            db.session.commit()
        return self
    

    def delete(self, commit = True):
        db.session.delete(self)
        return commit and db.session.commit()
    




db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()

    

