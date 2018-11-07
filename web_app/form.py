from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, SelectField, DateTimeField
from wtforms.validators import InputRequired, Email, Length, DataRequired, Required
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField


class RegisterFormView(FlaskForm):
    name = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Nama Anda"})
    email = StringField('', validators=[InputRequired(),
                        Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField('', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})


class LoginFormView(FlaskForm):
    email = StringField('', validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField('', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})
    remember = BooleanField('')



class SocietyInputDataView(FlaskForm):
    NIK_catin_laki_laki = IntegerField('', validators=[DataRequired()],
                                       render_kw={'placeholder': 'NIK Catin Laki-laki'})
    nama_catin_laki_laki = StringField('', validators=[DataRequired()],
                                       render_kw={"placeholder": "Nama Catin Laki-laki"})
    NIK_catin_perempuan = IntegerField('', validators=[DataRequired()],
                                       render_kw={'placeholder': 'NIK Catin Perempuan'})
    nama_catin_perempuan = StringField('', validators=[DataRequired()],
                                       render_kw={"placeholder": "Nama Catin Perempuan"})
    jadwal_nikah = DateField('Jadwal Nikah', format='%Y-%m-%d', validators=[DataRequired()])
    tempat_pelaksaan_nikah = StringField('', validators=[DataRequired()],
                                         render_kw={"placeholder": "Tempat Pelaksanaan Nikah"})



class OperatorAddDataView(FlaskForm):
    NIK_catin_laki_laki = IntegerField('', validators=[DataRequired()], render_kw={'placeholder': 'NIK Catin Laki-laki'})
    nama_catin_laki_laki = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Nama Catin Laki-laki"})
    NIK_catin_perempuan = IntegerField('', validators=[DataRequired()], render_kw={'placeholder': 'NIK Catin Perempuan'})
    nama_catin_perempuan = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Nama Catin Perempuan"})
    jadwal_nikah = DateField('Jadwal Nikah', format='%Y-%m-%d', validators=[DataRequired()])
    tempat_pelaksaan_nikah = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Tempat Pelaksanaan Nikah"})