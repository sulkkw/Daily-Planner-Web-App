from email.policy import default
from xmlrpc.client import DateTime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
#set up application
app = Flask(__name__) 
#setup databse
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db' 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app) 

#defining what to store in database 
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #return name of the task and id of the task 
    def __repr__(self) -> str:
        return '<Task %r>' % self.id 

#create index route to avoid error 404
@app.route('/', methods=['POST', 'GET']) 
#function for the route 
def index(): 
    #Check if request from the user was performed 
    if request.method == 'POST': 
        #task_conetent will hold the result of content in HTML form that user input
        task_content = request.form['content'] 
        
        new_task = Todo(content=task_content)

        try: 
            #add to db
            db.session.add(new_task) 
            db.session.commit()
            #redirect to homepage
            return redirect('/')
        
        except: 
            return "Your task could not be added"
    
    else: 
        #check the order  of task created and return all of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>') 
def delete(id): 
    task_to_delete = Todo.query.get_or_404(id) 

    try: 
        db.session.delete(task_to_delete) 
        db.session.commit() 
        return redirect('/') 
    except: 
         return "Task could not be deleted"

@app.route('/update/<int:id>', methods=['GET', 'POST']) 
def update(id): 
    task= Todo.query.get_or_404(id) 
    if request.method == 'POST': 
        task.content = request.form['content'] 

        try: 
            db.session.commit() 
            return redirect('/')
        
        except: 
            return "Task could not be updated"
    else: 
        return render_template('update.html', task=task)

if __name__ == "__main__": 
    app.run(debug=True) 
