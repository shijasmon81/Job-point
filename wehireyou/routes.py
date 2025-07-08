from flask import Flask,render_template,flash,redirect,request,send_from_directory,make_response,url_for
from wehireyou import db,app,mail 
from wehireyou.models import *
from wehireyou.forms import *
from flask import Markup
import os
from flask_login import login_user, current_user, logout_user, login_required
# from flask_user import roles_required
from random import randint
from PIL import Image
import smtplib
from flask_mail import Mail, Message
from flask import Markup
import pdfkit

from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
from datetime import date



@app.route('/about')
def about():
    return render_template("about.html")

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route('/student_index')
def student_index():
    return render_template("student_index.html")



@app.route('/provider_index')
def provider_index():
    return render_template("provider_index.html")


@app.route('/place_index')
def place_index():
    return render_template("place_index.html")

@app.route('/jobseeker_index')
def jobseeker_index():
    return render_template("jobseeker_index.html")



@app.route('/playout')
def playout():
    return render_template("playout.html")


@app.route('/student_login',methods=["GET","POST"])
def student_login():
    if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         pid=request.form['pid']
         student = Login.query.filter_by(username=username,pid=pid, password=password,usertype= 'student').first()
         if student:
             login_user(student)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/student_index') 
    return render_template("student_login.html")


