from marshmallow import Schema, fields, pre_load, post_dump





""" username = Column(db.String(80), unique=True, nullable=False)
email = Column(db.String(100), unique=True, nullable=False)
password = Column(db.LargeBinary(128), nullable = True)
created_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc))
updated_at = Column(db.DateTime, nullable = False, default=lambda: dt.datetime.now(dt.timezone.utc)) """
class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')


    user = fields.Nested('self', exclude=('user',), default=True, load_only=True)


    @pre_load
    def make_user(self, data, **kwargs):
        data = data["user"]
        if not data.get('email', True):
            del data['email']
        return data


    @post_dump
    def dump_user(self, data, **kwargs):
        return {'user': data}

    class Meta:
        strict = True


user_schema = UserSchema()
user_schemas = UserSchema(many=True)