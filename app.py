from flask import Flask,render_template,request,redirect,url_for,flash
# importin SQLAchemmy
from flask_sqlalchemy import SQLAlchemy
from forms.authentication import Register,Login
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
# creating configs
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:morgan8514@127.0.0.1:5432/todo'
app.config['SECRET_KEY']='secret'



# insantiate db
db = SQLAlchemy(app)

@app.before_first_request
def create():
    db.create_all()


# import model
from models.all_todo_model import Todo
from models.users import Users

# resetin password route
@app.route('/reset/password')
def reset_password():
    return render_template('forgot_password.html')

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
        
        if email_check:
            print("exist")
            return redirect(url_for("user_registration"))
        else:
            user_commit = Users(user_name = name, email=email,password=generate_password_hash(password))
            user_commit.create()
            print("record created")
            return redirect(url_for("login"))

    return render_template ('register.html',form=form) 
# route for login page
@app.route('/login', methods=['GET','POST'])
def login():
    form = Login(request.form)
    if request.method=="POST":
        email= request.form.get("email")
        password = request.form.get("password")

        # check if email exists
        check_email=Users.email_checker(email=email)
        if not check_email:
            print("email not found")
        else:

            chck_password= Users.password_checker(email=email,password=password)
            if chck_password:
                print("loggged in")

                return redirect(url_for("home"))

        
            return redirect(url_for("login"))

        # if email is found,check password if correct



    return render_template('login.html',form=form)

@app.route('/')
def home():
    return render_template ('homepage.html')


# route for todo
@app.route('/todo', methods=['GET','POST'])
def todo():
       # fetching all data from db
    all_data_in_db=Todo.query.all()
    if request.method=='POST':
        updated_content=request.form['updated_text']
        flash('updated content recieved')

    
    return render_template ('view_todo.html',all_data_in_db=all_data_in_db)


@app.route('/add_todo',methods=['POST','GET'])
def add_todo():

    if request.method=='POST':
        entered_data=request.form['entered_text']
    #    equating enter data to db column
        data=Todo(todo_content=entered_data)
         # sendind to db
        data.create()
        # print('imeingia')
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
        return redirect(url_for('todo'))

# creating a route to delete the todo
@app.route('/add_todo/delete/<int:id>', methods=['GET'])
def delete_todo(id):
    # calling the delete function
    delete_me=Todo.del_by_id(id)
    # if delete_me:
    #     print('deleted')
    
    return redirect(url_for('todo'))





if __name__ == '__main__':
    app.run(debug=True)
