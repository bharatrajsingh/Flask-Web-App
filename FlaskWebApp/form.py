from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,AnyOf


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role',validators=[DataRequired(),AnyOf(message='Sorry, You can enter only if you are a student or tecaher',
                         values=['student', 'teacher', 'Student','Teacher'])])
    submit = SubmitField('SignUp')


class Student_fillForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    roll_no = StringField('Roll_no',validators=[DataRequired()])
    branch = StringField('Branch',validators=[DataRequired()])
    submit = SubmitField('Submit')


class Teacher_fillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    teaching_sub = StringField('Teaching_sub', validators=[DataRequired()])
    submit = SubmitField('Submit')

# class FacultyLoginForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')