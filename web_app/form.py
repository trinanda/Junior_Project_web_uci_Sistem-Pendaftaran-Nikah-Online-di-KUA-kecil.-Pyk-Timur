from wtforms import TextAreaField, IntegerField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired, Required
from flask_wtf import FlaskForm


class RegisterFormView(FlaskForm):
    name = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Nama Anda"})
    email = StringField('', validators=[InputRequired(),
                        Email(message='Invalid email'), Length(max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField('', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})


class LoginFormView(FlaskForm):
    email = StringField('', validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField('', validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"})
    remember = BooleanField('')