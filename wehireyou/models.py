from wehireyou import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))

class Login(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)

    username = db.Column(db.String(50))
    orgcode = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(200))
    usertype = db.Column(db.String(20))
    pid = db.Column(db.String(20))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Login.query.get(user_id)

    def __repr__(self):
        return f"Login('{self.username}', '{self.password}','{self.usertype}','{self.email}', '{self.image_file}')"


class Provider(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    orgcode = db.Column(db.String(250))
    fname = db.Column(db.String(250),nullable=False)
    address = db.Column(db.String(520),nullable=False)
    pin = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String,nullable=False)
    phone = db.Column(db.String(220),nullable=False)
    mobile = db.Column(db.String(220),nullable=False)
    email = db.Column(db.String(520),nullable=False)
    password = db.Column(db.String(220),nullable=False)
    status = db.Column(db.String(220))


class Seeker(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    orgcode = db.Column(db.String)
    fname = db.Column(db.String(250),nullable=False)
    lname = db.Column(db.String(250),nullable=False)
    address = db.Column(db.String(520),nullable=False)
    country = db.Column(db.String(520),nullable=False)
    state = db.Column(db.String(520),nullable=False)
    city = db.Column(db.String(520),nullable=False)
    category = db.Column(db.String(520),nullable=False)
    qulification = db.Column(db.String(520),nullable=False)
    salarypackage = db.Column(db.Integer,nullable=False)
    pin = db.Column(db.Integer,nullable=False)
    locationp = db.Column(db.String,nullable=False)
    phone = db.Column(db.String(220),nullable=False)
    mobile = db.Column(db.String(220),nullable=False)
    email = db.Column(db.String(520),nullable=False)
    password = db.Column(db.String(220),nullable=False)
    verify = db.Column(db.String(220),nullable=False)
    status = db.Column(db.String(220))


class Contact(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(250))
    name = db.Column(db.String(202))
    message = db.Column(db.String(220))

class Feedback(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(520))
    name = db.Column(db.String(222))
    message = db.Column(db.String(220))


class Placement(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    # orgcode = db.Column(db.String)
    collegename = db.Column(db.String(520))
    university = db.Column(db.String(520))
    ptype = db.Column(db.String(520))
    pname= db.Column(db.String(520))
    email = db.Column(db.String(520))
    password = db.Column(db.String(222))
    contact = db.Column(db.String(220))
    status= db.Column(db.String(220))


class Jobs(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    # orgcode = db.Column(db.String)
    title = db.Column(db.String(1520))
    company_name = db.Column(db.String(520))
    location = db.Column(db.String(520))
    pay= db.Column(db.String(520))
    summary_bullets = db.Column(db.String(520))
    post = db.Column(db.String(222))
    status = db.Column(db.Boolean, nullable=False)
    created_date= db.Column(db.String(15), nullable=False)


class Resume(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    email = db.Column(db.String(80))
    web = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    comments = db.Column(db.String(80))
    field = db.Column(db.String(80))
    degree = db.Column(db.String(80))
    school = db.Column(db.String(80))
    fromedu = db.Column(db.String(80))
    toedu = db.Column(db.String(80))
    title = db.Column(db.String(80))
    company = db.Column(db.String(80))
    fromexp = db.Column(db.String(80))
    toexp = db.Column(db.String(80))
    description = db.Column(db.String(80))
    skill = db.Column(db.String(80))
    proficiency = db.Column(db.String(80))
    hobbies = db.Column(db.String(80))
    userid = db.Column(db.String(80))

class Postjob(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    tjob = db.Column(db.String(1520))
    qualification = db.Column(db.String(520))
    experiences = db.Column(db.String(520))
    salary= db.Column(db.String(520))
    description = db.Column(db.String(520))
    location = db.Column(db.String(222))
    postdate= db.Column(db.String(222))

class Postintership(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    internship = db.Column(db.String(1520))
    duration = db.Column(db.String(520))
    organisation = db.Column(db.String(520))
    interntype = db.Column(db.String(520))
    topic = db.Column(db.String(520))
    syllabus = db.Column(db.String(222))
    fee = db.Column(db.String(222))
    postdate= db.Column(db.String(222))



class Student(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    # orgcode = db.Column(db.String)
    sname = db.Column(db.String(520))
    collegename = db.Column(db.String(520))
    university = db.Column(db.String(520))
    course = db.Column(db.String(520))
    email= db.Column(db.String(520))
    password = db.Column(db.String(222))
    pid = db.Column(db.String(220))
    status= db.Column(db.String(220))
    verify= db.Column(db.String(220))



class Postdrive(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    drive = db.Column(db.String(1520))
    testdate = db.Column(db.String(520))
    testlocation = db.Column(db.String(520))
    regenddate = db.Column(db.String(520))
    qualification = db.Column(db.String(520))
    postdate = db.Column(db.String(222))
   

class Jobapply(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    email = db.Column(db.String(80))
    address = db.Column(db.String(80))
    verify = db.Column(db.String(80))
    tjob = db.Column(db.String(100))
    postdate = db.Column(db.String(100))

class Internapply(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    sname = db.Column(db.String(80))
    cname = db.Column(db.String(80))
    course = db.Column(db.String(80))
    email = db.Column(db.String(80))
    verify = db.Column(db.String(80))
    internship = db.Column(db.String(100))
    organisation = db.Column(db.String(100))
    postdate = db.Column(db.String(100))

class Driveapply(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    sname = db.Column(db.String(80))
    cname = db.Column(db.String(80))
    course = db.Column(db.String(80))
    email = db.Column(db.String(80))
    verify = db.Column(db.String(80))
    drive = db.Column(db.String(100))
    postdate = db.Column(db.String(100))
    
if __name__ == "__main__":     
    app.run(debug=True)