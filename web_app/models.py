from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, VARCHAR, Enum, Boolean, Date, Time
from flask_security import RoleMixin, UserMixin
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


# User
    # Admin
    # Operator
    # Masyarakat

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    roles = relationship('Role', secondary=roles_users,
                         backref=backref('users', lazy='dynamic'))

    def __init__(self, email='', password='', active=False):
        self.email = email
        self.password = password
        self.active = active


    def __str__(self):
        return self.email

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)


# content for index page
class Content(db.Model):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    post = Column(String)


# Data Catin
class dataCatin(db.Model):
    id = Column(Integer, primary_key=True)
    nikCatinLakiLaki = Column(Integer)
    catinLakiLakiName = Column(String(100))
    nikCatinPerempuan = Column(Integer)
    catinPerempuanName = Column(String(100))
    jadwalNikah = Column(DateTime)
    tempatPelaksanaanNikah = Column(String)

    user_id = Column(Integer, ForeignKey(User.id))

