from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from businessnews.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min = 6)])
    conform_password = PasswordField('Conform password',validators=[DataRequired(),Length(min = 6), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already exist.. Please choose another one')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exist.. Please choose another one')

class LoginForm(FlaskForm):
    # username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(min = 6)])
    # confirm_password = PasswordFied('password',validators=['Conform Password', DataRequired(),Length(min = 6)], EqualTo('password'))
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
class SearchForm(FlaskForm):
    business = BooleanField('Business')
    entertainment = BooleanField('Entertainment')
    health = BooleanField('Health')
    science = BooleanField('Science')
    sports = BooleanField('Sports')
    technology = BooleanField('Technology')
    # start_date = DateField('Search news from this date (Eg : 2016-11-26)',format='%Y-%m-%d')
    # end_date = DateField('End Date',format='%Y-%m-%d')
    keyword = StringField('Type keyword',validators=[DataRequired(),Length(min=3)])
    submit = SubmitField('Search')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already exist.. Please choose another one')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email already exist.. Please choose another one')