@app.route('/admin_login',methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         admin = Login.query.filter_by(username=username, password=password,usertype= 'admin').first()
         if admin:
             login_user(admin)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/aindex') 
    return render_template("admin_login.html", alert="Invalid Username or Password")


@app.route('/jobseeker_login',methods=["GET","POST"])
def jobseeker_login():
    if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         seeker = Login.query.filter_by(username=username, password=password,usertype= 'jobseeker').first()
         if seeker:
             login_user(seeker)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/jobseeker_index')
    return render_template("jobseeker_login.html")


@app.route('/provider_login',methods=["GET","POST"])
def provider_login():
    if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         provider = Login.query.filter_by(username=username, password=password,usertype='jobprovider').first()
         if provider:
             login_user(provider)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/provider_index')
    return render_template("provider_login.html")




@app.route('/place_login',methods=["GET","POST"])
def place_login():
    if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         place = Login.query.filter_by(username=username, password=password,usertype= 'placement').first()
         if place:
             login_user(place)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/place_index')
    return render_template("place_login.html")



@app.route('/gallery')
def gallery():
    return render_template("gallery.html")






@app.route('/')
def index():
    return render_template("index.html")


@app.route('/service')
def service():
    return render_template("service.html")




@app.route('/typography')
def typography():
    return render_template("typography.html")


@app.route('/place',methods=['POST','GET'])
def place():
    if request.method=="POST":
        # orgcode=request.form['orgcode']
        collegename=request.form['cname']
        university=request.form['university']
        ptype=request.form['ptype']
        email=request.form['email']
        password=request.form['password']
        contact=request.form['mobile']
        pname=request.form['pname']
        status="null"
        co=Placement(pname=pname,university=university,ptype=ptype,email=email,password=password,contact=contact,collegename=collegename,status=status)
        log=Login(username=email,password=password,usertype="placement")
        db.session.add(co)
        db.session.add(log)
        db.session.commit()
        return redirect('/place')

    return render_template("place.html")





@app.route('/contact',methods=['POST','GET'])
def contact():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
        co=Contact(name=name,email=email,message=message)
        db.session.add(co)
        db.session.commit()

    return render_template("contact.html")


@app.route('/acontact')
def acontact():
    a=Contact.query.all()
    return render_template("acontact.html",a=a)





@app.route('/pro',methods=['POST','GET'])
def pro():
   
    if request.method=="POST":
        name = request.form['name']
        address = request.form['address']
        location = request.form['location']
        pin = request.form['pin']
        phone = request.form['phone']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        status = "null"

        orgcode =  "null"

        register = Provider(fname=name, address=address, location=location,pin=pin,mobile=mobile,phone=phone,
                        email=email,password=password,status=status,orgcode=orgcode)
        log=Login(username=email,password=password,usertype="jobprovider")
      
        db.session.add(register)
        db.session.add(log)
        db.session.commit()
        message=Markup('''You registration will be confirmed soon thank you!''')
        return redirect('/pro')
        
    return render_template('pro.html')











@app.route('/seeker',methods=['POST','GET'])
def seeker():
    message=""
    if request.method=="POST":
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        category = request.form['category']
        qulification = request.form['qulification']
        salarypackage = request.form['salarypackage']
        pin = request.form['pin']
        location = request.form['locatipnp']
        phone = request.form['phone']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        status = "null"
        verify = "null"
        orgcode = request.form['orgcode']

        register = Seeker(fname=fname,lname=lname, address=address,country=country,state=state,city=city,category=category,qulification=qulification,
        
        salarypackage=salarypackage,locationp=location,pin=pin,mobile=mobile,phone=phone,
                        email=email,password=password,status=status,orgcode=orgcode,verify=verify)
        log=Login(username=email,password=password,usertype="jobseeker")
        try:
            db.session.add(register)
            db.session.add(log)
            db.session.commit()
            message=Markup('''You registration will be confirmed soon thank you!''')
            flash(message)
            return redirect('/seeker')
        except Exception as e:
            print(e)
    return render_template('seeker.html')

















@app.route('/alyout')
def alyout():
    return render_template("alyout.html")



@app.route('/aindex')
def aindex():
    return render_template("aindex.html")




@app.route('/aprovide')
def aprovide():
    mat=Provider.query.all()
    return render_template("aprovide.html",mat=mat)


@app.route('/view_cells')
def view_cells():
    mat=Placement.query.all()
    return render_template("view_cells.html",mat=mat)



@app.route('/a_prov_app/<int:id>',methods=['GET','POST'])
def a_prov_app(id):
     users = Provider.query.get_or_404(id)
     if request.method == 'POST':
          users.orgcode=request.form['orgcode']
          users.status=request.form['status']
          print(users.status)
          password=users.password
        #   hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
          db.session.commit()
          if users.status == "Approved":
               log = Login(username=users.fname,usertype="jobprovider",email=users.email,
               password=password,orgcode=users.orgcode)
               def sendmail():
                    msg = Message('Approved',recipients=[users.email])
                    msg.html = ('''<h2>You are Account has been approved !</h2><br>
                                        <h3>Login at Your Order 'http://127.0.0.1:5000/login'</h3><br>
                                        <h2>Your Username</h2><br>'''+users.email+ '''<br><h2>and Password is :</h2><br>'''+users.password)
                    mail.send(msg)
                    print("inside sendmail")
               sendmail()
               try:
                    db.session.add(log)
                    print(log)
                    db.session.commit()
                    return redirect('/a_prov_app')
               except Exception as e:
                    print(e)
          else:
               message=Markup(''' Application Rejected''')
               flash(message)
               return redirect('/a_prov_app')
     return render_template('a_prov_app.html',user=users)














@app.route('/aseek')
def aseek():
    a=Seeker.query.all()
    return render_template("aseek.html",a=a)




@app.route('/aaseekapp/<int:id>',methods=['GET','POST'])
def aaseekapp(id):
     users = Seeker.query.get_or_404(id)
     if request.method == 'POST':
          users.orgcode=request.form['orgcode']
          users.status=request.form['status']
          print(users.status)
          password=users.password
        #   hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
          db.session.commit()
          if users.status == "Approved":
               log = Login(username=users.fname,usertype="seeker",email=users.email,
               password=password,orgcode=users.orgcode)
               def sendmail():
                    msg = Message('Approved',recipients=[users.email])
                    msg.html = ('''<h2>You are Account has been approved !</h2><br>
                                        <h3>Login at Your Order 'http://127.0.0.1:5000/login'</h3><br>
                                        <h2>Your Username</h2><br>'''+users.email+ '''<br><h2>and Password is :</h2><br>'''+users.password)
                    mail.send(msg)
                    print("inside sendmail")
               sendmail()
               try:
                    db.session.add(log)
                    print(log)
                    db.session.commit()
                    return redirect('/aaseekapp')
               except Exception as e:
                    print(e)
          else:
               message=Markup(''' Application Rejected''')
               flash(message)
               return redirect('/aaseekapp')
     return render_template('aaseekapp.html',user=users)


@app.route('/aplaceapp/<int:id>',methods=['GET','POST'])
def aplaceapp(id):
     users = Placement.query.get_or_404(id)
     if request.method == 'POST':
          users.orgcode=request.form['orgcode']
          users.status=request.form['status']
          print(users.status)
          password=users.password
        #   hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
          db.session.commit()
          if users.status == "Approved":
               log = Login(username=users.pname,usertype="placement",email=users.email,
               password=password,orgcode=users.orgcode)
               def sendmail():
                    msg = Message('Approved',recipients=[users.email])
                    msg.html = ('''<h2>You are Account has been approved !</h2><br>
                                        <h3>Login at Your Order 'http://127.0.0.1:5000/login'</h3><br>
                                        <h2>Your Username</h2><br>'''+users.email+ '''<br><h2>and Password is :</h2><br>'''+users.password)
                    mail.send(msg)
                    print("inside sendmail")
               sendmail()
               try:
                    db.session.add(log)
                    print(log)
                    db.session.commit()
                    return redirect('/aplaceapp')
               except Exception as e:
                    print(e)
          else:
               message=Markup(''' Application Rejected''')
               flash(message)
               return redirect('/aplaceapp')
     return render_template('aplaceapp.html',user=users)


#################################################################################################
############################### Resume  #########################################################

@app.route('/resume')
def resume():

    return render_template("resume.html")

@app.route('/resume_enter',methods=['GET', 'POST'])
def resume_enter():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        web = request.form['web']
        phone = request.form['phone']
        comments = request.form['comments']
        field = request.form['field']
        degree = request.form['degree']
        school = request.form['school']
        fromedu = request.form['fromedu']
        toedu = request.form['toedu']
        title = request.form['title']
        company = request.form['company']
        fromexp = request.form['fromexp'] 
        toexp = request.form['toexp']
        description = request.form['description']
        skill = request.form['skill']
        proficiency = request.form['proficiency']
        hobbies = request.form['hobbies']

        my_data = Resume(name=name,address=address,web=web,phone=phone,comments=comments,field=field,degree=degree,school=school,fromedu=fromedu,toedu=toedu,title=title,company=company,fromexp=fromexp,toexp=toexp,description=description,skill=skill,proficiency=proficiency,hobbies=hobbies)
       
        db.session.add(my_data) 
        
        db.session.commit()
        
        return redirect('/cvdesign_one/'+str(my_data.id))
        
    else :
        return render_template("resume_enter.html")



@app.route('/resume_enter2',methods=['GET', 'POST'])
def resume_enter2():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        web = request.form['web']
        phone = request.form['phone']
        comments = request.form['comments']
        field = request.form['field']
        degree = request.form['degree']
        school = request.form['school']
        fromedu = request.form['fromedu']
        toedu = request.form['toedu']
        title = request.form['title']
        company = request.form['company']
        fromexp = request.form['fromexp']
        toexp = request.form['toexp']
        description = request.form['description']
        skill = request.form['skill']
        proficiency = request.form['proficiency']
        hobbies = request.form['hobbies']

        my_data = Resume(name=name,address=address,web=web,phone=phone,comments=comments,field=field,degree=degree,school=school,fromedu=fromedu,toedu=toedu,title=title,company=company,fromexp=fromexp,toexp=toexp,description=description,skill=skill,proficiency=proficiency,hobbies=hobbies)
       
        db.session.add(my_data) 
        
        db.session.commit()
        
        return redirect('/cvdesign_two/'+str(my_data.id))
        
    else :
        return render_template("resume_enter2.html")


@app.route('/resume_enter3',methods=['GET', 'POST'])
def resume_enter3():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        web = request.form['web']
        phone = request.form['phone']
        comments = request.form['comments']
        field = request.form['field']
        degree = request.form['degree']
        school = request.form['school']
        fromedu = request.form['fromedu']
        toedu = request.form['toedu']
        title = request.form['title']
        company = request.form['company']
        fromexp = request.form['fromexp']
        toexp = request.form['toexp']
        description = request.form['description']
        skill = request.form['skill']
        proficiency = request.form['proficiency']
        hobbies = request.form['hobbies']

        my_data = Resume(name=name,address=address,web=web,phone=phone,comments=comments,field=field,degree=degree,school=school,fromedu=fromedu,toedu=toedu,title=title,company=company,fromexp=fromexp,toexp=toexp,description=description,skill=skill,proficiency=proficiency,hobbies=hobbies)
       
        db.session.add(my_data) 
        
        db.session.commit()
        
        return redirect('/cvdesign_three/'+str(my_data.id))
        
    else :
        return render_template("resume_enter3.html")




@app.route('/cvdesign_three/<int:id>',methods=["GET","POST"])
def cvdesign_three(id):

    obj = Resume.query.get_or_404(id)
    return render_template("cvdesign_three.html",obj=obj)

@app.route('/cvdesign_two/<int:id>',methods=["GET","POST"])
def cvdesign_two(id):

    obj = Resume.query.get_or_404(id)
    return render_template("cvdesign_two.html",obj=obj)

@app.route('/cvdesign_one/<int:id>',methods=["GET","POST"])
def cvdesign_one(id):

    obj = Resume.query.get_or_404(id)
    return render_template("cvdesign_one.html",obj=obj)


###############################################################################################



#post job


@app.route('/postjob',methods=['GET', 'POST'])
def postjob():
    if request.method == 'POST':
        tjob = request.form['tjob']
        qualification = request.form['qualification']
        experiences = request.form['experiences']
        salary = request.form['salary']
        description = request.form['description']
        location = request.form['location']
        postdate = request.form['postdate']

        my_data = Postjob(tjob=tjob,qualification=qualification,experiences=experiences,salary=salary,description=description,location=location,postdate=postdate)
       
        db.session.add(my_data) 
        
        db.session.commit()
        d=Seeker.query.all()
        for i in d:
            send(i.email)
           
        flash("Registered successfully! Please Login..")
        return redirect('/provider_index') 
        
    else :
        return render_template("postjob.html")


def send(email):
    d=Seeker.query.all()
    
    for i in d:
     
         msg = Message('New Job Alert!!!!!!',
                  recipients=[i.email])
         msg.body = f''' We are Posted New jobs . Please verify through your account'''
         mail.send(msg) 

@app.route('/viewjob_seeker')
def viewjob_seeker():
    mat=Postjob.query.all()
    return render_template("viewjob_seeker.html",mat=mat)






@login_required
@app.route('/jobapply_seeker/<int:id>', methods=['GET', 'POST'])
def jobapply_seeker(id):
    obj = Postjob.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        verify = request.form['verify']
        my_data = Jobapply(name=name,phone=phone,email=email,address=address,verify=verify,tjob=obj.tjob,postdate=obj.postdate)
       
        db.session.add(my_data) 
        
        db.session.commit()
        return redirect('/viewjob_seeker')
    return render_template('jobapply_seeker.html',obj=obj)



@app.route('/viewapplied_pro')
def viewapplied_pro():
    mat=Jobapply.query.filter_by(verify='agree')
    return render_template("viewapplied_pro.html",mat=mat)


###########################################################################################
  
#internship

@app.route('/postinternship',methods=['GET', 'POST'])
def postinternship():
    if request.method == 'POST':
        internship = request.form['internship']
        duration = request.form['duration']
        organisation = request.form['organisation']
        interntype = request.form['interntype']
        topic = request.form['topic']
        syllabus = request.form['syllabus']
        fee = request.form['fee']
        postdate = request.form['postdate']
        my_data = Postintership(internship=internship,duration=duration,organisation=organisation,interntype=interntype,topic=topic,syllabus=syllabus,fee=fee,postdate=postdate)
       
        db.session.add(my_data) 
        
        db.session.commit()
        
        return redirect('/provider_index')
        
    else :
        return render_template("postinternship.html")


@app.route('/viewintern_stu')
def viewintern_stu():
    mat=Postintership.query.all()
    return render_template("viewintern_stu.html",mat=mat)


@app.route('/addstu_place',methods=['POST','GET'])
def addstu_place():
    if request.method=="POST":
        # orgcode=request.form['orgcode']
        sname=request.form['sname']
        collegename=request.form['cname']
        university=request.form['university']
        course=request.form['course']
        email=request.form['email']
        password=request.form['password']
        pid=request.form['pid']
        verify="null"
        status="null"
        co=Student(sname=sname,collegename=collegename,university=university,course=course,email=email,password=password,pid=pid,verify=verify,status=status)
        log=Login(username=email,password=password,pid=pid,usertype="student")
        db.session.add(co)
        db.session.add(log)
        db.session.commit()
        return redirect('/place')

    return render_template("addstu_place.html")



@login_required
@app.route('/internapply_stu/<int:id>', methods=['GET', 'POST'])
def internapply_stu(id):
    obj = Postintership.query.get_or_404(id)
    if request.method == 'POST':
        sname = request.form['sname']
        cname = request.form['cname']
        course = request.form['course']
        email = request.form['email']
        verify = request.form['verify']
        my_data = Internapply(sname=sname,cname=cname,course=course,email=email,verify=verify,internship=obj.internship,organisation=obj.organisation,postdate=obj.postdate)
       
        db.session.add(my_data) 
       
        db.session.commit()
        return redirect('/viewintern_stu')
    return render_template('internapply_stu.html', obj=obj)


@app.route('/viewstuapplied_pro')
def viewstuapplied_pro():
    mat=Internapply.query.filter_by(verify='agree')
    return render_template("viewstuapplied_pro.html",mat=mat)





 ###############################


@app.route('/pdf',methods=["GET","POST"])
def pdf():
    
    pdf = render_template('student_index.html')
    pdfkit.from_string(pdf, 'out3.pdf')




@app.route('/adddrive_place',methods=['GET', 'POST'])
def adddrive_place():
    if request.method == 'POST':
        drive = request.form['drive']
        testdate = request.form['testdate']
        testlocation = request.form['testlocation']
        regenddate = request.form['regenddate']
        qualification = request.form['qualification']
        postdate = request.form['postdate']
        
        my_data = Postdrive(drive=drive,testdate=testdate,testlocation=testlocation,regenddate=regenddate,qualification=qualification,postdate=postdate)
       
        db.session.add(my_data) 
        
        db.session.commit()
        
        d=Student.query.all()
        for i in d:
            sendmail(i.email)
           
        flash("Registered successfully! Please Login..")
        return redirect('/place_index') 
        
    else :
        return render_template("adddrive_place.html")


def sendmail(email):
    d=Student.query.all()
    
    for i in d:
     
         msg = Message('New Drive Alert!!!!!!',
                  recipients=[i.email])
         msg.body = f''' We are Posted New Drives . Please verify through your account'''
         mail.send(msg)


@app.route('/viewdrive_stu')
def viewdrive_stu():
    mat=Postdrive.query.all()
    return render_template("viewdrive_stu.html",mat=mat)



@login_required
@app.route('/driveapply_stu/<int:id>', methods=['GET', 'POST'])
def driveapply_stu(id):
    obj = Postdrive.query.get_or_404(id)
    if request.method == 'POST':
        sname = request.form['sname']
        cname = request.form['cname']
        course = request.form['course']
        email = request.form['email']
        verify = request.form['verify']
        my_data = Driveapply(sname=sname,cname=cname,course=course,email=email,verify=verify,drive=obj.drive,postdate=obj.postdate)
       
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/viewdrive_stu')
    return render_template('driveapply_stu.html', obj=obj)



@app.route('/viewstuapplied_place')
def viewstuapplied_place():
    mat=Driveapply.query.filter_by(verify='agree')
    return render_template("viewstuapplied_place.html",mat=mat)

@app.route('/deletedrive_place/<int:id>')
def deletefee(id):
    delet = Postdrive.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewdrive_place')
    except:
        return 'There was a problem deleting that task'

@app.route('/viewdrive_place')
def viewdrive_place():
    mat=Postdrive.query.all()
    return render_template("viewdrive_place.html",mat=mat)

 



@app.route('/scrapJobs')
def scrapandinsertJobs():
    today = date.today()
    # get input from user for job title and location
    # job_title = input('Enter job title: ')
    # job_location = input('Enter location for job: ')
    # experience_level = input('Choose experience category(Entry, Mid, Senior): ')

    job_title = ''
    job_location = 'india'
    experience_level = ''

    # assign experience level to corresponding url format using conditional
    # if experience_level.lower()[0] == 'e':
    #     experience_level = 'entry_level'
    # elif experience_level.lower()[0] == 'm':
    #     experience_level = 'mid_level'
    # elif experience_level.lower()[0] == 's':
    #     experience_level = 'senior_level'


    # function to replace spaces/commas in title and location for url format
    def format_strings(user_input):
        user_input = user_input.replace(' ', '%20')
        user_input = user_input.replace(',', '%2C')
        return user_input


    # call to function to format the user input
    job_title = format_strings(job_title)
    job_location = format_strings(job_location)

    # initialize empty list for jobs to be added to
    job_list = []

    # loop and increment count to switch over to next page of jobs
    count = 0
    for count in range(0, 40, 10):
        # fill in indeed url with given user input
        url = 'https://in.indeed.com/jobs?q={}&l={}&explvl={}&sort=date&start={}'.format(job_title.lower(), job_location,
                                                                                        experience_level, count)
        print(url)

        # get source code from website using requests library
        source = requests.get(url).text

        # pass website into beautiful soup
        soup = BeautifulSoup(source, 'html.parser')

        # find all job postings using the div found in the html
        posts = soup.select('a[class*="tapItem fs-unmask result"]')

        # loop through the div to get info for csv
        for post_info in posts:
            # get title from html using the second occurence of span
            try:
                title = post_info.find_all('span')[1].text
                #print(title)
            except Exception as e:
                title = 'NA'
                #print(title)

            # get company name
            try:
                company_name = post_info.find('span', class_='companyName').a.text
                #print(company_name)
            except Exception as e:
                company_name = 'NA'
                #print(company_name)

            # get location of job
            try:
                location = post_info.find('div', class_='companyLocation').text
                #print(location)
            except Exception as e:
                location = 'NA'
                #print(location)

            # get company pay
            try:
                pay = post_info.find('span', class_='salary-snippet').text
                #print(pay)
            except Exception as e:
                pay = 'NA'
                #print(pay)

            # get job summary bullest
            try:
                # get summary of job ([-1] so we do not get the more section on bottom)
                job_summary = post_info.find_all('li')[:-3]
                if len(job_summary) == 0:
                    summary_bullets = 'NA'
                    #print(summary_bullets)
                else:
                    for summary_bullets in job_summary:
                        summary_bullets = '•{}'.format(summary_bullets.text)
                        #print(summary_bullets)
            except Exception as e:
                summary_bullets = 'NA'
                #print(summary_bullets)

            # get vjk for the url
            job_jk = post_info.get(('data-jk'))
            post_url = 'https://www.indeed.com/viewjob?jk={}'.format(job_jk)
            #print(post_url)
            #print()

            # get posting date
            # try:
            #     posting_date = post_info.find('span', class_='date').text
            #     print(posting_date)
            # except Exception as e:
            #     posting_date = 'NA'
            #     print(posting_date)

            #print()

            # save info into dict for importing into csv
            job_info = {
                'title': title,
                'company_name': company_name,
                'location': location,
                'pay': pay,
                'summary_bullets': summary_bullets,
                'post_url': post_url
            }
            print(job_info)
            status = 1;
            created_date = today.strftime("%d/%m/%Y");
            
            jobData=Jobs(title=title,company_name=company_name,location=location,pay=pay,summary_bullets=summary_bullets,post=post_url, status=status,created_date=created_date)
            print(jobData)
            # append jobs to list
            try:
                db.session.add(jobData)
                db.session.commit()
            except Exception as e:
                print(e)
            job_list.append(job_info)

    #print('job list')
   # print(job_list)

    #add the data to the csv file
    #display job_list dict as data frame
    #df = pd.DataFrame(job_list)

    #get clean looking file name for user
    #csv_title = '{}Jobs'.format(job_title)
    #suffix = '.csv'
    #csv_title = csv_title.replace('%20', '_')
    #csv_title = csv_title + suffix

    #write the data to the file
    #df.to_csv(csv_title)
    #print('Data added to .csv file')
    
    return render_template("index.html")



@app.route('/jobs')
def jobs():
    mat=Jobs.query.all()
    return render_template("webscrap.html",mat=mat)


@app.route('/viewresumestu_place')
def viewresumestu_place():
    mat=Resume.query.all()
    return render_template("viewresumestu_place.html",mat=mat)

@app.route('/viewresumeseek_pro')
def viewresumeseek_pro():
    mat=Resume.query.all()
    return render_template("viewresumeseek_pro.html",mat=mat)


@app.route('/viewstu_place')
def viewstu_place():
    mat=Student.query.all()
    return render_template("viewstu_place.html",mat=mat)


@login_required
@app.route('/editstu_place/<int:id>', methods=['GET', 'POST'])
def editstu_place(id):
    obj = Student.query.get_or_404(id)
    if request.method == 'POST':
        obj.sname = request.form['sname']
        obj.collegename = request.form['cname']
        obj.university = request.form['university']
        obj.course = request.form['course']
        obj.email = request.form['email']
        obj.password = request.form['password']
        obj.pid = request.form['pid']
        db.session.commit()
        return redirect('/viewstu_place')
    return render_template('editstu_place.html', obj=obj)

@app.route('/deletestu_place/<int:id>')
def deletestu_place(id):
    delet = Student.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewstu_place')
    except:
        return 'There was a problem deleting that task'