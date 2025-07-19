
from silver_app.extensions import db




Column = db.Column
Model = db.Model



class SurrogatePK():
    """ Mixin that add surrogate integer primary key column named id to any delcarative mapped class 
    
    declarative class means the decalaration declares both the table and class structure
    
    """

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key = True)

    @classmethod
    def get_by_id(cls, record_id):

        if any(
                (isinstance(record_id, str) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
                
                )


        ):
            return cls.query.get(int(record_id))

def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
