# importing flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# setting up the application - referencing this file
app = Flask(__name__)
# telling our app where our database is located
# using 3 frwd slashes since we want a relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    # setting up some columns
    # id will be an integer that references id of each entry
    id = db.Column(db.Integer, primary_key=True)
    # max char content is 200, and the entry cannot be empty hence nullable=False
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # returning a string every time we create a new element
    def __repr__(self):
        return '<Task %r>' % self.id

# creating an index route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'
        
    else:
        # look at and return all db contents in order of date created
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# route for deleting an entry
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task.'

# route for updating an entry
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task=task)

# need to implement for updated flask
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug = True)