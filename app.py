import json
from flask import Flask,redirect,render_template,request,flash,session, url_for  
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from markupsafe import string
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from flask_mail import Mail 

#akhane json file ta open kora hoyeche....admin login ar jonno
with open('config.json','r') as c:
    jsondata=json.load(c)["jsonfile"]




app=Flask(__name__)
app.secret_key="password"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dipdip2020@localhost/mess_management'
db=SQLAlchemy(app)

#this is for getting the unique user access
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return Userinfo.query.get(int(user_id))


#akhane flask-mail ke configure kora hoyeche------
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=jsondata['gmail-user'], 
    MAIL_PASSWORD=jsondata['gmail-password']
    
)
mail=Mail(app)     


# all class ---------------------------------------------
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    admissionid=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50))


class Userlogin(UserMixin,db.Model):   
    id=db.Column(db.Integer,primary_key=True)
    admissionid=db.Column(db.String(1000))
    name=db.Column(db.String(50)) 
    email=db.Column(db.String(50),unique=True)
    address=db.Column(db.String(1000))
    phone=db.Column(db.String(50))



class Userinfo(UserMixin,db.Model):   
    id=db.Column(db.Integer,primary_key=True)
    admissionid=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50)) 
    email=db.Column(db.String(50),unique=True)
    address=db.Column(db.String(1000))
    phone=db.Column(db.String(50))

