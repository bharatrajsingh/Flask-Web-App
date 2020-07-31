from datetime import datetime
from flaskblog import db, app,login_manager
from flask_login import UserMixin
from functools import wraps
from flask_login import login_user, current_user
from flask import flash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


association_table = db.Table('association', db.metadata,
                    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id')),
                    db.Column('staff_id', db.Integer, db.ForeignKey('teacher.staff_id'))
)



class User(UserMixin, db.Model):
    # _tablename_ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    pwd_hash = db.Column(db.String(200))
    email = db.Column(db.String(256),unique=True)
    is_active = db.Column(db.Boolean,default=False)
    role = db.Column(db.String(20),unique=False)

    def __init__(self, pwd_hash,email,is_active,role):
        self.pwd_hash=pwd_hash
        self.email=email
        self.is_active = is_active
        self.role=role

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_authenticated


class Student(db.Model):
    # __tablename__ = "students"
    student_id = db.Column(db.Integer, unique=True, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),unique=True)
    name = db.Column(db.String(80),unique=False)
    email = db.Column(db.String(255))
    roll_no = db.Column(db.Integer,unique=False)
    branch = db.Column(db.String(50),unique=False)
    subjects = db.relationship("Teacher",
                                secondary=association_table,backref="students")
    def __repr__(self):
        return "<Student ID: {}>".format(self.student_id)


class Teacher(db.Model):
    # __tablename__ = "teachers"
    staff_id = db.Column(db.Integer, unique=True, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),unique=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(255))
    teaching_sub = db.Column(db.String(255),unique=False)

    def __repr__(self):
        return "<Staff ID: {}>".format(self.staff_id)


class Attendance(db.Model):
    staff_id = db.Column(db.Integer, unique=True, primary_key=True,autoincrement=True)
    total_lec = db.Column(db.Integer)
    stu_attnd = db.Column(db.String(255)) # {'date':
                  #                                 {'student_id':0/1}
                   #                          }


class attended_lects(db.Model):
    student_id = db.Column(db.Integer, unique=True, primary_key=True,autoincrement=True)
    data = db.Column(db.String) # {'staff_id': total_lectures attended }


