# importing db
from main import db
# creating a db
class Todo_(db.Model):
    __tablename__= 'todo_table'
    id = db.Column(db.Integer,primary_key=True)
    todo_content = db.Column(db.String(),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    
    

    # create method to send data to db
    def create(self):
        db.session.add(self)
        db.session.commit()
        

# creating a method to get the content in  the db and edit it
    @classmethod
    def update_by_id(cls,id,content=None):
        queried_content=cls.query.filter_by(id=id).first()
        if queried_content:
            queried_content.todo_content=content
            db.session.commit()
            return True

        else:
            return False


# creating a function to delete
    @classmethod
    def del_by_id(cls,id):
        fetch_del_id=cls.query.filter_by(id=id)
        if fetch_del_id.first():
            fetch_del_id.delete()
            db.session.commit()
            return True
        else:
            return False



        

        
           


    