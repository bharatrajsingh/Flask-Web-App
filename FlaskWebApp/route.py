from flaskblog.form import LoginForm,RegistrationForm,Student_fillForm,Teacher_fillForm
from flask_bcrypt import Bcrypt
from flask import Blueprint,render_template, url_for, flash, redirect, request
from flaskblog import app
from flaskblog import db
# from flaskblog.model import login_required

bcrypt = Bcrypt(app)
from flask_login import logout_user
from flaskblog.model import User,Student,Teacher,Attendance,attended_lects
from flask_login import login_user, current_user,login_required
site_blueprint = Blueprint('/',__name__,template_folder='templates')


@site_blueprint.route("/")
@site_blueprint.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('/.student_home')) if current_user.role=='student' \
                                                   else redirect(url_for('/.teacher_home'))
    return render_template('home.html')

@site_blueprint.route("/view_attendance",methods=["GET"])
def view_attendance():
    student = Student.query.filter_by(user_id=current_user.id).first()
    teachers = list(student.subjects)
    cond_lect = list()
    attnd_lect = list()
    t1 = list()
    ats = attended_lects.query.filter_by(student_id=student.student_id).first()
    for i in teachers:
        s = Attendance.query.filter_by(staff_id=i.staff_id).first()
        if s:
            t1.append(i)
            cond_lect.append(s.total_lec)
            if not ats:
                attnd_lect.append(0)
            elif (ats and i.staff_id not in eval(ats.data)):
                attnd_lect.append(0)
            else:
                f = eval(ats.data)
                attnd_lect.append(f[i.staff_id])
        else:
            t1.append(i)
            cond_lect.append(0)
            attnd_lect.append(0)
    all = list()
    all.append(t1)
    # print(len(t1))
    all.append(cond_lect)
    all.append(attnd_lect)
    return render_template('view_attendance.html', title='Student_home', Student=student, all=all, length=len(all[0]))


@site_blueprint.route("/student_home",methods=["GET", "POST"])
def student_home():
    student= Student.query.filter_by(user_id=current_user.id).first()
    teacher=student.subjects
    return render_template('student_home.html', title='Student_home',Student=student,Teacher=teacher)


@site_blueprint.route("/teacher_home",methods=["GET", "POST"])
def teacher_home():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    return render_template('teacher_home.html', title='Teacher_home',Teacher=teacher)

# @site_blueprint.route("/faculty _home")
# def faculty_home():
#     return render_template('about.html', title='About')

@site_blueprint.route("/about")
def about():
    return render_template('about.html', title='About')

@site_blueprint.route("/contact")
def contact():
    return render_template('contact.html',title='Contact')


