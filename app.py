from flask import Flask,render_template,request,redirect,url_for
# importin SQLAchemmy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# creating configs
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:morgan8514@127.0.0.1:5432/todo'
app.config['SECRETE_KEY']='secret_key'


# insantiate db
db = SQLAlchemy(app)

@app.before_first_request
def drop():
    db.create_all()


# import model
from models.all_todo_model import Todo

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
        print('updated content recieved')

    
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

# creating a route to edit the todo
@app.route('/add_todo/delete/<int:id>', methods=['GET'])
def delete_todo(id):
    # calling the delete function
    delete_me=Todo.del_by_id(id)
    # if delete_me:
    #     print('deleted')
    
    return redirect(url_for('todo'))





if __name__ == '__main__':
    app.run(debug=True)
