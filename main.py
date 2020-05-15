from flask import Flask,render_template,request,redirect,url_for,session ,g,flash
# importin SQLAchemmy
from flask_sqlalchemy import SQLAlchemy
from forms.authentication import Register,Login
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import os

DB_URL = ''
DB_URL_PRODUCTION = ''

app = Flask(__name__)
# creating configs
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY']=os.urandom(24)



# insantiate db
db = SQLAlchemy(app)

@app.before_first_request
def create():
    db.create_all()

# login  required wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            print("Unauthorized")
            return redirect(url_for('login'))
    return decorated_function

# import model
from models.all_todo_model import Todo
from models.users import Users


# creating registtration route
@app.route('/register',methods=["POST","GET"])
def user_registration():
    form = Register(request.form)
    if request.method=="POST":
        name=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password") 
        
        # checking if entered email exists
        email_check=Users.email_checker(email=email)
        
        if not email_check:
            user_commit = Users(user_name = name, email=email,password=generate_password_hash(password))
            user_commit.create()
            message="registration success! proceed to Login "
            return render_template ('register.html',form=form , message=message)  
            
            
            # return render_template ('register.html',form=form,message=message)
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
        check_email=Users.email_checker(email=email)
        if  check_email:

            chck_password= Users.password_checker(email=email,password=password)
            if chck_password:
                # flash("loggegin","success")
                # print("loggged in")
                session["logged_in"] = True
                session["username"] = check_email.user_name
                session["id"] = check_email.id

                return redirect(url_for("home"))
            else:
                print("wrong passwrod")
                error_password="incorrect password"
                
                return render_template('login.html',form=form,error_password=error_password)


        else:
            print("no email found")
            error="email not registered login"

    return render_template('login.html',form=form,error=error)

@app.route('/')
@login_required
def home():

    return render_template ('homepage.html')


# route for todo
@app.route('/todo', methods=['GET','POST'])
def todo():
       # fetching all data from db

    all_data_in_db=Todo.query.filter_by(user_id=session["id"])
    # filter here by session id
    
    if request.method=='POST':
        updated_content=request.form['updated_text']
        flash('updated content recieved')

    
    return render_template ('view_todo.html',all_data_in_db=all_data_in_db)

# viewing pad
@app.route('/add_todo',methods=['POST','GET'])
@login_required
def add_todo():

    if request.method=='POST':
        entered_data=request.form['entered_text']
    #    equating enter data to db column
        data=Todo(todo_content=entered_data,user_id=session["id"])
         # sendind to db
        data.create()
        # print('imeingia')
        flash(f"Todo created! ","success")
        return redirect(url_for('add_todo'))
    
    return render_template ('add_todo.html')

# creating a route to edit the todo
@app.route('/add_to/edit<int:id>', methods=['POST','GET'])
def editing_todo(id):
    if request.method=='POST':
        recieved_content=request.form['updated_content']
        # print(recieved_content)
# sending update to db
        to_db_recieved_content=Todo.update_by_id(id=id,content=recieved_content)
        # print('commited')
        flash(f"Todo updated! ","success")
        return redirect(url_for('todo'))

# creating a route to delete the todo
@app.route('/add_todo/delete/<int:id>', methods=['GET'])
def delete_todo(id):
    # calling the delete function
    delete_me=Todo.del_by_id(id)
    # if delete_me:
    #     print('deleted')
    flash(f"Todo deleted! ","danger")
    
    return redirect(url_for('todo'))


@app.route('/logout')
def logout():
    
    session.clear()
    

    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
