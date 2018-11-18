import pytz
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import or_, not_, and_
from sqlalchemy.types import TypeDecorator, DateTime
from flask.ext.security import UserMixin, RoleMixin

db = SQLAlchemy()

PHOTO_LENGTH = 300
NORMAL_STRING_LENGTH = 190
LARGE_STRING_LENGTH = 2000


class UTCDateTime(TypeDecorator):
    impl = DateTime

    def proccess_bind_param(self, value, engine):
        if value is not None:
            if value.tzinfo:
                return value.astimezone(tz=pytz.utc).replace(tzinfo=None)
            else:
                return value

    def process_result_value(self, value, engine):
        #if value is not None:
        #    return value.replace(tzinfo=pytz.utc)
        return value


class Roles(object):
    USER = {
        'name': 'USER',
        'description': u'normal user'
    }

    ADMIN = {
        'name': 'ADMIN',
        'description': u'admin user'
    }

    SUPER_ADMIN = {
        'name': 'SUPER_ADMIN',
        'description': u'super user that can do anything'
    }


user_role = db.Table('user_role',
    db.Column('user_id', db.Integer(),
        db.ForeignKey('user.id', ondelete="CASCADE")),
    db.Column('role_id', db.Integer(),
        db.ForeignKey('role.id', ondelete="CASCADE")))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(NORMAL_STRING_LENGTH), unique=True)
    description = db.Column(db.Unicode(NORMAL_STRING_LENGTH))


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(NORMAL_STRING_LENGTH))
    name = db.Column(db.Unicode(NORMAL_STRING_LENGTH))
    phone = db.Column(db.String(NORMAL_STRING_LENGTH), unique=True)
    email = db.Column(db.String(NORMAL_STRING_LENGTH))
    last_login_at = db.Column(UTCDateTime())
    nickname = db.Column(db.Unicode(NORMAL_STRING_LENGTH))
    sex = db.Column(db.Enum('MALE', 'FEMALE'))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=user_role)
    role = db.relationship('Role', secondary=user_role, uselist=False)
    device_uid = db.Column(db.String(NORMAL_STRING_LENGTH))


