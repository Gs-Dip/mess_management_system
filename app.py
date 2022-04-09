import json
from flask import Flask,redirect,render_template,request,flash,session  
from flask_sqlalchemy import SQLAlchemy
from importlib_metadata import re
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
app.secret_key="password"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dipdip2020@localhost/mess_management'
db=SQLAlchemy(app)



class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))




@app.route('/')
def home():
    return render_template('home.html')   



@app.route('/signup')
def signup():
    return render_template('signup.html')     


@app.route('/userlogin') 
def userlogin():
    return render_template('userlogin.html')   



@app.route('/adminlogin')  
def adminlogin():
    return render_template('adminlogin.html')  


@app.route('/admindashboard')    
def admindashboard():
    return render_template('dashboard.html')


@app.route('/alluser')  
def alluser():
    return render_template('alluser.html')  


@app.route('/adduser')
def adduser():
    return render_template('adduser.html')


@app.route('/dailybazarexpenses')
def dailybazarexpenses():
    return render_template('daily-bazar-expenses.html')    


@app.route('/mealrecord')
def mealrecord():
    return render_template('meal-record.html')    


@app.route('/endofmonth')
def endofmonth():
    return render_template('end-of-month.html') 



@app.route('/userdashboard')
def userdashboard():
    return render_template('userdashboard.html')       


@app.route('/userdailybazarexpense')
def userdailybazarexpense():
    return render_template('userdailybazarexpense.html') 





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