class Daily_bazarexpense(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    addmissionid=db.Column(db.String(50))
    name=db.Column(db.String(50))
    bazarinfo=db.Column(db.String(5000))
    amount=db.Column(db.Integer)
    date=db.Column(db.Date)    

class Meal_record(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    addmissionid=db.Column(db.String(50))
    name=db.Column(db.String(50))
    date=db.Column(db.Date)
    breakfast=db.Column(db.Integer)
    lunch=db.Column(db.Integer)
    dinner=db.Column(db.Integer)     


@app.route('/')
def home():
    return render_template('home.html')   



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="POST":
        addmissionid=request.form.get('addmissionid')
        addmissionid=addmissionid.upper()
        name=request.form.get('name')
        name=name.lower()
        email=request.form.get('email')  
        address=request.form.get('address')  
        phone=request.form.get('phone')   
        encriptpassword=generate_password_hash(addmissionid)   
         

        id=User.query.filter_by(admissionid=addmissionid).first()
        Username=User.query.filter_by(name=name).first()

        checkuser=Userlogin.query.filter_by(admissionid=addmissionid).first()
        checkemail=Userlogin.query.filter_by(email=email).first()

        if checkuser or checkemail:
            flash("AdmissionId and Emailaddress already taken","danger")
            return render_template("signup.html")

        elif id and Username:  
            new_user=db.engine.execute(f"INSERT INTO `userlogin` (`admissionid`,`name`,`email`,`address`,`phone`) VALUES ('{encriptpassword}','{name}','{email}','{address}','{phone}') ")

            db.engine.execute(f"INSERT INTO `userinfo` (`admissionid`,`name`,`email`,`address`,`phone`) VALUES ('{addmissionid}','{name}','{email}','{address}','{phone}') ")
            flash("Signup Success!!! Please Login","success")
            return render_template("userlogin.html")

       


        else:
            flash("The admin has not provided your signup access yet..please try Again later","info")
            return render_template("signup.html")

    return render_template("signup.html")



        
@app.route('/userlogin',methods=['GET','POST']) 
def userlogin():      
      if request.method=="POST":
        name=request.form.get('name')
        admissionid=request.form.get('admissionid')
        name=name.lower()
        admissionid=admissionid.upper()
        
        user=Userlogin.query.filter_by(name=name).first()
        
        if user and check_password_hash(user.admissionid,admissionid): 
            login_user(user)
            flash("Login Success!!!","info")
            return render_template("userdashboard.html")

        else:
            flash("Login Faild try again!!!","danger") 
            return render_template("userlogin.html")
        
      return render_template('userlogin.html')   


#admin login------------------------------
@app.route('/adminlogin',methods=['GET','POST'])  
def adminlogin():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        if(username==jsondata['user'] and password==jsondata['password']):
            session['user']=username
            flash("Login Success!!!","success")
            return redirect('/admindashboard')


        else:
            flash("Login Failed!!!","danger")
    
    return render_template('adminlogin.html')  


#admin logout-----------------------------------------
@app.route('/adminlogout')       

def adminlogout():
    session.pop('user')
    flash("Admin Logout Successful!!!","primary")
    return render_template("adminlogin.html")    



#user logout---------------------------------
@app.route('/userlogout')
def userlogout():
    logout_user()
    flash("Logout Successful","warning")
    return render_template("userlogin.html")



@app.route('/admindashboard')    
# @login_required
def admindashboard():   
    alluser=db.engine.execute("SELECT COUNT(*) FROM userinfo") 
    alluser=alluser.fetchone() #akhane fetchone()  bebohar korar karon holo userinfo theke total row jog korar  por shudhu sonkha ta pawar jonno.....
    
    totalbazar=db.engine.execute("SELECT COUNT(*) FROM daily_bazarexpense")
    totalbazar=totalbazar.fetchone()
    
      
    return render_template('dashboard.html',alluser=alluser,totalbazar=totalbazar)


@app.route('/alluser')  
def alluser():
    data=db.engine.execute("SELECT * From userinfo")

    return render_template('alluser.html',data=data)  


@app.route('/useredit/<string:id>',methods=['GET','POST'])
def useredit(id):
    if request.method=="POST":
        
        name=request.form.get('name')
        admissionid=request.form.get('admissionid')
        address=request.form.get('address')
        email=request.form.get('email')
        phone=request.form.get('phone')
        

        admissionid=admissionid.upper()
        name=name.lower()
        encriptpassword=generate_password_hash(admissionid)

        db.engine.execute(f"UPDATE `userlogin` SET `admissionid`='{encriptpassword}',`name`='{name}',`address`='{address}',`email`='{email}',`phone`='{phone}' WHERE `userlogin`.`id`={id}")

        db.engine.execute(f"UPDATE `userinfo` SET `admissionid`='{admissionid}',`name`='{name}',`address`='{address}',`email`='{email}',`phone`='{phone}' WHERE `userinfo`.`id`={id}")

        flash("User Update Successfully","info")
 
        return redirect("/alluser")

    post=Userinfo.query.filter_by(id=id).first()
    return render_template('useredit.html',post=post)    


@app.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method=="POST":
        name=request.form.get('name')
        admissionid=request.form.get('admissionid')
        admissionid=admissionid.upper()
        name=name.lower()
        db.engine.execute(f"INSERT INTO `user` (`admissionid`,`name`) VALUES ('{admissionid}','{name}') ")
        
        flash("Successfully Inserted Data On Your DataBase","success")
        return redirect("/adduser")


    getdata=db.engine.execute("SELECT * From user")
    return render_template('adduser.html',getdata=getdata)

#clear all data route------------------------------------------------------- 
@app.route('/deletealldata')
def deleteadduser():
    db.engine.execute("DELETE FROM user")
    db.engine.execute("DELETE FROM userinfo")
    db.engine.execute("DELETE FROM userlogin")
    db.engine.execute("DELETE FROM daily_bazarexpense")
        
    return redirect("/admindashboard")     

#admin daily bazar expenses-----------------------------------
@app.route('/dailybazarexpenses')
def dailybazarexpenses():    
    getdata=db.engine.execute("SELECT * From daily_bazarexpense")
    return render_template('daily-bazar-expenses.html',getdata=getdata)   




@app.route('/adminbazaredit/<string:id>',methods=['GET','POST'])
def adminbazaredit(id):
    if request.method=="POST":
        date=request.form.get('date')
        addmissionid=request.form.get('addmissionid')
        name=request.form.get('name')
        bazarinfo=request.form.get('bazarinfo')
        amount=request.form.get('amount')
        

        addmissionid=addmissionid.upper()
        name=name.lower()
        

        db.engine.execute(f"UPDATE `daily_bazarexpense` SET `date`='{date}',`name`='{name}',`addmissionid`='{addmissionid}',`bazarinfo`='{bazarinfo}',`amount`='{amount}' WHERE `daily_bazarexpense`.`id`={id}")
         
        flash("Bazar Record Update Successfully","success") 
        return redirect("/dailybazarexpenses")


    postdata=Daily_bazarexpense.query.filter_by(id=id).first()
    return render_template('adminbazaredit.html',postdata=postdata)     

#admin meal record---------------
@app.route('/mealrecord')
def mealrecord():
    getdata=db.engine.execute("SELECT * FROM meal_record")
    
    return render_template('meal-record.html',postdata=getdata)    


@app.route('/editmealrecord/<string:id>',methods=['GET','POST'])
def editmealrecord(id):
        if request.method=="POST":
            date=request.form.get('date')
            addmissionid=request.form.get('admissionid')
            name=request.form.get('name')
            breakfast=request.form.get('breakfast')
            lunch=request.form.get('lunch')
            dinner=request.form.get('dinner')
        

            addmissionid=addmissionid.upper()
            name=name.lower()
        

            db.engine.execute(f"UPDATE `meal_record` SET `date`='{date}',`name`='{name}',`addmissionid`='{addmissionid}',`breakfast`='{breakfast}',`lunch`='{lunch}',`dinner`='{dinner}' WHERE `meal_record`.`id`={id}")
         
            flash("Meal Record Update Successfully","success") 
            return redirect("/mealrecord")


        postdata=Meal_record.query.filter_by(id=id).first()
        return render_template('adminmealedit.html',postdata=postdata)



@app.route("/deletemeal/<string:id>",methods=['GET','POST'])

def hdelete(id):
    db.engine.execute(f"DELETE FROM `meal_record` WHERE  `meal_record`.`id`={id}")

    flash("Data Deleted Successfully","success")
    return redirect("/mealrecord")        

@app.route('/bazarrecord')
def bazarrecord():
    return render_template('bazar-record.html')    


@app.route('/endofmonth')
def endofmonth():
    return render_template('end-of-month.html') 



@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html')       


@app.route('/userdailybazarexpense',methods=['GET','POST'])
def userdailybazarexpense():
    if request.method=="POST":
        date=request.form.get('date') 
        addmissionid=request.form.get('admissionid')       
        name=request.form.get('name')        
        bazarinfo=request.form.get('bazarinfo')
        amount=request.form.get('amount')
        
        addmissionid=addmissionid.upper()
        name=name.lower()

        db.engine.execute(f"INSERT INTO `daily_bazarexpense` (`date`,`addmissionid`,`name`,`bazarinfo`,`amount`) VALUES ('{date}','{addmissionid}','{name}','{bazarinfo}','{amount}')")
        flash("Record Added Successfully","success")
        return render_template('userdailybazarexpense.html')
    return render_template('userdailybazarexpense.html') 


@app.route('/usermealrecord',methods=['GET','POST'])
def usermealrecord():
    if request.method=="POST":
        date=request.form.get('date')
        addmissionid=request.form.get('admissionid')
        addmissionid=addmissionid.upper()
        name=request.form.get('name')
        name=name.lower()
        breakfast=request.form.get('breakfast')
        lunch=request.form.get('lunch')
        dinner=request.form.get('dinner')

        db.engine.execute(f"INSERT INTO `meal_record` (`date`,`addmissionid`,`name`,`breakfast`,`lunch`,`dinner`) VALUES ('{date}','{addmissionid}','{name}','{breakfast}','{lunch}','{dinner}')")
        flash("Record Added Successfully","success")
        return redirect("/usermealrecord")
        
        
    return render_template('usermealrecord.html')    


@app.route('/usermessage')
def usermessage():
    return render_template('usermessage.html')   


@app.route('/userendofmonth')
def userendofmonth():
    return render_template('userendofmonth.html')     





@app.route('/test')
def test():
    try:
        a=Test.query.all()
        print(a)
        return "DATABASE Is successfully connected"

    except Exception as e:
        print(e)
        return f'my database is not connected {e}'    





if __name__=='__main__':
    app.run(debug=True,port=9000)