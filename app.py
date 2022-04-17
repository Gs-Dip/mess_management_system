import json
from flask import Flask,redirect,render_template,request,flash,session, url_for  
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
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
login_manager=LoginManager(app)
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



class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    admissionid=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(50))


class Userinfo(UserMixin,db.Model):   
    id=db.Column(db.Integer,primary_key=True)
    admissionid=db.Column(db.String(1000))
    name=db.Column(db.String(50)) 
    email=db.Column(db.String(50),unique=True)
    address=db.Column(db.String(1000))
    phone=db.Column(db.Integer)



@app.route('/')
def home():
    return render_template('home.html')   



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="POST":
        addmissionid=request.form.get('addmissionid')
        addmissionid=addmissionid.upper()
        name=request.form.get('name')
        email=request.form.get('email')  
        address=request.form.get('address')  
        phone=request.form.get('phone')   
        encriptpassword=generate_password_hash(addmissionid)   
         

        id=User.query.filter_by(admissionid=addmissionid).first()
        Username=User.query.filter_by(name=name).first()

        checkuser=Userinfo.query.filter_by(admissionid=addmissionid).first()
        checkemail=Userinfo.query.filter_by(email=email).first()

        if checkuser or checkemail:
            flash("AdmissionId and Emailaddress already taken","danger")
            return render_template("signup.html")

        elif id and Username:  
            new_user=db.engine.execute(f"INSERT INTO `userinfo` (`admissionid`,`name`,`email`,`address`,`phone`) VALUES ('{encriptpassword}','{name}','{email}','{address}','{phone}') ")
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
        
        user=Userinfo.query.filter_by(name=name).first()
        
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
            return render_template('dashboard.html')


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
  
    return render_template('dashboard.html')


@app.route('/alluser')  
def alluser():
    return render_template('alluser.html')  


@app.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method=="POST":
        name=request.form.get('name')
        admissionid=request.form.get('admissionid')
        admissionid=admissionid.upper()
        db.engine.execute(f"INSERT INTO `user` (`admissionid`,`name`) VALUES ('{admissionid}','{name}') ")
        flash("Successfully Inserted Data On Your DataBase","success")
        return render_template("adduser.html")

    return render_template('adduser.html')


@app.route('/dailybazarexpenses')
def dailybazarexpenses():
    return render_template('daily-bazar-expenses.html')    


@app.route('/mealrecord')
def mealrecord():
    return render_template('meal-record.html')    


@app.route('/bazarrecord')
def bazarrecord():
    return render_template('bazar-record.html')    


@app.route('/endofmonth')
def endofmonth():
    return render_template('end-of-month.html') 



@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html')       


@app.route('/userdailybazarexpense')
def userdailybazarexpense():
    return render_template('userdailybazarexpense.html') 


@app.route('/usermealrecord')
def usermealrecord():
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