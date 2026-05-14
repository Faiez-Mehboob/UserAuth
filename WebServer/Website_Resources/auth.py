from flask import Blueprint, render_template, request, session, url_for, redirect, flash, current_app
import socket
import json


auth = Blueprint('auth',__name__)


@auth.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET','POST'])
def login():
    AuthHOST=current_app.config.get('AuthHOST')
    AuthPORT=current_app.config.get('AuthPORT')

    
    if 'user' in session:
        return redirect(url_for('dash.dashboard'))
        
    if(request.method=='POST'):
        data=request.form.to_dict()
        data["route"]= "login"
        try:   
            servsock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            servsock.connect((AuthHOST,AuthPORT))
            servsock.send(json.dumps(data).encode())
        except Exception as e:
            flash("Error Connecting to Authentication Server!",category="error")
            return render_template('login.html',data=data)
        
        while True:
            try:
                response=servsock.recv(4096).decode()
            except Exception as e:
                flash("Connection timed out!",category="error")
                return render_template('login.html',data=data)
            
            if (response=="Success"):
                session['user']=data['username']
                return redirect(url_for('dash.dashboard'))
            
            elif (response=="Failure"):
                flash("Username or Password Invalid!",category="error")
                return render_template("login.html",data=data)
    
    return render_template("login.html",data={})


@auth.route('/signup', methods=['GET','POST'])
def signup():
    AuthHOST=current_app.config.get('AuthHOST')
    AuthPORT=current_app.config.get('AuthPORT')

    
    if 'user' in session:
        return redirect(url_for('dash.dashboard'))
    
    if(request.method=='POST'):
        data=request.form.to_dict()
        data["route"] = "signup"
        
        if data["passwd"]!=data["repasswd"]:
            flash("Passwords don't match!","error")
            return render_template('signup.html',data=data)
                     
        try:
            servsock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            servsock.connect((AuthHOST,AuthPORT))
            servsock.send(json.dumps(data).encode())
        except Exception as e:
            flash("Error Connecting to Authentication Server!",category="error")
            return render_template('signup.html',data=data)
        
        while True:
            try:
                response=servsock.recv(4096).decode()
            except Exception as e:
                flash("Connection timed out!",category="error")
                return render_template('signup.html',data=data)
                    
            if (response=="Success"):
                flash("Account Created Successfully!",category="success")
                return render_template('signup.html',data={})
            
            elif (response=="Failure"):
                flash("Account with username already exists!",category="error")
                return render_template('signup.html',data={})
            
    return render_template('signup.html',data={})

 