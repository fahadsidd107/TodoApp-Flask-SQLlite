from email.policy import default
from turtle import title
from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    des = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno}-{self.title}'
        


@app.route("/")
def hello_world():
    todo = Todo(title='Hello', des='World')
    db.session.add(todo)
    db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html" , all_todo = all_todo)
    # return "<h1>Hello, World!</h1>"

@app.route("/show")
def products():
    all_todo = Todo.query.all()
    print(all_todo)
    return "<h1>Products</h1>"

if __name__ == "__main__":
    app.run(debug=True)