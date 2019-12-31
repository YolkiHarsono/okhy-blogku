from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog_ku.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class Admin_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('submit')
    
class Login_F(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Registrasi_F(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    konfirmasi_password = PasswordField('Konfirmasi_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')

class Update_Account_F(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto = FileField('Update Foto Profil', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')

class Post_F(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    konten = TextAreaField('konten', validators=[DataRequired()])
    submit = SubmitField('POST')
