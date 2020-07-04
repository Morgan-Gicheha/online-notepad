from flask import Flask,render_template,request,redirect,url_for,session ,g,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from forms.authentication import Register,Login
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from oa import oauth, github
import os
import json

DB_URL = ''
DB_URL_PRODUCTION = ''
SQLLITE_DB= "sqlite:///db_todo.db"

app = Flask(__name__)
# creating configs
app.config['SQLALCHEMY_DATABASE_URI'] = SQLLITE_DB
app.config['SECRET_KEY']=os.urandom(20)




# insantiate db
db = SQLAlchemy(app)

@app.before_first_request
def create():
    oauth.init_app(app)
    db.create_all()

# login  required wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

# import model
from models.all_todo_model import Todo_
from models.users import Users_
 
#  github login
@app.route("/github")
def github_login():
    resp = github.authorize(url_for("authorized",_external=True))
    
    return resp


@app.route("/login/github/authorized")
def authorized():
    response = github.authorized_response()
    if response is None or response["access_token"] is None:
        flash("We have a problem with github authentication. Try again later as we fix the issue or login normaly.")
        return redirect(url_for("login"))
        
    access_token = response['access_token']
    github_user = github.get('user', token= access_token)
    #  github info about the user
    username= github_user.data["login"]
    email = github_user.data["email"]


        # working with username
    if email is  None and username is not None:
        github_username= Users_.query.filter_by(user_name= username).first()
        if github_username:
            
            session["logged_in"] = True
            session["username"] = github_username.user_name
            session["id"] = github_username.id
            return redirect(url_for("home"))
        else:
            save_username=Users_(user_name=username)
            save_username.create()

            github_username = Users_.query.filter_by(user_name= username).first()
            
            session["logged_in"] = True
            session["username"] = github_username.user_name
            session["id"] = github_username.id
            return redirect(url_for("home"))

    
    # working with email
    if email is not None:
        # checking if email is in our db
        user_email=Users_.query.filter_by(email=email).first()
        if user_email:
            # checking if user has username
            if user_email.user_name is not None:
                        session["logged_in"] = True
                        session["username"] = user_email.user_name
                        session["id"] = user_email.id
                        return redirect(url_for("home"))
            else:
                    session["logged_in"] = True
                    session["username"] = user_email.email
                    session["id"] = user_email.id
                    return redirect(url_for("home"))
        else:
            save_email= Users_(email=email)
            save_email.create()

            user_email=Users_.query.filter_by(email=email).first()
            session["logged_in"] = True
            session["username"] = user_email.email
            session["id"] = user_email.id
            return redirect(url_for("home"))



# creating registtration route
@app.route('/register',methods=["POST","GET"])
def user_registration():
    form = Register(request.form)
    if request.method=="POST":
        name=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password") 
        # checking if entered email exists
        email_check=Users_.email_checker(email=email)
        
        if not email_check:
            user_commit = Users_(user_name = name, email=email,password=generate_password_hash(password))
            user_commit.create()
            message="registration success! proceed to Login "
            return render_template ('register.html',form=form , message=message)  
        else:
            email_error="email is already registered"
            return render_template ('register.html',form=form,email_error=email_error)         
    return render_template ('register.html',form=form) 
# route for login page
@app.route('/login', methods=['GET','POST'])

def login():
    error= None
    form = Login(request.form)
    if request.method=="POST":
        email= request.form.get("email")
        password = request.form.get("password")
        # check if email exists
        check_email=Users_.email_checker(email=email)
        if  check_email:
            chck_password= Users_.password_checker(email=email,password=password)
            if chck_password:
                session["logged_in"] = True
                session["username"] = check_email.user_name
                session["id"] = check_email.id
                return redirect(url_for("home"))
            else:
                error_password="incorrect password"
                return render_template('login.html',form=form,error_password=error_password)
        else:
            error="email not registered login"
    return render_template('login.html',form=form,error=error)

@app.route('/')
@login_required
def home():
    return render_template ('homepage.html')

@app.route('/todo', methods=['GET','POST'])
def todo():
    all_data_in_db=Todo_.query.filter_by(user_id=session["id"])
    if request.method=='POST':
        updated_content=request.form['updated_text']
        flash('updated content recieved')
    return render_template ('view_todo.html',all_data_in_db=all_data_in_db)

@app.route('/add_todo',methods=['POST','GET'])
@login_required
def add_todo():
    if request.method=='POST':
        entered_data=request.form['entered_text']
        data=Todo_(todo_content=entered_data,user_id=session["id"])
        data.create()
        flash(f"Todo created! ","success")
        return redirect(url_for('add_todo'))
    return render_template ('add_todo.html')

# creating a route to edit the todo
@app.route('/add_to/edit<int:id>', methods=['POST','GET'])
def editing_todo(id):
    if request.method=='POST':
        recieved_content=request.form['updated_content']
        to_db_recieved_content=Todo_.update_by_id(id=id,content=recieved_content)
        flash(f"Todo updated! ","success")
        return redirect(url_for('todo'))

# creating a route to delete the todo
@app.route('/add_todo/delete/<int:id>', methods=['GET'])
def delete_todo(id):
    delete_me=Todo_.del_by_id(id)
    flash(f"Todo deleted! ","danger")
    return redirect(url_for('todo'))

@app.route('/logout')
def logout():  
    session.clear()   
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
