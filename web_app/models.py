from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, VARCHAR, Enum, Boolean, Date, Time, DECIMAL
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

    def __repr__(self):
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



    def __init__(self, name='', email='', password='', active=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active


    def __str__(self):
        return self.email

    def __repr__(self):
        return self.roles

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
class DataCatin(db.Model):
    id = Column(Integer, primary_key=True)
    NIK_catin_laki_laki = Column(DECIMAL, unique=True)
    nama_catin_laki_laki = Column(String(100))
    NIK_catin_perempuan = Column(DECIMAL, unique=True)
    nama_catin_perempuan = Column(String(100))
    tanggal_daftar = Column(Date)
    jadwal_nikah = Column(Date)
    jam = Column(Time)
    tempat_pelaksaan_nikah = Column(String)

    user_id = Column(Integer, ForeignKey(User.id))

    is_public = Column(Boolean(), nullable=False)

    ON_PROCESS = 'Sedang di proses'
    ACCEPTED = 'Diterima'

    status_pendaftaran = Column(Enum(ON_PROCESS, ACCEPTED, name='status_pendaftaran', default=ON_PROCESS))


    def __init__(self, NIK_catin_laki_laki='', nama_catin_laki_laki='', NIK_catin_perempuan='',
                 nama_catin_perempuan='', tanggal_daftar='', jadwal_nikah='', jam='', tempat_pelaksaan_nikah='', user_id='', is_public=False,
                 status_pendaftaran=ON_PROCESS):
        self.NIK_catin_laki_laki = NIK_catin_laki_laki
        self.nama_catin_laki_laki = nama_catin_laki_laki
        self.NIK_catin_perempuan = NIK_catin_perempuan
        self.nama_catin_perempuan = nama_catin_perempuan
        self.tanggal_daftar = tanggal_daftar
        self.jadwal_nikah = jadwal_nikah
        self.jam = jam
        self.tempat_pelaksaan_nikah = tempat_pelaksaan_nikah
        self.user_id = user_id
        self.is_public = is_public
        self.status_pendaftaran = status_pendaftaran