# @site_blueprint.route("/")
# @app.route("/home")
@site_blueprint.route("/login",methods=["GET", "POST"])
def Login():
    if current_user.is_authenticated:
        if current_user.role.lower() == 'student':
            return redirect(url_for('/.student_home'))
        elif current_user.role.lower() == 'teacher' :
            return redirect(url_for('/.teacher_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.role.lower()==form.role.data.lower() and form.password.data == user.pwd_hash:
            login_user(user)
            # print(current_user.id)
            if user.role.lower() == 'student':
                return redirect(url_for('/.student_home'))
            elif user.role.lower() == 'teacher':
                return redirect(url_for('/.teacher_home'))
        else:
            flash('Login Unsuccessful. Please check email , password and Role', 'danger')
            return redirect(url_for('/.Login'))
    else:
        # flash('Credentials should be in proper format', 'danger')
        return render_template('login.html', title='Login', form=form)


@site_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        if current_user.role == 'student' :
            return redirect(url_for('/.student_home'))
        elif current_user.role == 'teacher':
            return redirect(url_for('/.teacher_home'))
    if request.method=="POST":
        if form.validate_on_submit():
            user = User(email=form.email.data, pwd_hash=form.password.data,role=form.role.data.lower(),is_active=True)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Your account has been created! You are now logged in', 'success')
            return redirect(url_for('/.fill_student')) if user.role=='student' \
                                                    else redirect(url_for('/.fill_teacher'))
        flash('SignUp Unsuccessful. Please check Role [Student,Teacher]', 'danger')
    return render_template('registration.html', title='Register', form=form)


@site_blueprint.route("/fill_student", methods=['GET', 'POST'])
@login_required
def fill_student():
    form = Student_fillForm()
    if form.validate_on_submit():
        student = Student(user_id=current_user.id,email=form.email.data, name=form.name.data,roll_no=form.roll_no.data,
                          branch=form.branch.data)
        db.session.add(student)
        db.session.commit()
        # flash('Your details has been saved successfully', 'success')
        return redirect(url_for('/.student_home'))
    return render_template('student_fill.html', title='Register', form=form,user1=current_user)


@site_blueprint.route("/fill_teacher", methods=['GET', 'POST'])
@login_required
def fill_teacher():
    form = Teacher_fillForm()
    if form.validate_on_submit():
        teacher = Teacher(user_id=current_user.id,email=form.email.data, name=form.name.data,
                          teaching_sub=form.teaching_sub.data)
        db.session.add(teacher)
        db.session.commit()
        # flash('Your details has been saved successfully', 'success')
        return redirect(url_for('/.teacher_home'))
    return render_template('teacher_fill.html',title='Register',form=form,user1=current_user)


@site_blueprint.route("/student/update", methods=['GET', 'POST'])
@login_required
def update_student():
    student = Student.query.filter_by(user_id=current_user.id).first()
    form = Student_fillForm()
    if form.validate_on_submit():
        # user_id=current_user.id
        student.email=form.email.data
        student.name=form.name.data
        student.roll_no=form.roll_no.data
        student.branch=form.branch.data
        db.session.commit()
        flash('Your details has been updated!', 'success')
        return redirect(url_for('/.student_home'))
    return render_template('update_student.html', title='Update Student',
                           form=form, legend='Update Student')

# @site_blueprint.route("/teacher/update", methods=['GET', 'POST'])
# @login_required
# def update_teacher():
#     teacher = Teacher.query.get_or_404(current_user.id)
#     form = Teacher_fillForm()
#     if form.validate_on_submit():
#         teacher.email=form.email.data
#         teacher.name=form.name.data
#         teacher.teaching_sub=form.teaching_sub
#         db.session.commit()
#         flash('Your details has been updated!', 'success')
#         return redirect(url_for('/.teacher_home'))
#     return render_template('update_teacher.html', title='Update Teacher',
#                            form=form, legend='Update Teacher')


@site_blueprint.route("/subjects/add", methods=['GET', 'POST'])
def add_subjects():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if request.method=="POST":
        subj_to_add = request.form.getlist('subject')
        for i in subj_to_add:
            teacher=Teacher.query.filter_by(staff_id=i).first()
            student.subjects.append(teacher)
            db.session.commit()
        return redirect(url_for('/.student_home'))
    existed_sub=student.subjects
    teachers=Teacher.query.all()
    teachers= [item for item in teachers if item not in existed_sub]
    return render_template('add_subjects.html', title='Add Subjects',
                        legend='Add Subjects',Teachers=teachers)


@site_blueprint.route("/take_attendance", methods=['GET', 'POST'])
def take_attendance():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    students_ids=teacher.students
    if request.method=="POST":
        stu_to_mark = request.form.getlist('check-box')
        print(stu_to_mark)
        print(students_ids[0].student_id)
        # print()
        date  = request.form['date']
        print(date)
        attendance = Attendance.query.filter_by(staff_id=teacher.staff_id).first()
        print(attendance)
        if not attendance:
            s=dict()
            for i in students_ids:
                if not s:
                    s.update({date:{i.student_id:int(str(i.student_id) in stu_to_mark)}})
                else:
                    s[date].update({i.student_id:int(str(i.student_id) in stu_to_mark)})
                print(s)
            print(str(s))
            at1=Attendance(staff_id=teacher.staff_id, total_lec=1,
                                     stu_attnd=str(s))
            db.session.add(at1)
            db.session.commit()
            for i in students_ids:
                    print(i)
                    attnd_lect = attended_lects.query.filter_by(student_id=i.student_id).first()
                    if not attnd_lect:
                        at2 = attended_lects(student_id=i.student_id,data=str({teacher.staff_id:int(str(i.student_id) in stu_to_mark)}))
                        db.session.add(at2)
                        db.session.commit()
                    else:
                        f = eval(attnd_lect.data)
                        f[teacher.staff_id]=int(str(i.student_id) in stu_to_mark)
                        attnd_lect.data = str(f)
                        db.session.commit()
        else:
            stu = eval(attendance.stu_attnd)
            print(stu)
            # print(date in stu)
            if date not in stu:
                attendance.total_lec = attendance.total_lec + 1
                for i in students_ids:
                    print(i.student_id)
                    print(stu_to_mark)
                    if date not in stu:
                        stu.update({date:{i.student_id:int(str(i.student_id) in stu_to_mark)}})
                    else:
                        stu[date].update({i.student_id:int(str(i.student_id) in stu_to_mark)})
                    attendance.stu_attnd=str(stu)
                    db.session.commit()
                for i in students_ids:
                    attnd_lect = attended_lects.query.filter_by(student_id=i.student_id).first()
                    if not attnd_lect:
                        at3 = attended_lects(student_id=i.student_id, data=str({teacher.staff_id: int(str(i.student_id) in stu_to_mark)}))
                        db.session.add(at3)
                        db.session.commit()
                    else:
                        d = eval(attnd_lect.data)
                        if teacher.staff_id in d:
                            d[teacher.staff_id] = d[teacher.staff_id] + int(str(i.student_id) in stu_to_mark)
                            attnd_lect.data = str(d)
                            db.session.commit()
                        else:
                            d[teacher.staff_id]=int(str(i.student_id) in stu_to_mark)
                            attnd_lect.data = str(d)
                            db.session.commit()
            else:
                e=stu[date]
                print(e)
                for i in students_ids:
                    attnd_lect = attended_lects.query.filter_by(student_id=i.student_id).first()
                    if i.student_id in e:
                        y = eval(attnd_lect.data)
                        if e[i.student_id]!= int(str(i.student_id) in stu_to_mark):
                            if e[i.student_id]==1 and int(str(i.student_id) in stu_to_mark) == 0:
                                e[i.student_id]=0
                                y[teacher.staff_id]=y[teacher.staff_id]-1
                                attnd_lect.data = str(y)
                                print(e)
                                stu[date]=e
                                attendance.stu_attnd = str(stu)
                                db.session.commit()
                            elif e[i.student_id]==0 and int(str(i.student_id) in stu_to_mark) == 1:
                                e[i.student_id] = 1
                                y[teacher.staff_id] = y[teacher.staff_id] + 1
                                attnd_lect.data = str(y)
                                stu[date] = e
                                attendance.stu_attnd = str(stu)
                                db.session.commit()
                    else:
                        stu[date].update({i.student_id:int(str(i.student_id) in stu_to_mark)})
                        if not attnd_lect:
                            at4 = attended_lects(student_id=i.student_id, data=str({teacher.staff_id: int(str(i.student_id) in stu_to_mark)}))
                            print(stu)
                            attendance.stu_attnd = str(stu)
                            db.session.add(at4)
                            db.session.commit()
                        else:
                            z = eval(attnd_lect.data)
                            z[teacher.staff_id]=int(str(i.student_id) in stu_to_mark)
                            attnd_lect.data = str(z)
                            attendance.stu_attnd = str(stu)
                            db.session.commit()
        return redirect(url_for('/.teacher_home'))
    print("GET")
    return render_template('take_attendance.html', title='Take Attendance',
                                                  legend='Take Attendance',students=students_ids)


@site_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('/.home'))
