from flask import Flask,render_template,request,redirect# what is request library
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
# Static folder is used to upload your files exactly in the same format.
#Now we are creating a database and flask will help us-->
# Sqlalchemy is OMR mapper used to make changes in the database in flask with using python code.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
with app.app_context():
    db = SQLAlchemy(app)

    
# the upper code has created the databse and now we are the defining the database-->
class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"




@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    #creating todo instance-->
        
    allTodo = Todo.query.all()
    #print(allTodo)
    return render_template('index.html',allTodo = allTodo) # passing a python variable to index.html file

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, port=8000)
